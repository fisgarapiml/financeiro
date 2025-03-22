import xml.etree.ElementTree as ET

# Fatores de conversão por unidade de compra
FATORES_CONVERSAO = {
    'MIL': 1000,
    'CX': 50,
    'FD': 30,
    'SC': 25
    # Adicione outras unidades conforme necessário
}

def ler_nfe(arquivo_xml):
    """
    Lê um arquivo XML de NF-e e extrai:
    - Dados da nota
    - Produtos com custo unitário real e IPI
    """
    ns = "{http://www.portalfiscal.inf.br/nfe}"
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        infNFe = root.find('.//' + ns + 'infNFe')
        if infNFe is None:
            return {"erro": "Tag infNFe não encontrada."}

        # Dados gerais da nota
        nota_info = {
            'Id': infNFe.get('Id'),
            'Numero': infNFe.findtext(ns + 'ide/' + ns + 'nNF'),  # <- Número da NF-e
            'DataEmissao': infNFe.findtext(ns + 'ide/' + ns + 'dhEmi'),
            'CNPJ Emitente': infNFe.findtext(ns + 'emit/' + ns + 'CNPJ'),
            'Emitente': infNFe.findtext(ns + 'emit/' + ns + 'xNome'),
            'CNPJ Destinatario': infNFe.findtext(ns + 'dest/' + ns + 'CNPJ'),
            'Destinatario': infNFe.findtext(ns + 'dest/' + ns + 'xNome')
        }

        produtos = []
        for det in infNFe.findall(ns + 'det'):
            item = {"nItem": det.get("nItem")}
            prod = det.find(ns + "prod")
            imposto = det.find(ns + "imposto")

            # Inicia as variáveis
            ipi_percentual = 0.0

            if imposto is not None:
                ipi_node = imposto.find(f"{ns}IPI")
                if ipi_node is not None:
                    ipi_trib = ipi_node.find(f"{ns}IPITrib")
                    if ipi_trib is not None:
                        pIPI = ipi_trib.findtext(f"{ns}pIPI")
                        try:
                            ipi_percentual = float(pIPI.replace(",", ".")) if pIPI else 0.0
                        except:
                            ipi_percentual = 0.0

            if prod is not None:
                item["cProd"] = prod.findtext(ns + "cProd")
                item["xProd"] = prod.findtext(ns + "xProd")
                item["uCom"] = prod.findtext(ns + "uCom")
                item["qCom"] = prod.findtext(ns + "qCom")
                item["vUnCom"] = prod.findtext(ns + "vUnCom")
                item["vProd"] = prod.findtext(ns + "vProd")

                try:
                    unidade = item["uCom"].upper() if item["uCom"] else ""
                    fator = FATORES_CONVERSAO.get(unidade, 1)
                    vUnCom = float(item["vUnCom"].replace(",", ".")) if item["vUnCom"] else 0
                    custo_real = round(vUnCom / fator, 4) if fator else 0
                    custo_com_ipi = round(custo_real * (1 + ipi_percentual / 100), 4)

                    item["Fator Conversao"] = fator
                    item["Custo Unitario Real"] = custo_real
                    item["Percentual IPI"] = ipi_percentual
                    item["Custo Unitario com IPI"] = custo_com_ipi
                except:
                    item["Fator Conversao"] = None
                    item["Custo Unitario Real"] = None
                    item["Percentual IPI"] = None
                    item["Custo Unitario com IPI"] = None

            produtos.append(item)

        return {
            "Nota": nota_info,
            "Produtos": produtos
        }

    except ET.ParseError as e:
        print("Erro ao processar o XML:", e)
        return None
    except Exception as e:
        print("Ocorreu um erro:", e)
        return None


def exibir_info_nfe(arquivo_xml):
    info = ler_nfe(arquivo_xml)
    if info:
        if "erro" in info:
            print(info["erro"])
            return

        print("Informações da Nota:")
        for chave, valor in info["Nota"].items():
            print(f"{chave}: {valor}")

        print("\nProdutos:")
        for prod in info["Produtos"]:
            print("-" * 40)
            for chave, valor in prod.items():
                print(f"{chave}: {valor}")
    else:
        print("Não foi possível extrair informações da NF-e.")


if __name__ == '__main__':
    exibir_info_nfe('exemplo_nfe.xml')
