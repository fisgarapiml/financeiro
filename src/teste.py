import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="🔄 Teste de Lançamentos", layout="wide")
st.title("🧪 Inserir 10 Movimentações Fictícias")

# 🎨 Paleta de Cores
AZUL_TURQUESA = "#40E0D0"
AMARELO_ALEGRE = "#FFD700"
ROSA_VIBRANTE = "#FF69B4"
VERDE_LIMAO = "#32CD32"
LARANJA = "#FFA500"
ROXO = "#800080"

# Estilo personalizado para feedback visual
st.markdown(f"""
    <style>
        .stAlert > div {{
            background-color: {VERDE_LIMAO}20;
            border-left: 5px solid {VERDE_LIMAO};
        }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: {AZUL_TURQUESA};
        }}
        .stButton > button {{
            background-color: {LARANJA};
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }}
        .stButton > button:hover {{
            background-color: {ROXO};
        }}
    </style>
""", unsafe_allow_html=True)

# Caminho do banco
db_path = os.path.join(os.path.dirname(__file__), "contas_apagar.db")

# Conexão
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Produtos fictícios
produtos = [
    (f"Produto Teste {i}", f"000{i:03d}") for i in range(1, 11)
]

# Verifica se o produto existe e insere caso não exista
def garantir_produtos():
    for nome, codigo in produtos:
        cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()
        if not resultado:
            cursor.execute("""
                INSERT INTO produtos (
                    tipo, nome, codigo, marca, descricao, unidade_compra, fator_conversao,
                    preco_venda, custo_medio, ncm, cest, cod_barras, cod_interno,
                    fornecedor_padrao, cod_fabricante, observacoes, estoque_minimo,
                    estoque_maximo, localizacao, tipo_produto, origem, icms_cst,
                    pis_cst, cofins_cst, ipi_cst, cod_anp, cod_servico, ativo
                ) VALUES (
                    'Simples', ?, ?, 'Marca Teste', 'Descrição Teste', 'CX', 1,
                    10.00, 5.00, '00000000', '', '', '',
                    'Fornecedor Teste', '', '', 10, 100, 'Estoque A',
                    'Revenda', '0', '00', '01', '01', '50', '', '', 1
                )
            """, (nome, codigo))
    conn.commit()

# Inserir movimentações para os produtos
def inserir_movimentacoes():
    for nome, codigo in produtos:
        cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo,))
        produto_id = cursor.fetchone()
        if produto_id:
            cursor.execute("""
                INSERT INTO movimentacoes_estoque (
                    produto_id, tipo, quantidade, data_movimentacao, origem, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                produto_id[0], 'Entrada', 50,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Teste', f'Movimentação de {nome}'
            ))
    conn.commit()

# Execução
garantir_produtos()
inserir_movimentacoes()

st.success("✅ Produtos e movimentações fictícias inseridos com sucesso!")
