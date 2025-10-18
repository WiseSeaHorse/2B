import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Comparador de Planilhas", layout="wide")
st.title("Comparador de Planilhas - Sistema vs B3")

# Feriados fixos
feriados = ['01-01', '21-04', '01-05', '07-09', '12-10', '02-11', '15-11', '25-12']

def carregar_planilha(uploader, nome):
    try:
        if uploader is not None:
            df = pd.read_excel(uploader)
            st.success(f"{nome}: {df.shape[0]} linhas, {df.shape[1]} colunas")
            return df
        return None
    except Exception as e:
        st.error(f"Erro em {nome}: {str(e)}")
        return None

def verificar_data_util(data):
    if pd.isna(data):
        return False, "Data inválida"
    
    try:
        if isinstance(data, str):
            data = pd.to_datetime(data, errors='coerce')
            if pd.isna(data):
                return False, "Data inválida"
        
        if data.weekday() >= 5:
            return False, "Final de semana"
        
        data_str = data.strftime('%d-%m')
        if data_str in feriados:
            return False, "Feriado"
        
        return True, "Dia útil"
    except:
        return False, "Erro data"

def analisar_datas(sistema, b3, col_data_sis, col_data_b3):
    resultados = []
    
    for idx, (data_sis, data_b3) in enumerate(zip(sistema[col_data_sis], b3[col_data_b3])):
        util_sis, motivo_sis = verificar_data_util(data_sis)
        util_b3, motivo_b3 = verificar_data_util(data_b3)
        
        status = "OK"
        if not util_sis and not util_b3:
            status = "Ambas não úteis"
        elif not util_sis:
            status = f"Sistema: {motivo_sis}"
        elif not util_b3:
            status = f"B3: {motivo_b3}"
        
        resultados.append({
            'ID': idx,
            'Data_Sistema': data_sis,
            'Data_B3': data_b3,
            'Status': status
        })
    
    return pd.DataFrame(resultados)

def comparar_colunas(sistema, b3, col_sis, col_b3):
    try:
        dados_sis = sistema[col_sis].dropna().reset_index(drop=True)
        dados_b3 = b3[col_b3].dropna().reset_index(drop=True)
        
        max_len = max(len(dados_sis), len(dados_b3))
        comparacao = pd.DataFrame({
            f'{col_sis} (Sistema)': dados_sis.reindex(range(max_len)),
            f'{col_b3} (B3)': dados_b3.reindex(range(max_len)),
            'Status': ['Igual' if str(a) == str(b) else 'Diferente' 
                      for a, b in zip(dados_sis.reindex(range(max_len)), 
                                    dados_b3.reindex(range(max_len)))]
        })
        
        iguais = (comparacao['Status'] == 'Igual').sum()
        return comparacao, iguais, len(comparacao)
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return None, 0, 0

# Upload das planilhas
st.header("Upload das Planilhas")
col1, col2 = st.columns(2)

with col1:
    sis_upload = st.file_uploader("Planilha do Sistema", type=['xlsx', 'xls'])

with col2:
    b3_upload = st.file_uploader("Planilha da B3", type=['xlsx', 'xls'])

sistema = carregar_planilha(sis_upload, "Sistema")
b3 = carregar_planilha(b3_upload, "B3")

if sistema is not None and b3 is not None:
    
    # Análise de datas
    st.header("Análise de Datas")
    
    col1, col2 = st.columns(2)
    with col1:
        col_data_sis = st.selectbox("Data Sistema:", sistema.columns, key="data_sis")
    with col2:
        col_data_b3 = st.selectbox("Data B3:", b3.columns, key="data_b3")
    
    if st.button("Verificar Datas"):
        try:
            df_datas = analisar_datas(sistema, b3, col_data_sis, col_data_b3)
            st.dataframe(df_datas, height=400)
            
            problemas = len(df_datas[df_datas['Status'] != 'OK'])
            st.write(f"Registros com problemas: {problemas} de {len(df_datas)}")
            
            csv_datas = df_datas.to_csv(index=False)
            st.download_button("Baixar Análise Datas", data=csv_datas, 
                             file_name="analise_datas.csv")
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")

    # Subtração entre quantidades
    st.header("Subtração entre Quantidades")
    
    col1, col2 = st.columns(2)
    with col1:
        qtd_ini_sis = st.selectbox("Qtd Inicial Sistema:", sistema.columns, key="ini_sis")
        qtd_atual_sis = st.selectbox("Qtd Atual Sistema:", sistema.columns, key="atual_sis")
    
    with col2:
        qtd_ini_b3 = st.selectbox("Qtd Inicial B3:", b3.columns, key="ini_b3")
        qtd_atual_b3 = st.selectbox("Qtd Atual B3:", b3.columns, key="atual_b3")
    
    if st.button("Calcular Subtração"):
        try:
            sis_calc = sistema.copy()
            sis_calc['DIFERENCA_SISTEMA'] = sis_calc[qtd_atual_sis] - sis_calc[qtd_ini_sis]
            
            b3_calc = b3.copy()
            b3_calc['DIFERENCA_B3'] = b3_calc[qtd_atual_b3] - b3_calc[qtd_ini_b3]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("Sistema")
                st.dataframe(sis_calc[[qtd_ini_sis, qtd_atual_sis, 'DIFERENCA_SISTEMA']], height=400)
                st.write(f"Total: {sis_calc['DIFERENCA_SISTEMA'].sum():,.2f}")
            
            with col2:
                st.write("B3")
                st.dataframe(b3_calc[[qtd_ini_b3, qtd_atual_b3, 'DIFERENCA_B3']], height=400)
                st.write(f"Total: {b3_calc['DIFERENCA_B3'].sum():,.2f}")
            
            resultado = pd.DataFrame({
                'ID': sis_calc.index,
                f'{qtd_ini_sis}_Sistema': sis_calc[qtd_ini_sis],
                f'{qtd_atual_sis}_Sistema': sis_calc[qtd_atual_sis],
                'Diferenca_Sistema': sis_calc['DIFERENCA_SISTEMA'],
                f'{qtd_ini_b3}_B3': b3_calc[qtd_ini_b3],
                f'{qtd_atual_b3}_B3': b3_calc[qtd_atual_b3],
                'Diferenca_B3': b3_calc['DIFERENCA_B3']
            })
            
            csv = resultado.to_csv(index=False)
            st.download_button("Baixar Subtração", data=csv, file_name="subtracao.csv")
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")

    # Comparação de colunas
    st.header("Comparação de Colunas")
    
    col1, col2 = st.columns(2)
    with col1:
        col_sis = st.selectbox("Coluna Sistema:", sistema.columns, key="col_sis")
    with col2:
        col_b3 = st.selectbox("Coluna B3:", b3.columns, key="col_b3")
    
    if st.button("Comparar Colunas"):
        if col_sis and col_b3:
            comparacao, iguais, total = comparar_colunas(sistema, b3, col_sis, col_b3)
            
            if comparacao is not None:
                col1, col2, col3 = st.columns(3)
                col1.metric("Iguais", iguais)
                col2.metric("Diferentes", total - iguais)
                col3.metric("Total", total)
                
                st.dataframe(comparacao, height=400)
                
                csv_comp = comparacao.to_csv(index=False)
                st.download_button("Baixar Comparação", data=csv_comp, 
                                 file_name=f"comparacao_{col_sis}_{col_b3}.csv")

    # Comparação automática
    st.header("Comparação Automática")
    
    colunas_comuns = [col for col in sistema.columns if col in b3.columns]
    st.write(f"Colunas comuns: {len(colunas_comuns)}")
    
    for coluna in colunas_comuns:
        if st.button(f"Comparar: {coluna}", key=f"auto_{coluna}"):
            comparacao, iguais, total = comparar_colunas(sistema, b3, coluna, coluna)
            
            if comparacao is not None:
                col1, col2, col3 = st.columns(3)
                col1.metric("Iguais", iguais)
                col2.metric("Diferentes", total - iguais)
                col3.metric("Total", total)
                
                st.dataframe(comparacao.head(15), height=400)
                
                csv_auto = comparacao.to_csv(index=False)
                st.download_button("Baixar Comparação", data=csv_auto,
                                 file_name=f"comparacao_{coluna}.csv")

else:
    st.info("Faça upload das planilhas para começar")