import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Verificador de Movimentações", layout="wide")
st.title("Verificador de Movimentações - Sistema vs B3")

def calcular_movimentacao(df, col_inicial, col_atual, nome_sistema):
    """Calcula movimentação entre colunas"""
    df_calc = df.copy()
    df_calc[f'MOVIMENTAÇÃO_{nome_sistema}'] = df_calc[col_atual] - df_calc[col_inicial]
    return df_calc

def comparar_movimentacoes(sistema_df, b3_df, col_id, col_ini_sis, col_atual_sis, col_ini_b3, col_atual_b3):
    """Compara movimentações entre Sistema e B3"""
    
    resultados = {
        'mov_sistema_sem_b3': [],
        'mov_b3_sem_sistema': [], 
        'mov_conciliadas': [],
        'estatisticas': {}
    }
    
    # Calcular movimentações
    sistema_com_mov = calcular_movimentacao(sistema_df, col_ini_sis, col_atual_sis, 'SISTEMA')
    b3_com_mov = calcular_movimentacao(b3_df, col_ini_b3, col_atual_b3, 'B3')
    
    # Filtrar apenas registros com movimentação
    sistema_com_movimento = sistema_com_mov[sistema_com_mov['MOVIMENTAÇÃO_SISTEMA'] != 0].copy()
    b3_com_movimento = b3_com_mov[b3_com_mov['MOVIMENTAÇÃO_B3'] != 0].copy()
    
    # Verificar movimentações do Sistema na B3
    for _, linha_sis in sistema_com_movimento.iterrows():
        mov_sis = linha_sis['MOVIMENTAÇÃO_SISTEMA']
        id_sis = linha_sis[col_id]
        
        # Buscar correspondente na B3
        correspondente_b3 = b3_com_movimento[
            (b3_com_movimento[col_id] == id_sis) & 
            (abs(b3_com_movimento['MOVIMENTAÇÃO_B3'] - mov_sis) < 0.01)
        ]
        
        if len(correspondente_b3) == 0:
            resultados['mov_sistema_sem_b3'].append({
                'ID': id_sis,
                'MOVIMENTAÇÃO_SISTEMA': mov_sis,
                'QTD_INICIAL_SIS': linha_sis[col_ini_sis],
                'QTD_ATUAL_SIS': linha_sis[col_atual_sis],
                'STATUS': 'Não encontrada na B3'
            })
        else:
            linha_b3 = correspondente_b3.iloc[0]
            resultados['mov_conciliadas'].append({
                'ID': id_sis,
                'MOVIMENTAÇÃO_SISTEMA': mov_sis,
                'MOVIMENTAÇÃO_B3': linha_b3['MOVIMENTAÇÃO_B3'],
                'QTD_INICIAL_SIS': linha_sis[col_ini_sis],
                'QTD_ATUAL_SIS': linha_sis[col_atual_sis],
                'QTD_INICIAL_B3': linha_b3[col_ini_b3],
                'QTD_ATUAL_B3': linha_b3[col_atual_b3],
                'STATUS': 'Conciliada'
            })
    
    # Verificar movimentações da B3 no Sistema
    for _, linha_b3 in b3_com_movimento.iterrows():
        mov_b3 = linha_b3['MOVIMENTAÇÃO_B3']
        id_b3 = linha_b3[col_id]
        
        correspondente_sis = sistema_com_movimento[
            (sistema_com_movimento[col_id] == id_b3) & 
            (abs(sistema_com_movimento['MOVIMENTAÇÃO_SISTEMA'] - mov_b3) < 0.01)
        ]
        
        if len(correspondente_sis) == 0:
            resultados['mov_b3_sem_sistema'].append({
                'ID': id_b3,
                'MOVIMENTAÇÃO_B3': mov_b3,
                'QTD_INICIAL_B3': linha_b3[col_ini_b3],
                'QTD_ATUAL_B3': linha_b3[col_atual_b3],
                'STATUS': 'Não encontrada no Sistema'
            })
    
    # Estatísticas
    total_mov_sistema = len(sistema_com_movimento)
    total_mov_b3 = len(b3_com_movimento)
    mov_conciliadas = len(resultados['mov_conciliadas'])
    
    resultados['estatisticas'] = {
        'mov_sistema': total_mov_sistema,
        'mov_b3': total_mov_b3,
        'conciliadas': mov_conciliadas,
        'sistema_sem_b3': len(resultados['mov_sistema_sem_b3']),
        'b3_sem_sistema': len(resultados['mov_b3_sem_sistema'])
    }
    
    return resultados

# Interface principal
st.header("Upload dos Arquivos")

col1, col2 = st.columns(2)

with col1:
    upload_sistema = st.file_uploader("Planilha do Sistema", type=['xlsx', 'csv'])

with col2:
    upload_b3 = st.file_uploader("Planilha da B3", type=['xlsx', 'csv'])

if upload_sistema and upload_b3:
    # Carregar dados
    sistema_df = pd.read_excel(upload_sistema) if upload_sistema.name.endswith('.xlsx') else pd.read_csv(upload_sistema)
    b3_df = pd.read_excel(upload_b3) if upload_b3.name.endswith('.xlsx') else pd.read_csv(upload_b3)
    
    st.header("Configurar Colunas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sistema")
        col_id_sis = st.selectbox("Coluna de Identificação:", sistema_df.columns, key="id_sis")
        col_ini_sis = st.selectbox("Quantidade Inicial:", sistema_df.columns, key="ini_sis")
        col_atual_sis = st.selectbox("Quantidade Atual:", sistema_df.columns, key="atual_sis")
    
    with col2:
        st.subheader("B3")
        col_id_b3 = st.selectbox("Coluna de Identificação:", b3_df.columns, key="id_b3")
        col_ini_b3 = st.selectbox("Quantidade Inicial:", b3_df.columns, key="ini_b3")
        col_atual_b3 = st.selectbox("Quantidade Atual:", b3_df.columns, key="atual_b3")
    
    if st.button("🔍 Verificar Movimentações", type="primary", use_container_width=True):
        with st.spinner("Analisando movimentações..."):
            resultados = comparar_movimentacoes(
                sistema_df, b3_df, col_id_sis, col_ini_sis, col_atual_sis, col_ini_b3, col_atual_b3
            )
            
            # Resultados
            st.header("Resultados")
            
            stats = resultados['estatisticas']
            col1, col2, col3, col4, col5 = st.columns(5)
            
            col1.metric("Sistema", stats['mov_sistema'])
            col2.metric("B3", stats['mov_b3'])
            col3.metric("✅ Conciliadas", stats['conciliadas'])
            col4.metric("❌ Sistema s/B3", stats['sistema_sem_b3'])
            col5.metric("❌ B3 s/Sistema", stats['b3_sem_sistema'])
            
            # Alertas
            if stats['sistema_sem_b3'] > 0:
                st.error(f"{stats['sistema_sem_b3']} movimentações do Sistema não encontradas na B3")
            
            if stats['b3_sem_sistema'] > 0:
                st.warning(f"{stats['b3_sem_sistema']} movimentações da B3 não encontradas no Sistema")
            
            # Detalhes das divergências
            if resultados['mov_sistema_sem_b3']:
                st.subheader("Movimentações do Sistema sem B3")
                df_problemas = pd.DataFrame(resultados['mov_sistema_sem_b3'])
                st.dataframe(df_problemas, use_container_width=True)
                
                st.download_button(
                    "💾 Baixar Detalhes",
                    data=df_problemas.to_csv(index=False),
                    file_name="movimentações_sistema_sem_b3.csv",
                    key="download_sistema_sem_b3"
                )
            
            if resultados['mov_b3_sem_sistema']:
                st.subheader("Movimentações da B3 sem Sistema")
                df_problemas = pd.DataFrame(resultados['mov_b3_sem_sistema'])
                st.dataframe(df_problemas, use_container_width=True)
                
                st.download_button(
                    "💾 Baixar Detalhes",
                    data=df_problemas.to_csv(index=False),
                    file_name="movimentações_b3_sem_sistema.csv",
                    key="download_b3_sem_sistema"
                )
            
            # Movimentações conciliadas - removi o checkbox
            if resultados['mov_conciliadas']:
                st.subheader("Movimentações Conciliadas")
                st.success(f"{stats['conciliadas']} movimentações conciliadas com sucesso!")
                
                df_conciliadas = pd.DataFrame(resultados['mov_conciliadas'])
                st.dataframe(df_conciliadas, use_container_width=True)
                
                st.download_button(
                    "💾 Baixar Movimentações Conciliadas",
                    data=df_conciliadas.to_csv(index=False),
                    file_name="movimentações_conciliadas.csv",
                    key="download_conciliadas"
                )
            else:
                st.info("Nenhuma movimentação conciliada encontrada")

else:
    st.info("""
    👋 **Bem-vindo ao Verificador de Movimentações!**
    
    **O que este sistema faz:**
    - Compara as movimentações de quantidade entre Sistema e B3
    - Identifica movimentações que existem em um sistema mas não no outro
    - Ajuda a encontrar erros de registro e sincronização
    
    **Como usar:**
    1. Faça upload das planilhas do Sistema e B3
    2. Configure quais colunas usar para comparação  
    3. Clique em "Verificar Movimentações"
    4. Analise os resultados e baixe os relatórios
    
    """)
