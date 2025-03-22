import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📦 Controle de Estoque", layout="wide")
st.title("📦 Painel de Estoque")

# Caminho do banco
db_path = os.path.join(os.path.dirname(__file__), "contas_apagar.db")

# Conexão com banco de dados
def conectar():
    return sqlite3.connect(db_path)

# Criar tabelas se não existirem
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de estoque
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            estoque_atual REAL,
            data_atualizacao TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    ''')

    # Tabela de movimentações de estoque
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            tipo TEXT,
            quantidade REAL,
            data_movimentacao TEXT,
            origem TEXT,
            observacoes TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    ''')

    conn.commit()
    conn.close()

# Carregar dados combinados de produtos + estoque
def carregar_estoque():
    conn = conectar()
    query = '''
        SELECT p.id, p.nome, p.codigo, p.estoque_minimo, p.estoque_maximo, 
               COALESCE(e.estoque_atual, 0) as estoque_atual, p.ativo
        FROM produtos p
        LEFT JOIN estoque e ON p.id = e.produto_id
        ORDER BY p.nome ASC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    def classificar(linha):
        estoque_atual = linha.get("estoque_atual", 0)
        estoque_minimo = linha.get("estoque_minimo")
        estoque_maximo = linha.get("estoque_maximo")

        if linha["ativo"] == 0:
            return "Inativo"
        if estoque_atual == 0:
            return "Zerado"
        if pd.notna(estoque_minimo) and estoque_atual < estoque_minimo:
            return "Baixo"
        if pd.notna(estoque_maximo) and estoque_atual > estoque_maximo:
            return "Excedente"
        if pd.isna(estoque_minimo) and pd.isna(estoque_maximo):
            return "Sem info"
        return "OK"

    df["status_estoque"] = df.apply(classificar, axis=1)
    return df

# Inicializa tabelas
criar_tabelas()

# Carrega dados
df = carregar_estoque()

# Filtros
st.sidebar.header("🔍 Filtros")
status_options = df["status_estoque"].unique().tolist()
status_filtro = st.sidebar.multiselect("Status de Estoque", status_options, default=status_options)
mostrar_inativos = st.sidebar.checkbox("Mostrar produtos inativos", value=False)

# Aplicar filtros
df_filtrado = df[df["status_estoque"].isin(status_filtro)]
if not mostrar_inativos:
    df_filtrado = df_filtrado[df_filtrado["ativo"] == 1]

# Exibir
df_filtrado = df_filtrado.reset_index(drop=True)
st.markdown(f"### Produtos em Estoque: {len(df_filtrado)}")
st.dataframe(df_filtrado, use_container_width=True)

# Métricas
total_itens = df_filtrado["estoque_atual"].sum()
baixo = (df_filtrado["status_estoque"] == "Baixo").sum()
zerado = (df_filtrado["status_estoque"] == "Zerado").sum()
excedente = (df_filtrado["status_estoque"] == "Excedente").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔢 Total em Estoque", f"{total_itens:.0f}")
col2.metric("📉 Baixo", baixo)
col3.metric("🛑 Zerado", zerado)
col4.metric("📦 Excedente", excedente)

st.markdown("---")

with st.expander("📌 Próximas funcionalidades"):
    st.markdown("""
    - Inventário geral e por produto
    - Análise de giro de estoque e produtos parados
    - Histórico de movimentações (entradas e saídas)
    - Ajuste manual e por importação
    - Integração com compras e vendas em tempo real
    """)
