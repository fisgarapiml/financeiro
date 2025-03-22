import sqlite3
import os
from nfe import ler_nfe

# Caminho correto e absoluto do banco dentro da pasta src
DB = os.path.join(os.path.dirname(__file__), 'contas_apagar.db')

def criar_tabelas():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Criação da tabela de notas fiscais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave TEXT UNIQUE,
            numero TEXT,
            data_emissao TEXT,
            cnpj_emitente TEXT,
            nome_emitente TEXT,
            cnpj_destinatario TEXT,
            nome_destinatario TEXT
        );
    ''')

    # Criação da tabela de produtos da nota fiscal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos_nfe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nota_id INTEGER,
            codigo_produto TEXT,
            descricao TEXT,
            unidade TEXT,
            quantidade REAL,
            valor_unitario REAL,
            valor_total REAL,
            fator_conversao INTEGER,
            custo_unitario_real REAL,
            percentual_ipi REAL,
            custo_unitario_com_ipi REAL,
            FOREIGN KEY (nota_id) REFERENCES notas_fiscais(id)
        );
    ''')

    conn.commit()
    conn.close()

def verificar_e_criar_coluna(tabela, nome_coluna, tipo_coluna):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({tabela});")
    colunas = [info[1] for info in cursor.fetchall()]

    if nome_coluna not in colunas:
        try:
            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {nome_coluna} {tipo_coluna};")
            print(f"✅ Coluna '{nome_coluna}' adicionada em '{tabela}'")
        except Exception as e:
            print(f"Erro ao adicionar coluna '{nome_coluna}' em '{tabela}':", e)

    conn.commit()
    conn.close()

def nota_ja_existe(chave_nfe):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM notas_fiscais WHERE chave = ?", (chave_nfe,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def salvar_nfe_no_banco(arquivo_xml):
    dados = ler_nfe(arquivo_xml)
    if dados is None or "erro" in dados:
        print("Erro ao ler a NF-e.")
        return

    chave = dados["Nota"].get("Id")
    if nota_ja_existe(chave):
        print("✅ Nota já cadastrada. Nenhuma ação necessária.")
        return

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    nota = dados["Nota"]
    cursor.execute('''
        INSERT INTO notas_fiscais (
            chave, numero, data_emissao, cnpj_emitente, nome_emitente,
            cnpj_destinatario, nome_destinatario
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        nota['Id'],
        nota['Numero'],
        nota['DataEmissao'],
        nota['CNPJ Emitente'],
        nota['Emitente'],
        nota['CNPJ Destinatario'],
        nota['Destinatario']
    ))

    nota_id = cursor.lastrowid

    for p in dados["Produtos"]:
        try:
            quantidade = float(p.get('qCom', '0').replace(",", ".")) if p.get('qCom') else 0
            valor_unitario = float(p.get('vUnCom', '0').replace(",", ".")) if p.get('vUnCom') else 0
            valor_total = float(p.get('vProd', '0').replace(",", ".")) if p.get('vProd') else 0
            fator = p.get('Fator Conversao') or 1
            custo_real = p.get('Custo Unitario Real') or 0
            ipi = p.get('Percentual IPI') or 0
            custo_com_ipi = p.get('Custo Unitario com IPI') or 0
        except:
            quantidade = valor_unitario = valor_total = custo_real = ipi = custo_com_ipi = 0
            fator = 1

        cursor.execute('''
            INSERT INTO produtos_nfe (
                nota_id, codigo_produto, descricao, unidade,
                quantidade, valor_unitario, valor_total,
                fator_conversao, custo_unitario_real,
                percentual_ipi, custo_unitario_com_ipi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nota_id,
            p.get('cProd'),
            p.get('xProd'),
            p.get('uCom'),
            quantidade,
            valor_unitario,
            valor_total,
            fator,
            custo_real,
            ipi,
            custo_com_ipi
        ))

    conn.commit()
    conn.close()
    print("✅ NF-e salva no banco com sucesso!")

if __name__ == '__main__':
    criar_tabelas()
    verificar_e_criar_coluna("notas_fiscais", "numero", "TEXT")
    verificar_e_criar_coluna("produtos_nfe", "percentual_ipi", "REAL")
    verificar_e_criar_coluna("produtos_nfe", "custo_unitario_com_ipi", "REAL")
    salvar_nfe_no_banco('src/exemplo_nfe.xml')
