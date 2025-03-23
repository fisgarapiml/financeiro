import streamlit as st
import sqlite3
import pandas as pd
import os
from PIL import Image

# Configuração da página
st.set_page_config(page_title="📈 Painel de Estoque", layout="wide")

# 🎨 Paleta de cores
AZUL = "#40E0D0"
VERDE = "#32CD32"
AMARELO = "#FFD700"
ROSA = "#FF69B4"
ROXO = "#800080"
LARANJA = "#FFA500"

# 🔍 Menu lateral funcional (usando caminho relativo à pasta 'pages/')
st.sidebar.markdown("## 📦 Menu de Estoque")
st.sidebar.page_link("pages/interface_movimentacoes.py", label="🔄 Movimentações")
st.sidebar.page_link("pages/interface_estoque.py", label="📦 Controle de Estoque")
st.sidebar.page_link("pages/interface_listagem_edicao.py", label="🛠 Edição em Massa")
st.sidebar.page_link("pages/interface_estoque_entradas.py", label="📥 Entradas")
st.sidebar.page_link("pages/interface_estoque_saidas.py", label="📤 Saídas")

# Estilo visual customizado
st.markdown(f"""
    <style>
        .titulo-principal {{
            font-size: 36px;
            font-weight: bold;
            color: {AZUL};
            margin-bottom: 10px;
        }}
        .card {{
            background-color: #fff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .card h3 {{
            margin-bottom: 10px;
            font-size: 20px;
        }}
        .card p {{
            font-size: 28px;
            font-weight: bold;
        }}
        .botao-acao button {{
            background-color: {LARANJA} !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 16px;
        }}
    </style>
""", unsafe_allow_html=True)

# 🔐 Conexão com o banco
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📊 Dados principais
produtos = pd.read_sql_query("SELECT * FROM produtos", conn)
estoque = pd.read_sql_query("SELECT * FROM estoque", conn)

# 📊 Indicadores
produtos_baixo = produtos.merge(estoque, left_on="id", right_on="produto_id")
produtos_baixo = produtos_baixo[produtos_baixo["estoque_atual"] < produtos_baixo["estoque_minimo"]]

total_estoque = estoque["estoque_atual"].sum()
custo_total = (produtos.merge(estoque, left_on="id", right_on="produto_id")
                        .assign(total=lambda df: df["estoque_atual"] * df["custo_medio"])
                        ["total"].sum())
produtos_inativos = produtos[produtos["ativo"] == 0].shape[0]

# 📈 Cabeçalho principal
st.markdown("<div class='titulo-principal'>🏦 Painel Principal de Estoque</div>", unsafe_allow_html=True)

# 🗕 Cards com indicadores
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='card'><h3 style='color:{AMARELO}'>Produtos com Estoque Baixo</h3><p>{len(produtos_baixo)}</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><h3 style='color:{ROSA}'>Qtd. Total em Estoque</h3><p>{int(total_estoque)}</p></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><h3 style='color:{VERDE}'>Custo Total</h3><p>R$ {custo_total:,.2f}</p></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='card'><h3 style='color:{ROXO}'>Produtos Inativos</h3><p>{produtos_inativos}</p></div>", unsafe_allow_html=True)

# 🔧 Botões de ação
st.markdown("## ")
b1, b2, b3 = st.columns(3)
with b1:
    st.markdown("<div class='botao-acao'>", unsafe_allow_html=True)
    st.link_button("🔄 Ver Movimentações", url="/interface_movimentacoes")
    st.markdown("</div>", unsafe_allow_html=True)

with b2:
    st.markdown("<div class='botao-acao'>", unsafe_allow_html=True)
    st.link_button("➕ Cadastrar Produto", url="/interface_cadastro")
    st.markdown("</div>", unsafe_allow_html=True)

with b3:
    st.markdown("<div class='botao-acao'>", unsafe_allow_html=True)
    st.link_button("🚰 Ajustar Estoque", url="/interface_listagem_edicao")
    st.markdown("</div>", unsafe_allow_html=True)

# 📌 Execução:
# streamlit run src/interface_estoque_dashboard.py
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
