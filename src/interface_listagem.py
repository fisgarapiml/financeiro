import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Produtos Cadastrados", layout="wide")
st.title("📋 Lista de Produtos Cadastrados")

# Conexão com o banco de dados
@st.cache_resource
def conectar():
    db_path = os.path.join(os.path.dirname(__file__), "contas_apagar.db")
    return sqlite3.connect(db_path)

# Carregar todos os produtos
@st.cache_data
def carregar_produtos():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM produtos", conn)
    conn.close()
    return df

# Função para atualizar status
def atualizar_status(produto_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET ativo = ? WHERE id = ?", (novo_status, produto_id))
    conn.commit()
    conn.close()

# Carregar dados
df = carregar_produtos()

# Filtros
st.sidebar.header("🔍 Filtros")
tipos = df["tipo"].dropna().unique().tolist()
tipo_filtro = st.sidebar.multiselect("Tipo de Produto", tipos, default=tipos)

status_filtro = st.sidebar.selectbox("Status", ["Todos", "Ativos", "Inativos"])

# Aplicar filtros
df_filtrado = df[df["tipo"].isin(tipo_filtro)]
if status_filtro == "Ativos":
    df_filtrado = df_filtrado[df_filtrado["ativo"] == 1]
elif status_filtro == "Inativos":
    df_filtrado = df_filtrado[df_filtrado["ativo"] == 0]

st.markdown(f"### Produtos Encontrados: {len(df_filtrado)}")

# Exibir cards
for i in range(0, len(df_filtrado), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(df_filtrado):
            p = df_filtrado.iloc[i + j]
            with cols[j]:
                st.markdown(f"""
                <div style='background: #f9f9f9; border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
                    <h4 style='margin-bottom:5px;'>{p['nome']}</h4>
                    <p><strong>Código:</strong> {p['codigo']}</p>
                    <p><strong>Tipo:</strong> {p['tipo']}</p>
                    <p><strong>Unidade:</strong> {p['unidade_compra']} | <strong>Fator:</strong> {p['fator_conversao']}</p>
                    <p><strong>Preço Venda:</strong> R$ {p['preco_venda']:.2f} | <strong>Custo:</strong> R$ {p['custo_medio']:.4f}</p>
                    <p><strong>Status:</strong> {'Ativo' if p['ativo'] == 1 else 'Inativo'}</p>
                </div>
                """, unsafe_allow_html=True)

                # Ações
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("✏️ Editar", key=f"editar_{p['id']}"):
                        st.session_state['produto_id_editar'] = p['id']
                        st.switch_page("pages/interface_edicao.py")
                with col2:
                    st.link_button("➕ Novo Produto", url="/interface_cadastro")
                with col3:
                    novo_status = 0 if p["ativo"] == 1 else 1
                    botao_label = "Desativar" if p["ativo"] == 1 else "Ativar"
                    if st.button(botao_label, key=f"status_{p['id']}"):
                        atualizar_status(p['id'], novo_status)
                        st.experimental_rerun()

# Execução direta
if __name__ == "__main__":
    pass