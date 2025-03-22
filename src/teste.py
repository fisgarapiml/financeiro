import sqlite3

def inserir_produto_teste():
    conn = sqlite3.connect("src/contas_apagar.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos (
            tipo, nome, codigo, marca, descricao, unidade_compra,
            fator_conversao, preco_venda, custo_medio, ncm, cest,
            cod_barras, cod_interno, fornecedor_padrao, cod_fabricante,
            observacoes, estoque_minimo, estoque_maximo, localizacao,
            tipo_produto, origem, icms_cst, pis_cst, cofins_cst, ipi_cst,
            cod_anp, cod_servico, ativo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Simples', 'Produto Teste', 'TESTE123', 'Marca X', 'Produto de Teste automatizado',
        'UN', 1, 19.90, 10.50, '12345678', '1234567', '7890000000001', 'INT123',
        'Fornecedor Teste', 'FAB123', 'Sem observações', 10, 100, 'Est1',
        'revenda', '0', '00', '01', '01', '50', '', '', 1
    ))

    conn.commit()
    conn.close()
    print("✅ Produto de teste inserido com sucesso!")

if __name__ == "__main__":
    inserir_produto_teste()
