import streamlit as st
import os
import sys

# 🛠 Ajustar caminho para importar do src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from importar_produtos_xml import importar_produtos_xml

# Configuração da página
st.set_page_config(page_title="📥 Importar Produtos da NF-e", layout="centered")
st.title("📥 Importar Produtos a partir do XML da NF-e")

st.markdown("Cole abaixo o conteúdo **completo** de um arquivo XML de uma NF-e:")

# Campo para colar o XML
xml_conteudo = st.text_area("📄 Conteúdo do XML", height=300, placeholder="Cole aqui o XML da nota...")

# Criar pasta temporária
temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp"))
os.makedirs(temp_dir, exist_ok=True)

# Botão para importar
if st.button("🚀 Importar Produtos do XML"):
    if not xml_conteudo.strip().startswith("<"):
        st.error("❌ O conteúdo colado não parece ser um XML válido.")
    else:
        caminho_temp = os.path.join(temp_dir, "nfe_temp.xml")
        with open(caminho_temp, "w", encoding="utf-8") as f:
            f.write(xml_conteudo)

        try:
            novos, atualizados, aumento = importar_produtos_xml(caminho_temp)

            st.success(f"✅ Produtos novos cadastrados: {len(novos)}")
            st.warning(f"🔁 Produtos atualizados: {len(atualizados)}")
            st.error(f"⬆️ Produtos com aumento de custo: {len(aumento)}")

            if novos:
                st.markdown("### 🆕 Produtos Cadastrados:")
                for nome in novos:
                    st.write(f"🟢 {nome}")

            if atualizados:
                st.markdown("### 🔁 Produtos Atualizados:")
                for nome in atualizados:
                    st.write(f"🟡 {nome}")

            if aumento:
                st.markdown("### ⬆️ Produtos com Custo Aumentado:")
                for nome in aumento:
                    st.write(f"🔴 {nome}")

        except Exception as e:
            st.error(f"❌ Erro ao processar XML: {str(e)}")
