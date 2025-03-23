import streamlit as st
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="🔄 Movimentações de Estoque", layout="wide")
st.title("🔄 Histórico de Movimentações de Estoque")

# 📦 Caminho correto do banco
db_path = os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db")

# Conexão com banco
def conectar():
    return sqlite3.connect(db_path)

# Carregar movimentações
def carregar_movimentacoes():
    conn = conectar()
    query = '''
        SELECT m.id, 
               m.data_movimentacao AS "Data", 
               p.nome AS "Produto", 
               p.codigo AS "Código",
               m.tipo AS "Tipo", 
               m.quantidade AS "Quantidade", 
               m.origem AS "Origem", 
               m.observacoes AS "Observações"
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        ORDER BY m.data_movimentacao DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Filtros laterais
st.sidebar.header("🔍 Filtros")

try:
    movimentacoes = carregar_movimentacoes()

    if movimentacoes.empty:
        st.warning("Nenhuma movimentação encontrada no sistema.")
    else:
        # Corrigir o parsing de data
        movimentacoes["Data"] = pd.to_datetime(movimentacoes["Data"], format='mixed', dayfirst=True)

        # Filtros
        tipos = movimentacoes["Tipo"].dropna().unique().tolist()
        tipo_filtro = st.sidebar.multiselect("Tipo de Movimentação", tipos, default=tipos)

        produtos = movimentacoes["Produto"].dropna().unique().tolist()
        produto_filtro = st.sidebar.multiselect("Produto", produtos, default=produtos)

        data_inicio = st.sidebar.date_input("Data inicial", value=movimentacoes["Data"].min().date())
        data_fim = st.sidebar.date_input("Data final", value=movimentacoes["Data"].max().date())

        # Aplicar filtros
        filtro = (
            movimentacoes["Tipo"].isin(tipo_filtro) &
            movimentacoes["Produto"].isin(produto_filtro) &
            (movimentacoes["Data"] >= pd.to_datetime(data_inicio)) &
            (movimentacoes["Data"] <= pd.to_datetime(data_fim))
        )

        movimentacoes_filtradas = movimentacoes[filtro]

        st.markdown(f"### 📋 Movimentações Encontradas: {len(movimentacoes_filtradas)}")
        st.dataframe(movimentacoes_filtradas, use_container_width=True)

        # Totais por tipo
        totais = movimentacoes_filtradas.groupby("Tipo")["Quantidade"].sum().reset_index()

        st.markdown("---")
        st.subheader("📊 Totais por Tipo de Movimentação")
        col1, col2 = st.columns(2)

        with col1:
            if not totais.empty:
                for _, row in totais.iterrows():
                    st.metric(label=row["Tipo"], value=int(row["Quantidade"]))
            else:
                st.info("Nenhuma movimentação para os filtros aplicados.")

        with col2:
            if not totais.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(totais["Tipo"], totais["Quantidade"], color="#4a90e2")
                ax.set_ylabel("Quantidade")
                ax.set_xlabel("Tipo")
                ax.set_title("Distribuição das Movimentações")
                st.pyplot(fig)

        # Resumo por produto
        st.markdown("---")
        st.subheader("📦 Total Movimentado por Produto")
        total_produto = movimentacoes_filtradas.groupby("Produto")["Quantidade"].sum().reset_index().sort_values(by="Quantidade", ascending=False)
        st.dataframe(total_produto, use_container_width=True)

except Exception as e:
    st.error(f"❌ Erro ao carregar movimentações: {e}")

# 📌 Execução:
# streamlit run src/interface_estoque_dashboard.py
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
