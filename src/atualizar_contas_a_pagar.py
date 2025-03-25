import pandas as pd
import sqlite3
import re

# Mapeamentos (resumo mantido para visualização – mantenha os completos no seu código)
mapeamento_categorias = {
    "Café da Manhã": "Alimentação",
    "Contabilidade": "Custo Fixo",
    "Altamiris Goes": "Custo Fixo",
    # ... (demais mapeamentos)
}

mapeamento_nome_razao_social = {
    "Elismar Mota": "Funcionários",
    "Prolabores": "Funcionários",
    "Restaurante": "Fornecedores",
    # ... (demais mapeamentos)
}

custo_fixo_variavel = {
    "Funcionários": "Fixo",
    "Custo Fixo": "Fixo",
    "Impostos": "Variável",
    "Fornecedores": "Variável",
    "Água/Luz/Telefone": "Fixo",
    # ... (demais tipos)
}

# Função para normalizar nomes de colunas
def normalizar_nome_coluna(nome):
    return re.sub(r'[^a-zA-Z0-9_]', '_', nome)

# Carregar Google Sheets sem autenticação
def carregar_planilha_google_sheets(sheet_id, sheet_name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        print("✅ Planilha carregada com sucesso do Google Sheets.")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar a planilha: {e}")
        return None

# Processar e categorizar os dados
def processar_dados(df):
    try:
        df.columns = [normalizar_nome_coluna(coluna.strip().lower().replace(" ", "_")) for coluna in df.columns]

        if 'codigo' not in df.columns:
            df['codigo'] = range(1, len(df) + 1)

        # Mapeia categorias
        df['categorias'] = df['plano_de_contas'].astype(str).str.strip().map(mapeamento_categorias).fillna("Outros")

        # Verifica coluna de nome/razão social
        nome_coluna_razao_social = None
        for col in df.columns:
            if "nome___raz_o_social" in col:
                nome_coluna_razao_social = col
                break

        if nome_coluna_razao_social:
            df['categorias'] = df[nome_coluna_razao_social].map(mapeamento_nome_razao_social).fillna(df['categorias'])

        # Garante que "Contabilidade" e "Altamiris Goes" sejam "Custo Fixo"
        df.loc[df['plano_de_contas'] == "Contabilidade", 'categorias'] = "Custo Fixo"
        df.loc[df['plano_de_contas'] == "Altamiris Goes", 'categorias'] = "Custo Fixo"

        # Define o tipo de custo (Fixo ou Variável)
        df['tipo_custo'] = df['categorias'].apply(
            lambda x: "Fixo" if x == "Funcionários" or x == "Custo Fixo" else custo_fixo_variavel.get(x, "Variável")
        )

        # 🔁 Converte 'valor' para negativo
        if 'r__valor' in df.columns:
            df['r__valor'] = df['r__valor'].astype(str).str.replace(',', '.').astype(float)
            df['r__valor'] = df['r__valor'].apply(lambda x: -abs(x))

        # 🔁 Converte 'valor_pago' para positivo
        if 'r__pago' in df.columns:
            df['r__pago'] = df['r__pago'].astype(str).str.replace(',', '.').astype(float)
            df['r__pago'] = df['r__pago'].apply(lambda x: abs(x))

        # ✅ Renomeia colunas para o padrão do sistema
        colunas_renomear = {
            'nome___raz_o_social': 'fornecedor',
            'r__valor': 'valor',
            'r__pago': 'valor_pago',
            'r__pendente': 'valor_pendente',
            'n__documento': 'documento',
            'tipo_documento': 'documento_tipo',
            'tipo_pagamento': 'pagamento_tipo',
            'data_compet_ncia': 'data_competencia',
            'coment_rios': 'comentario',
            'c_digo': 'codigo_externo'
        }
        df.rename(columns=colunas_renomear, inplace=True)

        # Remove duplicatas e finaliza
        df.drop_duplicates(inplace=True)
        print("✅ Dados processados com sucesso.")
        return df

    except Exception as e:
        print(f"❌ Erro ao processar os dados: {e}")
        return None

# Importar no SQLite com atualização
def importar_para_sqlite(df, banco_dados):
    try:
        conn = sqlite3.connect(banco_dados)
        cursor = conn.cursor()

        colunas = list(df.columns)
        colunas_sql = ", ".join([f'"{col}" TEXT' for col in colunas if col != "codigo"])
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS contas_a_pagar (
                codigo INTEGER PRIMARY KEY,
                {colunas_sql}
            )
        ''')

        colunas_insert = ", ".join([f'"{col}"' for col in df.columns])
        placeholders = ", ".join(["?" for _ in df.columns])

        for _, row in df.iterrows():
            cursor.execute(f'''
                INSERT INTO contas_a_pagar ({colunas_insert}) VALUES ({placeholders})
                ON CONFLICT(codigo) DO UPDATE SET
                {", ".join([f'{col} = EXCLUDED.{col}' for col in df.columns if col != "codigo"])}
            ''', tuple(row))

        conn.commit()
        conn.close()
        print("✅ Dados importados com sucesso no banco SQLite.")
    except Exception as e:
        print(f"❌ Erro ao importar para SQLite: {e}")

# FLUXO PRINCIPAL
if __name__ == "__main__":
    sheet_id = "1zj7fuvta2T55G0-cPnWthEfrVnqaui9u2EJ2cBJp64M"
    sheet_name = "financeiro"

    df = carregar_planilha_google_sheets(sheet_id, sheet_name)
    if df is not None:
        df_processado = processar_dados(df)
        if df_processado is not None:
            print("\n🔎 Exemplo de dados processados:")
            print(df_processado[['codigo', 'categorias', 'tipo_custo']].head())
            importar_para_sqlite(df_processado, "grupo_fisgar.db")
