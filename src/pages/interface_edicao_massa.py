import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="🛠 Edição em Massa", layout="wide")
st.title("🛠 Edição em Massa de Produtos")

# Conectar ao banco de dados
def conectar():
    caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
    return sqlite3.connect(caminho, check_same_thread=False)

# Carregar produtos do banco
@st.cache_data(ttl=60)
def carregar_produtos():
    with conectar() as conn:
        df = pd.read_sql_query('''
            SELECT id, nome, preco_venda, custo_medio, estoque_minimo, estoque_maximo, ativo
            FROM produtos
            ORDER BY nome
        ''', conn)
    return df

# Atualizar os produtos editados
def atualizar_produtos(df_editado):
    with conectar() as conn:
        cursor = conn.cursor()
        for _, row in df_editado.iterrows():
            cursor.execute('''
                UPDATE produtos SET
                    nome = ?, preco_venda = ?, custo_medio = ?,
                    estoque_minimo = ?, estoque_maximo = ?, ativo = ?
                WHERE id = ?
            ''', (
                row["nome"], row["preco_venda"], row["custo_medio"],
                row["estoque_minimo"], row["estoque_maximo"], int(row["ativo"]), row["id"]
            ))
        conn.commit()

# 🔍 Buscar produtos e exibir tabela editável
df = carregar_produtos()
st.caption("Edite diretamente os campos abaixo e clique em **Salvar Alterações** para atualizar o banco de dados.")

# Convertendo o campo 'ativo' para booleano (caso venha como inteiro)
df["ativo"] = df["ativo"].astype(bool)

# Área de edição
df_editado = st.data_editor(
    df,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "nome": st.column_config.TextColumn(label="🧸 Nome do Produto"),
        "preco_venda": st.column_config.NumberColumn(label="💰 Preço de Venda", format="R$ %.2f"),
        "custo_medio": st.column_config.NumberColumn(label="📊 Custo Médio", format="R$ %.4f"),
        "estoque_minimo": st.column_config.NumberColumn(label="📦 Estoque Mínimo"),
        "estoque_maximo": st.column_config.NumberColumn(label="📦 Estoque Máximo"),
        "ativo": st.column_config.CheckboxColumn(label="✔️ Ativo")
    },
    disabled=["id"],
    key="editor_produtos"
)

# Botão para salvar alterações
st.markdown("---")
if st.button("💾 Salvar Alterações em Massa"):
    atualizar_produtos(df_editado)
    st.success("✅ Alterações salvas com sucesso!")
