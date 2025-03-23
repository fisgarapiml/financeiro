import streamlit as st
import sqlite3
import pandas as pd
import os
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header

# 🎯 Configuração da página
st.set_page_config(page_title="📤 Saídas de Estoque", layout="wide")

# 🎨 Paleta de Cores
AZUL_TURQUESA = "#40E0D0"
ROSA_VIBRANTE = "#FF69B4"
LARANJA = "#FFA500"

# 🌈 Estilo visual customizado
st.markdown(f"""
    <style>
        .main .block-container {{
            padding-top: 2rem;
        }}
        .css-1d391kg, .css-1v0mbdj, .st-bj {{
            background-color: #f9f9f9;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {ROSA_VIBRANTE};
        }}
    </style>
""", unsafe_allow_html=True)

# 🧾 Cabeçalho
st.markdown(f"""
    <h1 style='color: {ROSA_VIBRANTE}; font-size: 36px;'>📤 Saídas de Estoque</h1>
    <p style='font-size: 18px;'>Visualize aqui todas as movimentações de saída do seu estoque.</p>
""", unsafe_allow_html=True)

# 🔌 Caminho absoluto do banco de dados
def conectar():
    caminho_banco = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
    return sqlite3.connect(caminho_banco, check_same_thread=False)

# 🔎 Carregar dados de saídas
def carregar_saidas():
    query = '''
        SELECT m.id, m.data_movimentacao AS "Data",
               p.nome AS "Produto", m.quantidade AS "Quantidade",
               m.origem AS "Origem", m.observacoes AS "Observações"
        FROM movimentacoes_estoque m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.tipo = 'saida'
        ORDER BY m.data_movimentacao DESC
    '''
    with conectar() as conn:
        df = pd.read_sql_query(query, conn)
    return df

# 📊 Dados
df_saidas = carregar_saidas()

# 📈 Métricas
total_saidas = len(df_saidas)
total_quantidade = df_saidas["Quantidade"].sum()
produtos_unicos = df_saidas["Produto"].nunique()

st.markdown("""<div style='margin-top: 20px;'></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("📤 Total de Saídas", total_saidas)
col2.metric("📦 Itens Movimentados", total_quantidade)
col3.metric("🧸 Produtos Envolvidos", produtos_unicos)

style_metric_cards()

# 📋 Lista de saídas
st.markdown("---")
colored_header("📋 Lista de Saídas", description="Detalhamento completo das saídas de estoque", color_name="red-70")

st.dataframe(df_saidas, use_container_width=True, hide_index=True)

# ℹ️ Rodapé informativo
st.markdown("---")
st.info("Esses dados representam as movimentações de saída no estoque. Em breve será possível lançar manualmente e importar em lote.")
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
