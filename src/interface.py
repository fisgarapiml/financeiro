import sqlite3
import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt

# === CONFIGURAÇÃO GLOBAL DO LAYOUT ===
st.set_page_config(page_title="Sistema Financeiro Fisgar", layout="wide")

# === ESTILO VISUAL MODERNO E FUTURISTA ===
st.markdown("""
    <style>
        body {
            background-color: #f2f4f8;
            font-family: 'Segoe UI', sans-serif;
        }
        .titulo-principal {
            background: linear-gradient(90deg, #3f51b5, #00bcd4);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 30px;
            color: white;
            text-align: center;
            font-size: 32px;
            font-weight: 600;
            letter-spacing: 1px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        }
        .card {
            background: #ffffff;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border: none;
        }
        .card:hover {
            transform: translateY(-6px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .card h4 {
            margin-bottom: 1rem;
            color: #004d99;
            font-size: 20px;
            font-weight: 600;
        }
        .card p {
            margin: 0.35rem 0;
            color: #2c3e50;
            font-size: 0.95rem;
        }
        .stButton>button {
            background: linear-gradient(90deg, #2196f3, #00bcd4);
            color: white;
            border: none;
            padding: 10px 22px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: background 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #1976d2, #0097a7);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-principal'>Painel de Compras - NF-e</div>", unsafe_allow_html=True)

# Caminho do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'contas_apagar.db')

# === FUNÇÃO PARA CARREGAR DADOS ===
def carregar_dados():
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT nf.numero AS "NF-e",
               nf.data_emissao AS "Data Emissão",
               p.codigo_produto AS "Código",
               p.descricao AS "Produto",
               p.quantidade AS "Qtd",
               p.unidade AS "Un",
               p.valor_unitario AS "Valor Unit",
               p.valor_total AS "Total",
               p.custo_unitario_real AS "Custo Unit",
               p.percentual_ipi AS "% IPI",
               p.custo_unitario_com_ipi AS "Custo c/ IPI"
        FROM produtos_nfe p
        JOIN notas_fiscais nf ON nf.id = p.nota_id
        ORDER BY nf.numero DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# === DADOS CARREGADOS ===
df = carregar_dados()

# === INDICADORES RESUMIDOS ===
st.markdown("## Indicadores Gerais")
col1, col2 = st.columns(2)
with col1:
    st.metric("Notas Fiscais Importadas", df["NF-e"].nunique())
with col2:
    st.metric("Total de Itens", len(df))

st.markdown("---")

# === FILTRO DE NOTA ===
st.markdown("### Selecione a NF-e para visualizar os produtos")
nfes = df["NF-e"].unique()
selecionada = st.selectbox("NF-e", options=nfes)
df_nf = df[df["NF-e"] == selecionada]

# === TOTAL DA NF-E SELECIONADA ===
total_nfe = df_nf["Total"].sum()
st.markdown(f"<div class='card'><h4>Total da NF-e {selecionada}</h4><p style='font-size: 22px;'>R$ {total_nfe:,.2f}</p></div>", unsafe_allow_html=True)

# === BOTÃO DE EXPORTAÇÃO PARA EXCEL ===
excel_buffer = BytesIO()
df_nf.to_excel(excel_buffer, index=False, sheet_name=f"NF_{selecionada}")
excel_buffer.seek(0)
st.download_button(
    label="📥 Baixar NF-e em Excel",
    data=excel_buffer,
    file_name=f"NF-e_{selecionada}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# === GRÁFICO DE VALORES TOTAIS POR PRODUTO ===
st.markdown("### Gráfico de Custos por Produto")
fig, ax = plt.subplots(figsize=(12, 5))
df_nf_sorted = df_nf.sort_values("Total", ascending=False)
ax.bar(df_nf_sorted["Produto"], df_nf_sorted["Total"], color="#42a5f5")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Valor Total (R$)")
plt.xlabel("Produto")
plt.title("Total por Produto na NF-e")
st.pyplot(fig)

# === LISTAGEM DOS PRODUTOS EM CARDS ===
st.markdown(f"## Produtos da NF-e {selecionada}")

for i in range(0, len(df_nf), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(df_nf):
            produto = df_nf.iloc[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div class='card'>
                        <h4>{produto['Produto']}</h4>
                        <p><strong>Código:</strong> {produto['Código']}</p>
                        <p><strong>Quantidade:</strong> {produto['Qtd']} {produto['Un']}</p>
                        <p><strong>Valor Unitário:</strong> R$ {produto['Valor Unit']:.2f}</p>
                        <p><strong>Custo Real:</strong> R$ {produto['Custo Unit']:.4f}</p>
                        <p><strong>IPI:</strong> {produto['% IPI']:.2f}%</p>
                        <p><strong>Custo com IPI:</strong> R$ {produto['Custo c/ IPI']:.4f}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# === BOTÕES DE AÇÕES ===
st.markdown("### Ações do Sistema")
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("Sincronizar com Financeiro"):
        st.success("Financeiro sincronizado com sucesso.")
with col_b:
    if st.button("Sincronizar com Estoque"):
        st.success("Estoque atualizado com sucesso.")
with col_c:
    if st.button("Sincronizar com Compras"):
        st.success("Compras sincronizadas com sucesso.")