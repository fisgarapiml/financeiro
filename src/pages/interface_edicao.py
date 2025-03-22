import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Editar Produto", layout="centered")
st.title("✏️ Edição de Produto")

# Conectar ao banco de dados
def conectar():
    db_path = os.path.join(os.path.dirname(__file__), "../contas_apagar.db")
    return sqlite3.connect(db_path)

# Buscar dados do produto por ID
def carregar_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    colunas = [col[0] for col in cursor.description]
    valores = cursor.fetchone()
    conn.close()
    if valores:
        return dict(zip(colunas, valores))
    return None

# Atualizar produto no banco de dados
def salvar_edicao(produto_id, dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos SET
            tipo=?, nome=?, codigo=?, marca=?, descricao=?, unidade_compra=?,
            fator_conversao=?, preco_venda=?, custo_medio=?, ncm=?, cest=?,
            cod_barras=?, cod_interno=?, fornecedor_padrao=?, cod_fabricante=?,
            observacoes=?, estoque_minimo=?, estoque_maximo=?, localizacao=?,
            tipo_produto=?, origem=?, icms_cst=?, pis_cst=?, cofins_cst=?, ipi_cst=?,
            cod_anp=?, cod_servico=?, ativo=?
        WHERE id=?
    ''', (*dados.values(), produto_id))
    conn.commit()
    conn.close()

# Verifica se veio ID pela sessão
st.write("Session state:", st.session_state)  # Ajuda para debug

if 'produto_id_editar' not in st.session_state:
    st.warning("Nenhum produto selecionado para edição.")
    st.stop()

# Corrigir o ID mesmo que venha como np.int64(1)
produto_id_raw = st.session_state['produto_id_editar']
try:
    produto_id = int(str(produto_id_raw).replace("np.int64(", "").replace(")", ""))
except:
    st.error("ID inválido. Não foi possível processar o produto.")
    st.stop()

dados = carregar_produto(produto_id)

if not dados:
    st.error(f"Produto com ID {produto_id} não encontrado no banco de dados.")
    st.stop()

# Formulário preenchido com os dados do produto
tipo = st.selectbox("Tipo", ["Simples", "Kit", "Com Variação"], index=["Simples", "Kit", "Com Variação"].index(dados['tipo']))
nome = st.text_input("Nome", dados['nome'])
codigo = st.text_input("Código", dados['codigo'])
marca = st.text_input("Marca", dados['marca'])
descricao = st.text_area("Descrição", dados['descricao'])
unidade = st.text_input("Unidade de Compra", dados['unidade_compra'])
fator = st.number_input("Fator de Conversão", min_value=1, value=dados['fator_conversao'])
preco_venda = st.number_input("Preço de Venda", value=dados['preco_venda'], format="%.2f")
custo_medio = st.number_input("Custo Médio", value=dados['custo_medio'], format="%.4f")
ncm = st.text_input("NCM", dados['ncm'])
cest = st.text_input("CEST", dados['cest'])
cod_barras = st.text_input("Código de Barras", dados['cod_barras'])
cod_interno = st.text_input("Código Interno", dados['cod_interno'])
fornecedor = st.text_input("Fornecedor", dados['fornecedor_padrao'])
cod_fab = st.text_input("Código Fabricante", dados['cod_fabricante'])
obs = st.text_area("Observações", dados['observacoes'])
est_min = st.number_input("Estoque Mínimo", value=dados['estoque_minimo'])
est_max = st.number_input("Estoque Máximo", value=dados['estoque_maximo'])
local = st.text_input("Localização", dados['localizacao'])
tipo_prod = st.text_input("Tipo Produto", dados['tipo_produto'])
origem = st.text_input("Origem", dados['origem'])
icms = st.text_input("ICMS CST", dados['icms_cst'])
pis = st.text_input("PIS CST", dados['pis_cst'])
cofins = st.text_input("COFINS CST", dados['cofins_cst'])
ipi = st.text_input("IPI CST", dados['ipi_cst'])
anp = st.text_input("Código ANP", dados['cod_anp'])
servico = st.text_input("Código Serviço", dados['cod_servico'])
ativo = st.checkbox("Ativo", value=bool(dados['ativo']))

if st.button("💾 Salvar Alterações"):
    novo_dados = {
        "tipo": tipo,
        "nome": nome,
        "codigo": codigo,
        "marca": marca,
        "descricao": descricao,
        "unidade_compra": unidade,
        "fator_conversao": fator,
        "preco_venda": preco_venda,
        "custo_medio": custo_medio,
        "ncm": ncm,
        "cest": cest,
        "cod_barras": cod_barras,
        "cod_interno": cod_interno,
        "fornecedor_padrao": fornecedor,
        "cod_fabricante": cod_fab,
        "observacoes": obs,
        "estoque_minimo": est_min,
        "estoque_maximo": est_max,
        "localizacao": local,
        "tipo_produto": tipo_prod,
        "origem": origem,
        "icms_cst": icms,
        "pis_cst": pis,
        "cofins_cst": cofins,
        "ipi_cst": ipi,
        "cod_anp": anp,
        "cod_servico": servico,
        "ativo": int(ativo)
    }
    salvar_edicao(produto_id, novo_dados)
    st.success("Produto atualizado com sucesso!")
    st.link_button("⬅ Voltar para listagem", url="/interface_listagem")
