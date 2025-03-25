import streamlit as st
import sqlite3
from datetime import datetime

# Conectar ao banco
conn = sqlite3.connect("../src/grupo_fisgar.db")
cursor = conn.cursor()

# Funções de cálculo
def get_total_mes():
    cursor.execute("""
        SELECT SUM(valor) FROM contas_a_pagar
        WHERE strftime('%m-%Y', vencimento) = strftime('%m-%Y', 'now')
    """)
    resultado = cursor.fetchone()[0]
    return resultado or 0

def get_vencidas():
    cursor.execute("""
        SELECT COUNT(*), SUM(valor_pendente) FROM contas_a_pagar
        WHERE status = 'Vencido'
    """)
    qtd, total = cursor.fetchone()
    return qtd, total or 0

def get_a_vencer():
    hoje = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(f"""
        SELECT COUNT(*), SUM(valor_pendente) FROM contas_a_pagar
        WHERE status != 'Vencido' AND vencimento > '{hoje}'
    """)
    qtd, total = cursor.fetchone()
    return qtd, total or 0

def get_total_pendente():
    cursor.execute("SELECT SUM(valor_pendente) FROM contas_a_pagar")
    total = cursor.fetchone()[0]
    return total or 0

# Layout
st.set_page_config(page_title="Contas a Pagar", layout="wide")
st.title("💼 Contas a Pagar - Grupo Fisgar")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 💰 Contas do Mês")
    st.metric(label="Total", value=f"R$ {get_total_mes():,.2f}")

with col2:
    vencidas_qtd, vencidas_valor = get_vencidas()
    st.markdown("### ⏰ Vencidas")
    st.metric(label=f"{vencidas_qtd} contas", value=f"R$ {vencidas_valor:,.2f}")

with col3:
    a_vencer_qtd, a_vencer_valor = get_a_vencer()
    st.markdown("### 📅 A Vencer")
    st.metric(label=f"{a_vencer_qtd} contas", value=f"R$ {a_vencer_valor:,.2f}")

with col4:
    st.markdown("### 💸 Total Pendente")
    st.metric(label="Em aberto", value=f"R$ {get_total_pendente():,.2f}")

st.markdown("---")

# Botão estilizado
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #25C2A0;
        color: white;
        padding: 0.75em 2em;
        font-size: 16px;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 1px 1px 5px #888;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1AA187;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("➕ Nova Conta"):
    st.info("Tela de cadastro de nova conta em desenvolvimento.")

conn.close()
