import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Comparador de Colunas", layout="wide")
st.title("Comparador de Colunas - Sistema vs B3")

# Caminhos dos arquivos
sistema_file = "/content/Sistema.xlsx"
b3_file = "/content/B3.xlsx"

def gerar_relatorio_comparacao(coluna_nome, iguais, diferentes, total):
    """Gera relatório automático para comparação de colunas"""
    percentual_iguais = (iguais / total) * 100 if total > 0 else 0
    
    relatorio = f"""
    **RELATÓRIO DE ANÁLISE - {coluna_nome.upper()}**
    
    **Estatísticas:**
    - Total de registros: {total}
    - Registros iguais: {iguais} ({percentual_iguais:.1f}%)
    - Registros diferentes: {diferentes} ({100-percentual_iguais:.1f}%)
    
    **Análise:**
    """
    
    if percentual_iguais >= 90:
        relatorio += "- Excelente correspondência (>90% iguais)"
    elif percentual_iguais >= 70:
        relatorio += "- Boa correspondência (70-90% iguais)"
    elif percentual_iguais >= 50:
        relatorio += "- Correspondência moderada (50-70% iguais)"
    else:
        relatorio += "- Baixa correspondência (<50% iguais)"
    
    if diferentes == 0:
        relatorio += "\n- Perfeita sincronização entre sistemas"
    elif diferentes <= total * 0.1:
        relatorio += "\n- Poucas divergências (<10%)"
    else:
        relatorio += "\n- Necessita verificação das divergências"
    
    return relatorio

def gerar_relatorio_subtracao(total_sis, total_b3, positivas_sis, negativas_sis, positivas_b3, negativas_b3):
    """Gera relatório automático para subtrações"""
    
    relatorio = f"""
    **RELATÓRIO DE ANÁLISE - SUBTRAÇÕES**
    
    **Sistema:**
    - Total de subtrações: {total_sis:,.2f}
    - Subtrações positivas: {positivas_sis} registros
    - Subtrações negativas: {negativas_sis} registros
    
    **B3:**
    - Total de subtrações: {total_b3:,.2f}
    - Subtrações positivas: {positivas_b3} registros
    - Subtrações negativas: {negativas_b3} registros
    
    **Insights:**
    """
    
    # Análise comparativa
    if total_sis > total_b3:
        relatorio += "- Sistema apresenta maior variação total que a B3\n"
    elif total_sis < total_b3:
        relatorio += "- B3 apresenta maior variação total que o Sistema\n"
    else:
        relatorio += "- Variações totais são iguais entre Sistema e B3\n"
    
    # Análise de tendências
    if positivas_sis > positivas_b3:
        relatorio += "- Sistema tem mais registros com aumento\n"
    elif positivas_sis < positivas_b3:
        relatorio += "- B3 tem mais registros com aumento\n"
    else:
        relatorio += "- Número de aumentos igual em ambos os sistemas\n"
    
    # Análise de consistência
    diferenca_percentual = abs(total_sis - total_b3) / max(abs(total_sis), abs(total_b3)) * 100
    if diferenca_percentual > 20:
        relatorio += f"- Diferença significativa entre sistemas ({diferenca_percentual:.1f}%)\n"
    else:
        relatorio += "- Sistemas relativamente consistentes\n"
    
    return relatorio

if os.path.exists(sistema_file) and os.path.exists(b3_file):
    # Carregar planilhas
    sistema = pd.read_excel(sistema_file)
    b3 = pd.read_excel(b3_file)
    
    st.success("Planilhas carregadas com sucesso")
    
    # Informações das planilhas
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sistema")
        st.write(f"Linhas: {sistema.shape[0]}, Colunas: {sistema.shape[1]}")
    
    with col2:
        st.subheader("B3")
        st.write(f"Linhas: {b3.shape[0]}, Colunas: {b3.shape[1]}")

    # SEÇÃO 1: SUBTRAÇÃO ENTRE QUANTIDADES
    st.header("Subtração entre Quantidades")
    st.write("Calcule a diferença entre quantidade inicial e atual")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Sistema")
        qtd_inicial_sis = st.selectbox("Quantidade Inicial:", sistema.columns, key="qtd_ini_sis")
        qtd_atual_sis = st.selectbox("Quantidade Atual:", sistema.columns, key="qtd_atual_sis")
    
    with col2:
        st.write("B3")
        qtd_inicial_b3 = st.selectbox("Quantidade Inicial:", b3.columns, key="qtd_ini_b3")
        qtd_atual_b3 = st.selectbox("Quantidade Atual:", b3.columns, key="qtd_atual_b3")
    
    if st.button("Calcular Subtrações"):
        # Cálculos para Sistema
        sistema_calc = sistema.copy()
        sistema_calc['DIFERENCA_SISTEMA'] = sistema_calc[qtd_atual_sis] - sistema_calc[qtd_inicial_sis]
        
        # Cálculos para B3
        b3_calc = b3.copy()
        b3_calc['DIFERENCA_B3'] = b3_calc[qtd_atual_b3] - b3_calc[qtd_inicial_b3]
        
        # Resultados combinados
        resultado_final = pd.DataFrame({
            'ID': sistema_calc.index,
            f'{qtd_inicial_sis}_Sistema': sistema_calc[qtd_inicial_sis],
            f'{qtd_atual_sis}_Sistema': sistema_calc[qtd_atual_sis],
            'Diferenca_Sistema': sistema_calc['DIFERENCA_SISTEMA'],
            f'{qtd_inicial_b3}_B3': b3_calc[qtd_inicial_b3],
            f'{qtd_atual_b3}_B3': b3_calc[qtd_atual_b3],
            'Diferenca_B3': b3_calc['DIFERENCA_B3']
        })
        
        # Exibir resultados
        col1, col2 = st.columns(2)
        with col1:
            st.write("Sistema - Diferenças")
            st.dataframe(sistema_calc[[qtd_inicial_sis, qtd_atual_sis, 'DIFERENCA_SISTEMA']].head(10))
            total_sis = sistema_calc['DIFERENCA_SISTEMA'].sum()
            st.write(f"Total Sistema: {total_sis:,.2f}")
        
        with col2:
            st.write("B3 - Diferenças")
            st.dataframe(b3_calc[[qtd_inicial_b3, qtd_atual_b3, 'DIFERENCA_B3']].head(10))
            total_b3 = b3_calc['DIFERENCA_B3'].sum()
            st.write(f"Total B3: {total_b3:,.2f}")
        
        # Download
        csv_data = resultado_final.to_csv(index=False)
        st.download_button("Baixar Resultados CSV", data=csv_data, file_name="subtracao_resultados.csv")
        
        # Relatório automático da IA para subtrações
        st.subheader("Relatório de Análise - Subtrações")
        positivas_sis = len(sistema_calc[sistema_calc['DIFERENCA_SISTEMA'] > 0])
        negativas_sis = len(sistema_calc[sistema_calc['DIFERENCA_SISTEMA'] < 0])
        positivas_b3 = len(b3_calc[b3_calc['DIFERENCA_B3'] > 0])
        negativas_b3 = len(b3_calc[b3_calc['DIFERENCA_B3'] < 0])
        
        relatorio_subtracao = gerar_relatorio_subtracao(
            total_sis, total_b3, positivas_sis, negativas_sis, positivas_b3, negativas_b3
        )
        st.write(relatorio_subtracao)

    # SEÇÃO 2: COMPARAÇÃO DE COLUNAS COM NOMES DIFERENTES
    st.header("Comparação de Colunas com Nomes Diferentes")
    
    col1, col2 = st.columns(2)
    with col1:
        col_sistema = st.selectbox("Coluna do Sistema:", sistema.columns, key="col_sis")
    with col2:
        col_b3 = st.selectbox("Coluna da B3:", b3.columns, key="col_b3")
    
    if st.button("Comparar Colunas Selecionadas"):
        if col_sistema and col_b3:
            # Preparar dados para comparação
            dados_sistema = sistema[col_sistema].dropna().reset_index(drop=True)
            dados_b3 = b3[col_b3].dropna().reset_index(drop=True)
            
            # Criar comparação
            tamanho_max = max(len(dados_sistema), len(dados_b3))
            comparacao_df = pd.DataFrame({
                f'{col_sistema} (Sistema)': dados_sistema.reindex(range(tamanho_max)),
                f'{col_b3} (B3)': dados_b3.reindex(range(tamanho_max)),
                'Status': ['Igual' if str(a) == str(b) else 'Diferente' 
                          for a, b in zip(dados_sistema.reindex(range(tamanho_max)), 
                                        dados_b3.reindex(range(tamanho_max)))]
            })
            
            # Estatísticas
            iguais = (comparacao_df['Status'] == 'Igual').sum()
            diferentes = (comparacao_df['Status'] == 'Diferente').sum()
            total = len(comparacao_df)
            
            # Exibir resultados
            st.subheader(f"Comparação: {col_sistema} vs {col_b3}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Iguais", iguais)
            col2.metric("Diferentes", diferentes)
            col3.metric("Total", total)
            
            st.dataframe(comparacao_df)
            
            # Relatório da IA
            st.subheader("Relatório de Análise")
            relatorio_comparacao = gerar_relatorio_comparacao(
                f"{col_sistema} vs {col_b3}", iguais, diferentes, total
            )
            st.write(relatorio_comparacao)
            
            # Download
            csv_comparacao = comparacao_df.to_csv(index=False)
            st.download_button(
                "Baixar Comparação CSV", 
                data=csv_comparacao, 
                file_name=f"comparacao_{col_sistema}_{col_b3}.csv"
            )

    # SEÇÃO 3: COMPARAÇÃO AUTOMÁTICA DE COLUNAS COMUNS
    st.header("Comparação Automática de Colunas Comuns")
    
    colunas_comuns = [col for col in sistema.columns if col in b3.columns]
    st.write(f"Colunas comuns encontradas: {len(colunas_comuns)}")
    
    for coluna in colunas_comuns:
        if st.button(f"Comparar Coluna: {coluna}"):
            # Preparar dados
            dados_sistema = sistema[coluna].dropna().reset_index(drop=True)
            dados_b3 = b3[coluna].dropna().reset_index(drop=True)
            
            # Criar comparação
            tamanho_max = max(len(dados_sistema), len(dados_b3))
            comparacao_df = pd.DataFrame({
                f'{coluna} (Sistema)': dados_sistema.reindex(range(tamanho_max)),
                f'{coluna} (B3)': dados_b3.reindex(range(tamanho_max)),
                'Status': ['Igual' if str(a) == str(b) else 'Diferente' 
                          for a, b in zip(dados_sistema.reindex(range(tamanho_max)), 
                                        dados_b3.reindex(range(tamanho_max)))]
            })
            
            # Estatísticas
            iguais = (comparacao_df['Status'] == 'Igual').sum()
            diferentes = (comparacao_df['Status'] == 'Diferente').sum()
            total = len(comparacao_df)
            
            # Exibir resultados
            st.subheader(f"Comparação da Coluna: {coluna}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Iguais", iguais)
            col2.metric("Diferentes", diferentes)
            col3.metric("Total", total)
            
            st.dataframe(comparacao_df)
            
            # Relatório da IA
            st.subheader("Relatório de Análise")
            relatorio_comparacao = gerar_relatorio_comparacao(coluna, iguais, diferentes, total)
            st.write(relatorio_comparacao)
            
            # Download
            csv_comparacao = comparacao_df.to_csv(index=False)
            st.download_button(
                "Baixar Comparação CSV", 
                data=csv_comparacao, 
                file_name=f"comparacao_{coluna}.csv"
            )

else:
    st.error("Arquivos não encontrados. Verifique se os arquivos estão em /content/")