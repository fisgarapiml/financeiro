import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="📦 Estoque - Início", layout="wide")

# 🎨 Paleta de cores
AZUL = "#40E0D0"
VERDE = "#32CD32"
AMARELO = "#FFD700"
ROSA = "#FF69B4"
ROXO = "#800080"
LARANJA = "#FFA500"

# Estilo visual customizado
st.markdown(f"""
    <style>
        .titulo-home {{
            font-size: 36px;
            font-weight: bold;
            color: {AZUL};
            margin-bottom: 20px;
        }}
        .subtitulo {{
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }}
        .botao-home button {{
            background-color: {VERDE} !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-size: 16px;
            font-weight: bold;
        }}
    </style>
""", unsafe_allow_html=True)

# 🧭 Menu lateral com links para páginas do módulo de estoque
st.sidebar.markdown("## 📦 Menu do Estoque")
st.sidebar.page_link("pages/interface_estoque_dashboard.py", label="🏠 Painel Principal")
st.sidebar.page_link("pages/interface_movimentacoes.py", label="🔄 Movimentações")
st.sidebar.page_link("pages/interface_estoque.py", label="📦 Controle de Estoque")
st.sidebar.page_link("pages/interface_listagem_edicao.py", label="🛠 Edição em Massa")
st.sidebar.page_link("pages/interface_estoque_entradas.py", label="📥 Entradas")
st.sidebar.page_link("pages/interface_estoque_saidas.py", label="📤 Saídas")

# ✅ Título e mensagem de boas-vindas
st.markdown("<div class='titulo-home'>📦 Bem-vindo ao Módulo de Estoque</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Gerencie de forma moderna e visual seus produtos, entradas, saídas e ajustes de estoque.</div>", unsafe_allow_html=True)

# 🔘 Atalhos principais
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='botao-home'>", unsafe_allow_html=True)
    st.link_button("📊 Abrir Painel Principal", url="/interface_estoque_dashboard")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='botao-home'>", unsafe_allow_html=True)
    st.link_button("📥 Entrada de Produtos", url="/interface_estoque_entradas")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='botao-home'>", unsafe_allow_html=True)
    st.link_button("📤 Saída de Produtos", url="/interface_estoque_saidas")
    st.markdown("</div>", unsafe_allow_html=True)

# 📝 Dica adicional
st.markdown("### ℹ️ Use o menu lateral para acessar qualquer funcionalidade do módulo de estoque.")
