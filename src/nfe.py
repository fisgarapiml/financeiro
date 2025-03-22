import xml.etree.ElementTree as ET

# Fatores de conversão por unidade de compra
FATORES_CONVERSAO = {
    'MIL': 1000,
    'CX': 50,
    'FD': 30,
    'SC': 25
    # Adicione outras unidades conforme sua realidade
}

def ler_nfe(arquivo_xml):
    """
    Lê um arquivo XML de NF-e e extrai:
    - Dados da nota
    - Produtos (com cálculo de custo unitário real e alíquota de IPI)
    """
    ns = "{http://www.portalfiscal.inf.br/nfe}"
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        infNFe = root.find('.//' + ns + 'infNFe')
        if infNFe is None:
            return {"erro": "Tag infNFe não encontrada."}

        nota_info = {
            'Id': infNFe.get('Id'),
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
            ipi = imposto.find(ns + "IPI/" + ns + "IPITrib") if imposto is not None else None

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

                    item["Fator Conversao"] = fator
                    item["Custo Unitario Real"] = custo_real
                except:
                    item["Fator Conversao"] = None
                    item["Custo Unitario Real"] = None

                # Extração da alíquota de IPI (%)
                try:
                    pIPI = ipi.findtext(ns + "pIPI") if ipi is not None else None
                    item["Percentual IPI"] = float(pIPI.replace(",", ".")) if pIPI else 0.0
                except:
                    item["Percentual IPI"] = 0.0

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
    """
    Exibe os dados extraídos da NF-e de forma organizada.
    """
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
