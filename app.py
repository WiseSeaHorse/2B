import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Comparador de Planilhas", layout="wide")
st.title("📊 Comparador de Planilhas - Sistema vs B3")

# Caminhos dos arquivos no Colab
sistema_file = "/content/Sistema.xlsx"
b3_file = "/content/B3.xlsx"

# Verificar se os arquivos existem
if os.path.exists(sistema_file) and os.path.exists(b3_file):
    try:
        # Carregar as planilhas
        sistema = pd.read_excel(sistema_file)
        b3 = pd.read_excel(b3_file)
        st.success("✅ Planilhas carregadas automaticamente!")

        # Mostrar informações das planilhas
        st.write(f"**Sistema:** {sistema.shape[0]} linhas, {sistema.shape[1]} colunas")
        st.write(f"**B3:** {b3.shape[0]} linhas, {b3.shape[1]} colunas")

        # Padronizar colunas
        sistema.columns = sistema.columns.str.strip().str.lower()
        b3.columns = b3.columns.str.strip().str.lower()

        # Mostrar colunas disponíveis
        st.write("**Colunas do Sistema:**", list(sistema.columns))
        st.write("**Colunas da B3:**", list(b3.columns))

        # Escolher coluna-chave
        colunas_comuns = [col for col in sistema.columns if col in b3.columns]
        if colunas_comuns:
            chave = st.selectbox("🔑 Escolha a coluna de identificação", colunas_comuns)

            # Merge das planilhas
            df = pd.merge(sistema, b3, on=chave, how="outer", suffixes=("_sis", "_b3"), indicator=True)

            # Comparar campos comuns (excluindo a chave)
            campos_comuns = [c for c in sistema.columns if c in b3.columns and c != chave]

            if campos_comuns:
                for campo in campos_comuns:
                    df[f"{campo}_status"] = df.apply(
                        lambda x: "OK" if pd.notna(x.get(f"{campo}_sis")) and pd.notna(x.get(f"{campo}_b3")) and x[f"{campo}_sis"] == x[f"{campo}_b3"]
                        else "Divergente", axis=1
                    )

                # Status geral
                colunas_status = [f"{c}_status" for c in campos_comuns]
                df["Status_Geral"] = df[colunas_status].apply(
                    lambda x: "OK" if all(v == "OK" for v in x) else "Divergente", axis=1
                )

                # Resumo
                st.subheader("📈 Resumo da Conferência")
                resumo = df["Status_Geral"].value_counts().reset_index()
                resumo.columns = ["Status", "Quantidade"]
                st.dataframe(resumo, use_container_width=True)

                # Filtro interativo
                filtro = st.radio("Filtrar por status:", ["Todos", "OK", "Divergente"])
                if filtro != "Todos":
                    df_filtrado = df[df["Status_Geral"] == filtro]
                else:
                    df_filtrado = df

                # Estilo para destacar divergências
                def highlight_divergente(val):
                    if val == "Divergente":
                        return "color: red; font-weight: bold"
                    elif val == "OK":
                        return "color: green; font-weight: bold"
                    else:
                        return ""

                st.subheader("📋 Resultado da Comparação")

                # Preparar colunas para exibição
                colunas_exibicao = [chave] + colunas_status + ["Status_Geral"]
                for campo in campos_comuns:
                    colunas_exibicao.extend([f"{campo}_sis", f"{campo}_b3"])

                # Exibir dataframe com estilo
                styled_df = df_filtrado[colunas_exibicao].style.applymap(
                    highlight_divergente,
                    subset=colunas_status + ["Status_Geral"]
                )

                st.dataframe(styled_df, use_container_width=True)

                # Download CSV
                csv = df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "💾 Baixar Resultado em CSV",
                    data=csv,
                    file_name="comparacao_resultado.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ Não foram encontrados campos comuns para comparação (além da coluna-chave).")
        else:
            st.error("❌ Não foram encontradas colunas comuns entre as planilhas para usar como chave.")

    except Exception as e:
        st.error(f"❌ Erro ao processar as planilhas: {str(e)}")
else:
    st.error("❌ Arquivos não encontrados!")
    st.write("Certifique-se de que os arquivos estão no caminho correto:")
    st.write(f"- Sistema: {sistema_file}")
    st.write(f"- B3: {b3_file}")

    # Listar arquivos disponíveis no diretório
    st.write("**Arquivos disponíveis no /content:**")
    try:
        arquivos = os.listdir("/content")
        for arquivo in arquivos:
            st.write(f"- {arquivo}")
    except:
        st.write("Não foi possível listar os arquivos do diretório.")
