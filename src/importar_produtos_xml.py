import xml.etree.ElementTree as ET
import sqlite3
import os

def importar_produtos_xml(xml_path):
    novos_produtos = []
    produtos_atualizados = []
    aumentaram_custo = []

    # Caminho do banco
    caminho_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "contas_apagar.db"))
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # Ler o XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Namespace do XML
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    for det in root.findall(".//nfe:det", ns):
        prod = det.find("nfe:prod", ns)
        imposto = det.find("nfe:imposto", ns)
        ipi_tag = imposto.find("nfe:IPI", ns) if imposto is not None else None

        # Dados extraídos do XML
        nome = prod.findtext("nfe:xProd", default="Não informado", namespaces=ns)
        cod_barras = prod.findtext("nfe:cEAN", default="", namespaces=ns)
        cod_interno = prod.findtext("nfe:cProd", default="", namespaces=ns)
        codigo = cod_interno  # Usando o mesmo valor para o campo "codigo"
        ncm = prod.findtext("nfe:NCM", default="", namespaces=ns)
        cest = prod.findtext("nfe:CEST", default="", namespaces=ns)
        unidade = prod.findtext("nfe:uCom", default="", namespaces=ns)
        quantidade = float(prod.findtext("nfe:qCom", default="1", namespaces=ns))
        valor_total = float(prod.findtext("nfe:vProd", default="0", namespaces=ns))

        valor_unitario = valor_total / quantidade if quantidade else 0

        # Percentual de IPI
        aliq_ipi = 0.0
        if ipi_tag is not None:
            for ipi_tipo in ["IPITrib", "IPINT"]:
                c = ipi_tag.find(f"nfe:{ipi_tipo}", ns)
                if c is not None:
                    aliq_ipi = float(c.findtext("nfe:pIPI", default="0", namespaces=ns))
                    break

        custo_final = valor_unitario * (1 + aliq_ipi / 100)

        # Verificar se o produto já existe
        cursor.execute("""
            SELECT * FROM produtos WHERE cod_barras = ? OR cod_interno = ?
        """, (cod_barras, cod_interno))
        existente = cursor.fetchone()

        if existente is None:
            # Inserir novo produto (com 28 campos!)
            cursor.execute("""
                INSERT INTO produtos (
                    tipo, nome, codigo, marca, descricao, unidade_compra,
                    fator_conversao, preco_venda, custo_medio, ncm, cest,
                    cod_barras, cod_interno, fornecedor_padrao, cod_fabricante,
                    observacoes, estoque_minimo, estoque_maximo, localizacao,
                    tipo_produto, origem, icms_cst, pis_cst, cofins_cst, ipi_cst,
                    cod_anp, cod_servico, ativo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "Simples", nome, codigo, "", "", unidade, 1,
                0.00, round(custo_final, 4), ncm, cest,
                cod_barras, cod_interno, "", "", "", 0, 0,
                "", "", "", "", "", "", "", "", 1
            ))
            novos_produtos.append(nome)
        else:
            # Produto já existe — atualizar custo se necessário
            id_produto = existente[0]
            custo_atual = float(existente[8])  # custo_medio

            if round(custo_final, 4) != round(custo_atual, 4):
                if custo_final > custo_atual:
                    aumentaram_custo.append(nome)

                cursor.execute("""
                    UPDATE produtos SET custo_medio = ? WHERE id = ?
                """, (round(custo_final, 4), id_produto))
                produtos_atualizados.append(nome)

    conn.commit()
    conn.close()

    return novos_produtos, produtos_atualizados, aumentaram_custo
