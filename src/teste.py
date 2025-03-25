import sqlite3
import os

# Caminhos dos bancos
origem = "financeiro.db"
destino = "grupo_fisgar.db"

# Conectar à origem
conn_origem = sqlite3.connect(origem)
cur_origem = conn_origem.cursor()

# Criar destino
conn_destino = sqlite3.connect(destino)
cur_destino = conn_destino.cursor()

# Criar tabela padronizada no banco destino
cur_destino.execute("""
CREATE TABLE IF NOT EXISTS contas_a_pagar (
    id INTEGER PRIMARY KEY,
    vencimento TEXT,
    fornecedor TEXT,
    valor REAL,
    valor_pendente REAL,
    valor_pago REAL,
    tipo_documento TEXT,
    plano_contas TEXT,
    data_cadastro TEXT,
    data_competencia TEXT,
    data_pagamento TEXT,
    status TEXT,
    categoria TEXT,
    tipo_custo TEXT,
    comentarios TEXT
);
""")

# Buscar dados da tabela antiga
cur_origem.execute("SELECT * FROM contas_a_pagar")
colunas = [desc[0] for desc in cur_origem.description]
dados = cur_origem.fetchall()

# Mapeamento de nomes antigos → novos
def mapear_linha(linha):
    dados_dict = dict(zip(colunas, linha))
    return (
        dados_dict.get("codigo"),
        dados_dict.get("vencimento"),
        dados_dict.get("nome___raz_o_social"),
        float(str(dados_dict.get("r__valor", "0")).replace(",", ".")),
        float(str(dados_dict.get("r__pendente", "0")).replace(",", ".")),
        float(str(dados_dict.get("r__pago", "0")).replace(",", ".")),
        dados_dict.get("tipo_documento"),
        dados_dict.get("plano_de_contas"),
        dados_dict.get("data_cadastro"),
        dados_dict.get("data_compet_ncia"),
        dados_dict.get("data_pagamento"),
        dados_dict.get("status"),
        dados_dict.get("categorias"),
        dados_dict.get("tipo_custo"),
        dados_dict.get("coment_rios")
    )

# Inserir no banco novo
for linha in dados:
    nova_linha = mapear_linha(linha)
    cur_destino.execute("""
        INSERT INTO contas_a_pagar (
            id, vencimento, fornecedor, valor, valor_pendente, valor_pago,
            tipo_documento, plano_contas, data_cadastro, data_competencia,
            data_pagamento, status, categoria, tipo_custo, comentarios
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, nova_linha)

# Finalizar
conn_destino.commit()
conn_origem.close()
conn_destino.close()

print("✅ Migração concluída com sucesso! Dados transferidos para grupo_fisgar.db.")
