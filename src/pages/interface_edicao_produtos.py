import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="✏️ Edição de Produtos", layout="centered")
st.title("✏️ Editar Produto Cadastrado")

# Conexão com banco
def conectar():
    caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "contas_apagar.db"))
    return sqlite3.connect(caminho, check_same_thread=False)

# Carregar todos os produtos para busca
def carregar_produtos():
    with conectar() as conn:
        df = pd.read_sql_query("SELECT id, nome, codigo FROM produtos ORDER BY nome", conn)
    return df

# Buscar dados de um produto pelo ID
def carregar_dados_produto(id_produto):
    with conectar() as conn:
        produto = pd.read_sql_query(f"SELECT * FROM produtos WHERE id = {id_produto}", conn)
    return produto.iloc[0] if not produto.empty else None

# Atualizar produto
def salvar_alteracoes(id_produto, dados):
    with conectar() as conn:
        cursor = conn.cursor()
        query = """
            UPDATE produtos SET
                tipo=?, nome=?, codigo=?, marca=?, descricao=?, unidade_compra=?,
                fator_conversao=?, preco_venda=?, custo_medio=?, ncm=?, cest=?,
                cod_barras=?, cod_interno=?, fornecedor_padrao=?, cod_fabricante=?,
                observacoes=?, estoque_minimo=?, estoque_maximo=?, localizacao=?,
                tipo_produto=?, origem=?, icms_cst=?, pis_cst=?, cofins_cst=?, ipi_cst=?,
                cod_anp=?, cod_servico=?, ativo=?
            WHERE id=?
        """
        valores = (*dados, id_produto)
        cursor.execute(query, valores)
        conn.commit()

# Interface principal
df_produtos = carregar_produtos()
produto_selecionado = st.selectbox("🔍 Selecione o produto para editar", df_produtos["nome"])

if produto_selecionado:
    id_produto = df_produtos[df_produtos["nome"] == produto_selecionado]["id"].values[0]
    dados = carregar_dados_produto(id_produto)

    if dados is not None:
        # Formulário preenchido com os dados reais
        tipo = st.selectbox("Tipo de Produto", ["Simples", "Kit", "Com Variação"], index=["Simples", "Kit", "Com Variação"].index(dados["tipo"]))
        nome = st.text_input("Nome do Produto", dados["nome"])
        codigo = st.text_input("Código", dados["codigo"])
        marca = st.text_input("Marca", dados["marca"])
        descricao = st.text_area("Descrição", dados["descricao"])
        unidade = st.text_input("Unidade de Compra", dados["unidade_compra"])
        fator = st.number_input("Fator de Conversão", min_value=1, value=int(dados["fator_conversao"]))
        preco_venda = st.number_input("Preço de Venda", min_value=0.0, value=float(dados["preco_venda"]), format="%.2f")
        custo_medio = st.number_input("Custo Médio", min_value=0.0, value=float(dados["custo_medio"]), format="%.4f")
        ncm = st.text_input("NCM", dados["ncm"])
        cest = st.text_input("CEST", dados["cest"])
        cod_barras = st.text_input("Código de Barras", dados["cod_barras"])
        cod_interno = st.text_input("Código Interno", dados["cod_interno"])
        fornecedor = st.text_input("Fornecedor Padrão", dados["fornecedor_padrao"])
        cod_fabricante = st.text_input("Código do Fabricante", dados["cod_fabricante"])
        observacoes = st.text_area("Observações", dados["observacoes"])
        estoque_min = st.number_input("Estoque Mínimo", min_value=0.0, value=float(dados["estoque_minimo"]))
        estoque_max = st.number_input("Estoque Máximo", min_value=0.0, value=float(dados["estoque_maximo"]))
        localizacao = st.text_input("Localização", dados["localizacao"])
        tipo_produto = st.text_input("Tipo do Produto", dados["tipo_produto"])
        origem = st.text_input("Origem", dados["origem"])
        icms = st.text_input("ICMS CST", dados["icms_cst"])
        pis = st.text_input("PIS CST", dados["pis_cst"])
        cofins = st.text_input("COFINS CST", dados["cofins_cst"])
        ipi = st.text_input("IPI CST", dados["ipi_cst"])
        cod_anp = st.text_input("Código ANP", dados["cod_anp"])
        cod_servico = st.text_input("Código do Serviço", dados["cod_servico"])
        ativo = st.checkbox("Produto Ativo", value=bool(dados["ativo"]))

        st.markdown("---")
        if st.button("💾 Salvar Alterações"):
            novos_dados = (
                tipo, nome, codigo, marca, descricao, unidade, fator,
                preco_venda, custo_medio, ncm, cest, cod_barras, cod_interno,
                fornecedor, cod_fabricante, observacoes, estoque_min, estoque_max,
                localizacao, tipo_produto, origem, icms, pis, cofins, ipi,
                cod_anp, cod_servico, int(ativo)
            )
            salvar_alteracoes(id_produto, novos_dados)
            st.success("✅ Alterações salvas com sucesso!")
    else:
        st.error("❌ Produto não encontrado no banco de dados.")
