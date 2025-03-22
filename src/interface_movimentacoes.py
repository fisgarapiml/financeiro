import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="🔄 Movimentações de Estoque", layout="wide")
st.title("🔄 Histórico de Movimentações de Estoque")

# Caminho do banco
db_path = os.path.join(os.path.dirname(__file__), "contas_apagar.db")

# Conexão com banco de dados
def conectar():
    return sqlite3.connect(db_path)

# Carregar movimentações
def carregar_movimentacoes():
    conn = conectar()
    query = '''
        SELECT m.id, m.data_movimentacao AS "Data",
               p.nome AS "Produto", p.codigo AS "Código",
               m.tipo AS "Tipo", m.quantidade AS "Quantidade",
               m.origem AS "Origem", m.observacoes AS "Observações"
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data_movimentacao DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Filtros laterais
st.sidebar.header("🔍 Filtros")

movimentacoes = carregar_movimentacoes()

# Filtro por tipo
tipos = movimentacoes["Tipo"].unique().tolist()
tipo_filtro = st.sidebar.multiselect("Tipo de Movimentação", tipos, default=tipos)

# Filtro por produto
produtos = movimentacoes["Produto"].unique().tolist()
produto_filtro = st.sidebar.multiselect("Produto", produtos, default=produtos)

# Filtro por data
data_inicio = st.sidebar.date_input("Data inicial", value=pd.to_datetime("2024-01-01"))
data_fim = st.sidebar.date_input("Data final", value=pd.to_datetime("today"))

# Aplicar filtros
filtro = (
    (movimentacoes["Tipo"].isin(tipo_filtro)) &
    (movimentacoes["Produto"].isin(produto_filtro)) &
    (pd.to_datetime(movimentacoes["Data"]) >= pd.to_datetime(data_inicio)) &
    (pd.to_datetime(movimentacoes["Data"]) <= pd.to_datetime(data_fim))
)

movimentacoes_filtradas = movimentacoes[filtro]

st.markdown(f"### Movimentações Encontradas: {len(movimentacoes_filtradas)}")
st.dataframe(movimentacoes_filtradas, use_container_width=True)

# Total por tipo
totais = movimentacoes_filtradas.groupby("Tipo")["Quantidade"].sum().reset_index()

st.markdown("---")
st.subheader("📊 Totais por Tipo de Movimentação")
col1, col2 = st.columns(2)

with col1:
    for _, row in totais.iterrows():
        st.metric(label=row["Tipo"], value=int(row["Quantidade"]))

with col2:
    st.markdown("""
    **Tipos comuns:**
    - Entrada (Compra, Ajuste, Transferência)
    - Saída (Venda, Perda, Ajuste)
    - Inventário
    """)

st.markdown("---")
with st.expander("📌 Próximas funcionalidades"):
    st.markdown("""
    - Lançamento manual de movimentações
    - Importação por planilhas ou integrações
    - Visualização em gráficos
    - Relatórios avançados por período
    """)
