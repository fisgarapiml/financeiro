import streamlit as st
import sqlite3
import os

# Configuração da página
st.set_page_config(page_title="Cadastro de Produtos", layout="centered")
st.title("📦 Cadastro de Produtos")

# Função para conectar ao banco de dados (corrigido para pasta correta)
def conectar_banco():
    db_path = os.path.join(os.path.dirname(__file__), "contas_apagar.db")
    return sqlite3.connect(db_path)

# Campos do cadastro
tipo = st.selectbox("Tipo de Produto", ["Simples", "Kit", "Com Variação"])
nome = st.text_input("Nome do Produto")
codigo = st.text_input("Código")
marca = st.text_input("Marca")
descricao = st.text_area("Descrição")
unidade = st.text_input("Unidade de Compra (ex: CX, MIL, UN)")
fator = st.number_input("Fator de Conversão para unidade real", min_value=1, value=1)
preco_venda = st.number_input("Preço de Venda Sugerido", min_value=0.0, format="%.2f")
custo_medio = st.number_input("Custo Médio", min_value=0.0, format="%.4f")
ncm = st.text_input("NCM")
cest = st.text_input("CEST")
cod_barras = st.text_input("Código de Barras")
cod_interno = st.text_input("Código Interno")
fornecedor = st.text_input("Fornecedor Padrão")
cod_fabricante = st.text_input("Código do Fabricante")
observacoes = st.text_area("Observações")
estoque_min = st.number_input("Estoque Mínimo", min_value=0.0)
estoque_max = st.number_input("Estoque Máximo", min_value=0.0)
localizacao = st.text_input("Localização no Estoque")
tipo_produto = st.text_input("Tipo do Produto (revenda, consumo, etc.)")
origem = st.text_input("Origem (0 a 8)")
icms = st.text_input("ICMS CST")
pis = st.text_input("PIS CST")
cofins = st.text_input("COFINS CST")
ipi = st.text_input("IPI CST")
cod_anp = st.text_input("Código ANP")
cod_servico = st.text_input("Código do Serviço")
ativo = st.checkbox("Produto Ativo", value=True)

# Botão para salvar
tem_erro = False
if st.button("📂 Salvar Produto"):
    if not nome or not codigo:
        st.error("⚠️ Nome e Código são obrigatórios.")
        tem_erro = True

    if not tem_erro:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO produtos (
                tipo, nome, codigo, marca, descricao, unidade_compra,
                fator_conversao, preco_venda, custo_medio, ncm, cest,
                cod_barras, cod_interno, fornecedor_padrao, cod_fabricante,
                observacoes, estoque_minimo, estoque_maximo, localizacao,
                tipo_produto, origem, icms_cst, pis_cst, cofins_cst, ipi_cst,
                cod_anp, cod_servico, ativo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tipo, nome, codigo, marca, descricao, unidade, fator, preco_venda,
            custo_medio, ncm, cest, cod_barras, cod_interno, fornecedor,
            cod_fabricante, observacoes, estoque_min, estoque_max,
            localizacao, tipo_produto, origem, icms, pis, cofins, ipi,
            cod_anp, cod_servico, int(ativo)
        ))

        conn.commit()
        conn.close()
        st.success("✅ Produto cadastrado com sucesso!")

