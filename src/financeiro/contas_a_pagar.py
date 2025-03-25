import streamlit as st
import sqlite3
from datetime import datetime

# Conexão com o banco
conn = sqlite3.connect("grupo_fisgar.db")
cursor = conn.cursor()

st.set_page_config(page_title="Financeiro - Contas a Pagar", layout="wide")

# ======================
# CONFIGURAÇÕES
# ======================
mes_atual = datetime.now().month
ano_atual = datetime.now().year
meses_portugues = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# ======================
# FORMATADOR
# ======================
def formatar_valor(valor):
    try:
        valor = float(valor)
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

# ======================
# ESTILO VISUAL
# ======================
st.markdown("""
    <style>
        .cabecalho {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            margin-top: -20px;
        }
        .cabecalho h1 {
            font-size: 34px;
            font-weight: 800;
            color: #25C2A0;
            margin: 0;
            padding: 0;
            line-height: 1.1;
        }
        .card {
            background-color: #ffffff;
            padding: 1.3em;
            border-radius: 20px;
            box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: scale(1.01);
            box-shadow: 1px 1px 15px rgba(0,0,0,0.15);
        }
        .titulo {
            font-size: 18px;
            color: #555555;
            margin-bottom: 0.3em;
        }
        .valor {
            font-size: 24px;
            font-weight: bold;
            color: #111111;
        }
    </style>
""", unsafe_allow_html=True)

# ======================
# CABEÇALHO
# ======================
col1, col2 = st.columns([6, 2])
with col1:
    st.markdown('<h1 class="cabecalho">💼 Financeiro - Contas a Pagar</h1>', unsafe_allow_html=True)

with col2:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_mes_nome = st.selectbox("Mês", meses_portugues, index=mes_atual - 1)
        filtro_mes_num = f"{meses_portugues.index(filtro_mes_nome) + 1:02d}"
    with col_f2:
        filtro_ano = st.selectbox("Ano", list(range(ano_atual - 3, ano_atual + 3)), index=3)

filtro_mes_ano = f"{filtro_mes_num}/{filtro_ano}"

# ======================
# FUNÇÕES RESUMO
# ======================
def get_valores_financeiros(mes_ano):
    cursor.execute("""
        SELECT 
            SUM(CAST(valor AS REAL)),
            SUM(CAST(valor_pago AS REAL)),
            SUM(CAST(valor_pendente AS REAL))
        FROM contas_a_pagar
        WHERE vencimento LIKE ?
    """, (f"%/{mes_ano}",))
    v_total, v_pago, v_pendente = cursor.fetchone()
    v_total = v_total or 0
    v_pago = v_pago or 0
    v_pendente = v_pendente or 0
    saldo = v_pago - abs(v_total)
    return v_total, v_pago, v_pendente, saldo

# ======================
# RESUMO EM CARDS
# ======================
valor_previsto, valor_pago, valor_restante, saldo_atual = get_valores_financeiros(filtro_mes_ano)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="card" style="border-top: 5px solid #25C2A0;">
            <div class="titulo">💰 Total do Mês</div>
            <div class="valor">{formatar_valor(abs(valor_previsto))}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card" style="border-top: 5px solid #43a047;">
            <div class="titulo">✅ Total Pago</div>
            <div class="valor">{formatar_valor(valor_pago)}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card" style="border-top: 5px solid #f4511e;">
            <div class="titulo">🔄 Ainda a Pagar</div>
            <div class="valor">{formatar_valor(valor_restante)}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="card" style="border-top: 5px solid #1e88e5;">
            <div class="titulo">📉 Saldo Real</div>
            <div class="valor">{formatar_valor(saldo_atual)}</div>
        </div>
    """, unsafe_allow_html=True)

# ======================
# LISTAGEM ESTILIZADA + FILTRO
# ======================
st.markdown("### 🎯 Filtros de Lançamentos (opcional)")
with st.expander("🔍 Aplicar Filtros Avançados", expanded=False):
    colf1, colf2, colf3, colf4 = st.columns(4)
    with colf1:
        filtro_status = st.multiselect("Status", options=["Pago", "Aberto", "Vencido"])
    with colf2:
        fornecedores_unicos = [row[0] for row in cursor.execute("SELECT DISTINCT fornecedor FROM contas_a_pagar")]
        filtro_fornecedor = st.multiselect("Fornecedor", options=fornecedores_unicos)
    with colf3:
        categorias_unicas = [row[0] for row in cursor.execute("SELECT DISTINCT categorias FROM contas_a_pagar")]
        filtro_categoria = st.multiselect("Categoria", options=categorias_unicas)
    with colf4:
        tipos_custo = [row[0] for row in cursor.execute("SELECT DISTINCT tipo_custo FROM contas_a_pagar")]
        filtro_tipo = st.multiselect("Tipo de Custo", options=tipos_custo)

    aplicar = st.button("🔎 Aplicar Filtros")

# Consulta lançamentos
cursor.execute("""
    SELECT vencimento, fornecedor, valor, valor_pago, valor_pendente, status, categorias, tipo_custo 
    FROM contas_a_pagar
    WHERE vencimento LIKE ?
    ORDER BY vencimento
""", (f"%/{filtro_mes_ano}",))
dados = cursor.fetchall()

lancamentos = []
for row in dados:
    vencimento, fornecedor, valor, valor_pago, valor_pendente, status, cat, tipo = row
    try:
        valor_float = float(str(valor).replace(",", "."))
        valor_pago_float = float(str(valor_pago).replace(",", "."))
        valor_pendente_float = float(str(valor_pendente).replace(",", "."))
    except:
        valor_float = valor_pago_float = valor_pendente_float = 0
    lancamentos.append({
        "vencimento": vencimento,
        "fornecedor": fornecedor,
        "valor": valor_float,
        "valor_pago": valor_pago_float,
        "valor_pendente": valor_pendente_float,
        "status": status,
        "categoria": cat,
        "tipo": tipo
    })

if aplicar:
    if filtro_status:
        lancamentos = [l for l in lancamentos if l["status"] in filtro_status]
    if filtro_fornecedor:
        lancamentos = [l for l in lancamentos if l["fornecedor"] in filtro_fornecedor]
    if filtro_categoria:
        lancamentos = [l for l in lancamentos if l["categoria"] in filtro_categoria]
    if filtro_tipo:
        lancamentos = [l for l in lancamentos if l["tipo"] in filtro_tipo]

    total_filtrado = sum(l["valor"] for l in lancamentos)

    st.markdown(f"""
        <div style="background-color:#E3FCEF;padding:1rem;border-radius:10px;margin-bottom:20px;">
            <strong>🔢 Total dos lançamentos filtrados:</strong> {formatar_valor(total_filtrado)}
        </div>
    """, unsafe_allow_html=True)

    if not lancamentos:
        st.warning("Nenhum lançamento encontrado com os filtros selecionados.")
else:
    st.markdown("### 📋 Lançamentos do Mês (sem filtro aplicado)")

# Listagem visual moderna
for l in lancamentos:
    st.markdown(f"""
        <div style="border:1px solid #eee;border-left:5px solid #25C2A0;border-radius:10px;padding:15px;margin-bottom:12px;box-shadow:1px 1px 4px rgba(0,0,0,0.04);">
            <div style="font-size:18px;font-weight:600;color:#25C2A0;">🗓️ {l['vencimento']} — {l['fornecedor']}</div>
            <div style="margin-top:4px;font-size:15px;color:#333;">
                💰 Valor: <strong>{formatar_valor(l['valor'])}</strong> |
                ✅ Pago: <strong>{formatar_valor(l['valor_pago'])}</strong> |
                ⏳ Pendente: <strong>{formatar_valor(l['valor_pendente'])}</strong> |
                📌 Status: <strong>{l['status']}</strong> |
                📂 Categoria: <strong>{l['categoria']}</strong> |
                🧾 Tipo de Custo: <strong>{l['tipo']}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# BOTÃO FINAL
st.markdown("## ")
if st.button("➕ Nova Conta"):
    st.info("A tela de cadastro ainda será implementada.")

conn.close()
