import sqlite3
from nfe import ler_nfe

DB = 'contas_apagar.db'

def criar_tabelas():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Criação da tabela de notas fiscais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave TEXT,
            data_emissao TEXT,
            cnpj_emitente TEXT,
            nome_emitente TEXT,
            cnpj_destinatario TEXT,
            nome_destinatario TEXT
        );
    ''')

    # Criação da tabela de produtos da NF-e (estrutura base)
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
            FOREIGN KEY (nota_id) REFERENCES notas_fiscais(id)
        );
    ''')

    conn.commit()
    conn.close()

def verificar_e_criar_coluna(nome_coluna, tipo_coluna):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Verifica se a coluna existe
    cursor.execute("PRAGMA table_info(produtos_nfe);")
    colunas = [info[1] for info in cursor.fetchall()]

    if nome_coluna not in colunas:
        try:
            cursor.execute(f"ALTER TABLE produtos_nfe ADD COLUMN {nome_coluna} {tipo_coluna};")
            print(f"✅ Coluna '{nome_coluna}' criada com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar coluna '{nome_coluna}':", e)

    conn.commit()
    conn.close()

def salvar_nfe_no_banco(arquivo_xml):
    dados = ler_nfe(arquivo_xml)
    if dados is None or "erro" in dados:
        print("Erro ao ler a NF-e.")
        return

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Inserir nota fiscal
    nota = dados["Nota"]
    cursor.execute('''
        INSERT INTO notas_fiscais (
            chave, data_emissao, cnpj_emitente, nome_emitente,
            cnpj_destinatario, nome_destinatario
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        nota['Id'],
        nota['DataEmissao'],
        nota['CNPJ Emitente'],
        nota['Emitente'],
        nota['CNPJ Destinatario'],
        nota['Destinatario']
    ))

    nota_id = cursor.lastrowid

    # Inserir os produtos
    for p in dados["Produtos"]:
        try:
            quantidade = float(p.get('qCom', '0').replace(",", ".")) if p.get('qCom') else 0
            valor_unitario = float(p.get('vUnCom', '0').replace(",", ".")) if p.get('vUnCom') else 0
            valor_total = float(p.get('vProd', '0').replace(",", ".")) if p.get('vProd') else 0
            fator = p.get('Fator Conversao') or 1
            custo_real = p.get('Custo Unitario Real') or 0
            ipi = p.get('Percentual IPI') or 0
        except:
            quantidade = valor_unitario = valor_total = custo_real = ipi = 0
            fator = 1

        cursor.execute('''
            INSERT INTO produtos_nfe (
                nota_id, codigo_produto, descricao, unidade,
                quantidade, valor_unitario, valor_total,
                fator_conversao, custo_unitario_real, percentual_ipi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            ipi
        ))

    conn.commit()
    conn.close()
    print("NF-e salva no banco com sucesso!")


if __name__ == '__main__':
    criar_tabelas()
    verificar_e_criar_coluna("percentual_ipi", "REAL")
    salvar_nfe_no_banco('exemplo_nfe.xml')
