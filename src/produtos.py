import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="🧸 Produtos Cadastrados", layout="wide")

# 🎨 Paleta de Cores
AZUL = "#40E0D0"
VERDE = "#32CD32"
AMARELO = "#FFD700"
ROSA = "#FF69B4"
LARANJA = "#FFA500"
VERMELHO = "#FF6347"
ROXO = "#800080"

# 🎨 Estilo visual
st.markdown(f"""
    <style>
        .titulo {{
            font-size: 36px;
            font-weight: bold;
            color: {AZUL};
            margin-bottom: 15px;
        }}
        .card-produto {{
            background-color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }}
        .campo {{
            font-size: 15px;
            margin-bottom: 4px;
        }}
        .status {{
            padding: 5px 10px;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
            color: white;
        }}
        .ativo {{ background-color: {VERDE}; }}
        .inativo {{ background-color: {VERMELHO}; }}
    </style>
""", unsafe_allow_html=True)

# 🧾 Título da página
st.markdown("<div class='titulo'>🧸 Produtos Cadastrados</div>", unsafe_allow_html=True)
st.write("Visualize todos os produtos com informações completas e organizadas.")

# 🔌 Conexão com banco
def conectar():
    caminho_banco = os.path.abspath(os.path.join(os.path.dirname(__file__), "contas_apagar.db"))
    return sqlite3.connect(caminho_banco, check_same_thread=False)

# 📦 Carregar dados
def carregar_dados():
    with conectar() as conn:
        produtos = pd.read_sql_query("SELECT * FROM produtos", conn)
        estoque = pd.read_sql_query("SELECT * FROM estoque", conn)
    df = produtos.merge(estoque, left_on="id", right_on="produto_id", how="left")
    return df.fillna("Não informado")

df = carregar_dados()

# Função segura para pegar dados
def get_safe(row, campo):
    return row[campo] if campo in row and row[campo] not in [None, ""] else "Não informado"

# 📋 Exibir cards organizados
colunas = st.columns(3)

for i, (_, row) in enumerate(df.iterrows()):
    with colunas[i % 3]:
        st.markdown("<div class='card-produto'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:{ROSA}'>{get_safe(row, 'nome')}</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Tipo:</strong> {get_safe(row, 'tipo')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Unidade:</strong> {get_safe(row, 'unidade_compra')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Código:</strong> {get_safe(row, 'codigo')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Marca:</strong> {get_safe(row, 'marca')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Preço Venda:</strong> R$ {get_safe(row, 'preco_venda')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Custo Médio:</strong> R$ {get_safe(row, 'custo_medio')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Estoque Atual:</strong> {get_safe(row, 'estoque_atual')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Estoque Mínimo:</strong> {get_safe(row, 'estoque_minimo')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Estoque Máximo:</strong> {get_safe(row, 'estoque_maximo')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Localização:</strong> {get_safe(row, 'localizacao')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='campo'><strong>Fornecedor:</strong> {get_safe(row, 'fornecedor_padrao')}</div>", unsafe_allow_html=True)

        status = "ativo" if str(get_safe(row, "ativo")) == "1" else "inativo"
        status_texto = "Ativo" if status == "ativo" else "Inativo"
        st.markdown(f"<div class='status {status}'>{status_texto}</div>", unsafe_allow_html=True)

        with st.expander("🔎 Ver mais detalhes"):
            st.markdown(f"- **Descrição:** {get_safe(row, 'descricao')}")
            st.markdown(f"- **Observações:** {get_safe(row, 'observacoes')}")
            st.markdown(f"- **Tipo do Produto:** {get_safe(row, 'tipo_produto')}")
            st.markdown(f"- **Origem:** {get_safe(row, 'origem')}")
            st.markdown(f"- **ICMS CST:** {get_safe(row, 'icms_cst')}")
            st.markdown(f"- **PIS CST:** {get_safe(row, 'pis_cst')}")
            st.markdown(f"- **COFINS CST:** {get_safe(row, 'cofins_cst')}")
            st.markdown(f"- **IPI CST:** {get_safe(row, 'ipi_cst')}")
            st.markdown(f"- **NCM:** {get_safe(row, 'ncm')}")
            st.markdown(f"- **CEST:** {get_safe(row, 'cest')}")
            st.markdown(f"- **Código de Barras:** {get_safe(row, 'cod_barras')}")
            st.markdown(f"- **Código Interno:** {get_safe(row, 'cod_interno')}")
            st.markdown(f"- **Código do Fabricante:** {get_safe(row, 'cod_fabricante')}")
            st.markdown(f"- **Código ANP:** {get_safe(row, 'cod_anp')}")
            st.markdown(f"- **Código do Serviço:** {get_safe(row, 'cod_servico')}")
            st.markdown(f"- **Fator de Conversão:** {get_safe(row, 'fator_conversao')}")

        st.markdown("</div>", unsafe_allow_html=True)

# 🔙 Voltar para o Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="estoque_home")
