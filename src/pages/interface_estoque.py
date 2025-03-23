import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="📦 Painel de Estoque", layout="wide")
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
        }
        .css-1d391kg, .css-1v0mbdj, .st-bj {
            background-color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# 🎨 Paleta de Cores
AZUL_TURQUESA = "#40E0D0"
AMARELO_ALEGRE = "#FFD700"
ROSA_VIBRANTE = "#FF69B4"
VERDE_LIMAO = "#32CD32"
LARANJA = "#FFA500"
ROXO = "#800080"

# 📊 Cabeçalho Visual
st.markdown(f"""
    <h1 style='color: {AZUL_TURQUESA}; font-size: 36px;'>📦 Controle de Estoque</h1>
    <p style='font-size: 18px;'>Acompanhe a saúde do estoque com informações visuais e rápidas.</p>
""", unsafe_allow_html=True)

# 🔗 Conexão com banco de dados
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
def conectar():
    return sqlite3.connect(db_path)

# 🔎 Consultar dados do estoque
def consultar_estoque():
    conn = conectar()
    query = '''
        SELECT p.id, p.nome, p.estoque_minimo, p.estoque_maximo,
               COALESCE(e.estoque_atual, 0) as estoque_atual,
               p.preco_venda
        FROM produtos p
        LEFT JOIN estoque e ON p.id = e.produto_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 🔢 Indicadores
df = consultar_estoque()
total_produtos = len(df)
estoque_zerado = df[df["estoque_atual"] == 0].shape[0]
estoque_baixo = df[df["estoque_atual"] < df["estoque_minimo"]].shape[0]
custo_total = (df["estoque_atual"] * df["preco_venda"]).sum()

# 📊 Métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧸 Produtos com Estoque Baixo", estoque_baixo)
col2.metric("❌ Produtos Zerados", estoque_zerado)
col3.metric("📦 Produtos no Estoque", total_produtos)
col4.metric("💰 Custo Total Estocado", f"R$ {custo_total:,.2f}".replace(",", "."))

style_metric_cards()

st.markdown("---")
colored_header("🔗 Acessos Rápidos", description="Gerencie as operações do módulo de estoque", color_name="violet-70")

col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("📥 Entradas de Estoque", use_container_width=True):
        switch_page("interface_estoque_entradas")
with col_b:
    if st.button("📤 Saídas de Estoque", use_container_width=True):
        switch_page("interface_estoque_saidas")
with col_c:
    if st.button("📋 Inventário de Estoque", use_container_width=True):
        switch_page("interface_estoque_inventario")

st.markdown("---")
st.info("Essa é a tela principal do módulo de estoque. Em breve, mais relatórios visuais e insights serão adicionados!")
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
