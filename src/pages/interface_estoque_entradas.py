import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page

# 🎯 Configuração da página
st.set_page_config(page_title="📥 Entradas de Estoque", layout="wide")

# 🎨 Paleta de Cores
AZUL_TURQUESA = "#40E0D0"
AMARELO_ALEGRE = "#FFD700"
ROSA_VIBRANTE = "#FF69B4"
VERDE_LIMAO = "#32CD32"
LARANJA = "#FFA500"
ROXO = "#800080"

# 🎨 Estilo personalizado
st.markdown(f"""
    <style>
        .main .block-container {{
            padding-top: 2rem;
        }}
        .css-1d391kg, .css-1v0mbdj, .st-bj {{
            background-color: #f9f9f9;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {AZUL_TURQUESA};
        }}
        .botao-acao {{
            background-color: {LARANJA};
            color: white;
            padding: 0.6em 1em;
            border-radius: 8px;
            text-align: center;
            margin: 5px;
            display: inline-block;
            font-weight: bold;
            font-size: 16px;
        }}
        .botao-acao:hover {{
            background-color: #e67e22;
        }}
    </style>
""", unsafe_allow_html=True)

# 🧾 Cabeçalho
st.markdown(f"""
    <h1 style='color: {AZUL_TURQUESA}; font-size: 36px;'>📥 Entradas de Estoque</h1>
    <p style='font-size: 18px;'>Veja abaixo os lançamentos de entrada de produtos no estoque com visual moderno e agradável.</p>
""", unsafe_allow_html=True)

# 🚀 Botões de acesso rápido
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("📤 Acessar Saídas de Estoque"):
        switch_page("interface_estoque_saidas")

with col_btn2:
    if st.button("📦 Voltar ao Controle de Estoque"):
        switch_page("interface_estoque")

# 🔌 Função de conexão com o banco (sem cache para evitar erro de threads)
def conectar():
    caminho_banco = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
    return sqlite3.connect(caminho_banco, check_same_thread=False)

# 🔍 Função para carregar entradas
def carregar_entradas():
    query = '''
        SELECT m.id, m.data_movimentacao AS "Data",
               p.nome AS "Produto", m.quantidade AS "Quantidade",
               m.origem AS "Origem", m.observacoes AS "Observações"
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.tipo = 'entrada'
        ORDER BY m.data_movimentacao DESC
    '''
    with conectar() as conn:
        df = pd.read_sql_query(query, conn)
    return df

# 📊 Carregar dados
df_entradas = carregar_entradas()

# 📈 Métricas
total_entradas = len(df_entradas)
total_quantidade = df_entradas["Quantidade"].sum()
produtos_unicos = df_entradas["Produto"].nunique()

st.markdown("""<div style='margin-top: 20px;'></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total de Entradas", total_entradas)
col2.metric("📦 Itens Movimentados", total_quantidade)
col3.metric("🧸 Produtos Envolvidos", produtos_unicos)

style_metric_cards()

# 📋 Lista visual
st.markdown("---")
colored_header("🧾 Lista de Entradas", description="Detalhes de cada entrada registrada", color_name="blue-70")

st.dataframe(df_entradas, use_container_width=True, hide_index=True)

# ℹ️ Rodapé
st.markdown("---")
st.info("Esses dados representam as movimentações de entrada no estoque. Em breve será possível lançar manualmente e importar em lote.")
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
