import sqlite3
import os

# Caminho direto para o arquivo dentro da pasta atual
caminho_banco = "financeiro.db"

# Verificar se o arquivo existe
if not os.path.exists(caminho_banco):
    print(f"❌ Banco de dados não encontrado em: {caminho_banco}")
else:
    # Conectar ao banco
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Listar todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    if not tabelas:
        print("⚠️ Nenhuma tabela encontrada no banco.")
    else:
        print("\n🔍 Tabelas encontradas no banco financeiro.db:")
        for tabela in tabelas:
            print(f" - {tabela[0]}")

    # Fechar conexão
    conn.close()
