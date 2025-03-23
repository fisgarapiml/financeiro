import streamlit as st
import sqlite3
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="🧮 Edição em Massa de Produtos", layout="wide")
st.title("🧾 Lista de Produtos com Edição em Massa")

# Caminho do banco
db_path = os.path.join(os.path.dirname(__file__), "../contas_apagar.db")

# Conexão
def conectar():
    return sqlite3.connect(db_path)

# Carregar dados
def carregar_dados():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM produtos", conn)
    conn.close()
    return df

# Atualizar apenas os registros alterados (sem substituir a tabela inteira)
def atualizar_registros_alterados(df_original, df_editado):
    conn = conectar()
    cursor = conn.cursor()

    colunas = df_original.columns.tolist()

    for index, row in df_editado.iterrows():
        if not row.equals(df_original.loc[index]):
            set_clause = ", ".join([f"{col} = ?" for col in colunas if col != "id"])
            valores = [row[col] for col in colunas if col != "id"]
            valores.append(row["id"])
            cursor.execute(f"UPDATE produtos SET {set_clause} WHERE id = ?", valores)

    conn.commit()
    conn.close()

# Exibir a tabela editável
st.subheader("📋 Produtos Cadastrados")
df = carregar_dados()
df_original = df.copy()

# Filtros
st.sidebar.header("🔎 Filtros")
tipos = df["tipo"].dropna().unique().tolist()
tipo_filtro = st.sidebar.multiselect("Tipo de Produto", tipos, default=tipos)
status_filtro = st.sidebar.selectbox("Status", ["Todos", "Ativos", "Inativos"])

# Aplicar filtros
df = df[df["tipo"].isin(tipo_filtro)]
if status_filtro == "Ativos":
    df = df[df["ativo"] == 1]
elif status_filtro == "Inativos":
    df = df[df["ativo"] == 0]

# Tradução para português da interface AgGrid
locale_pt = {
    "filterOoo": "Filtrar...",
    "equals": "Igual",
    "notEqual": "Diferente",
    "greaterThan": "Maior que",
    "greaterThanOrEqual": "Maior ou igual",
    "lessThan": "Menor que",
    "lessThanOrEqual": "Menor ou igual",
    "inRange": "Entre",
    "blank": "Em branco",
    "notBlank": "Preenchido",
    "contains": "Contém",
    "notContains": "Não contém",
    "startsWith": "Começa com",
    "endsWith": "Termina com",
    "andCondition": "E",
    "orCondition": "Ou",
    "noRowsToShow": "Nenhum dado disponível",
    "loadingOoo": "Carregando...",
    "applyFilter": "Aplicar filtro",
    "resetFilter": "Redefinir filtro",
    "clearFilter": "Limpar filtro",
    "textFilter": "Filtro de texto",
    "numberFilter": "Filtro numérico",
    "dateFilter": "Filtro de data",
    "columns": "Colunas",
    "filters": "Filtros",
    "rowGroupColumnsEmptyMessage": "Arraste colunas aqui para agrupar",
    "group": "Agrupar",
    "ungroup": "Desagrupar",
    "selectAll": "Selecionar tudo",
    "deselectAll": "Desmarcar tudo",
    "searchOoo": "Buscar...",
    "copy": "Copiar",
    "copyWithHeaders": "Copiar com cabeçalhos",
    "ctrlC": "Ctrl+C",
    "paste": "Colar",
    "ctrlV": "Ctrl+V",
    "export": "Exportar",
    "csvExport": "Exportar para CSV",
    "excelExport": "Exportar para Excel",
    "pinColumn": "Fixar Coluna",
    "noPin": "Sem fixação",
    "pinLeft": "Fixar à esquerda",
    "pinRight": "Fixar à direita",
    "autosizeThisColumn": "Ajustar esta coluna",
    "autosizeAllColumns": "Ajustar todas as colunas",
    "resetColumns": "Redefinir colunas",
    "menuFilter": "Filtro",
    "menuColumns": "Colunas",
    "menuExport": "Exportar",
    "menuFilterColumns": "Colunas com filtro",
    "showColumns": "Mostrar colunas",
    "toolPanel": "Painel de ferramentas",
    "rowGroup": "Grupo de linhas",
    "rowGroupColumnsEmptyMessage": "Arraste colunas aqui para agrupar"
}

# Configurar grade
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True, resizable=True, wrapText=True, autoHeight=True, minWidth=300)
gb.configure_selection("multiple", use_checkbox=True)
gb.configure_grid_options(localeText=locale_pt)

# Aplicar AgGrid com tema moderno e idioma
grid_response = AgGrid(
    df,
    gridOptions=gb.build(),
    height=700,
    width='100%',
    update_mode=GridUpdateMode.VALUE_CHANGED,
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    theme="alpine",
    localeText=locale_pt
)

df_editado = grid_response["data"]
selecionados = grid_response["selected_rows"]

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Salvar Tudo"):
        atualizar_registros_alterados(df_original, df_editado)
        st.success("Todas as alterações foram salvas com sucesso!")

with col2:
    if st.button("🛠 Aplicar a Selecionados"):
        if len(selecionados) > 0:
            st.warning("🔧 Essa função será programada para aplicar alterações em lote nos produtos selecionados.")
        else:
            st.error("Selecione ao menos um produto.")

st.markdown("---")
st.info("Você pode editar qualquer campo diretamente na tabela.")
# 🔙 Botão de retorno à Home do Estoque
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("🔙 Voltar para o Início do Estoque", url="../estoque_home")
