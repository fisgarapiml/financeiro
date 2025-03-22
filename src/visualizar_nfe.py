import pandas as pd
from nfe import ler_nfe  # Supondo que sua função ler_nfe está em nfe.py

def visualizar_dados_nfe(arquivo_xml):
    # Extrai os dados do XML
    dados = ler_nfe(arquivo_xml)
    if dados:
        # Converte o dicionário em uma lista de tuplas e cria um DataFrame
        df = pd.DataFrame(list(dados.items()), columns=['Campo', 'Valor'])
        print(df)
    else:
        print("Não foi possível extrair os dados da NF-e.")

if __name__ == '__main__':
    visualizar_dados_nfe('exemplo_nfe.xml')
