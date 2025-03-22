from financeiro import exibir_info_financeira
from nfe import exibir_info_nfe

def main():
    print("Projeto Financeiro iniciado!")
    exibir_info_financeira()
    # Chama o processamento de NF-e; ajuste o caminho conforme necessário
    exibir_info_nfe('exemplo_nfe.xml')

if __name__ == '__main__':
    main()
