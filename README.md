## **Explicação do Código - Comparador de Planilhas**

### **Visão Geral**
Aplicativo Streamlit para comparar planilhas do Sistema vs B3, verificando dados, datas e calculando diferenças.

### **Funções Principais**

#### **1. `carregar_planilha(uploader, nome)`**
- **Função**: Carrega arquivos Excel
- **Entrada**: Arquivo uploader e nome para identificação
- **Saída**: DataFrame pandas ou None em caso de erro
- **Propósito**: Valida e carrega as planilhas com tratamento de erro

#### **2. `verificar_data_util(data)`**
- **Função**: Verifica se uma data é dia útil
- **Verifica**: 
  - Finais de semana (sábado e domingo)
  - Feriados nacionais brasileiros
  - Datas inválidas
- **Saída**: (True/False, motivo)

#### **3. `analisar_datas(sistema, b3, col_data_sis, col_data_b3)`**
- **Função**: Compara datas entre as duas planilhas
- **Identifica**: 
  - Emissões em feriados/finais de semana
  - Discrepâncias entre sistemas
- **Saída**: DataFrame com análise de cada registro

#### **4. `comparar_colunas(sistema, b3, col_sis, col_b3)`**
- **Função**: Compara valores de colunas correspondentes
- **Processo**: 
  - Remove valores vazios
  - Alinha por índice
  - Marca como "Igual" ou "Diferente"
- **Saída**: DataFrame comparativo com estatísticas

### **Seções do Aplicativo**

#### **1. Upload de Planilhas**
- Interface para carregar Sistema.xlsx e B3.xlsx
- Validação de formato e tratamento de erro

#### **2. Análise de Datas**
- Seleciona colunas de data de cada planilha
- Verifica se emissões foram em dias úteis
- Identifica possíveis causas de divergência

#### **3. Subtração entre Quantidades**
- Calcula diferença entre quantidade inicial e atual
- Mostra resultados completos de ambos sistemas
- Gera CSV com totais e diferenças

#### **4. Comparação de Colunas**
- Compara colunas específicas entre sistemas
- Mostra estatísticas de correspondência
- Permite download dos resultados

#### **5. Comparação Automática**
- Detecta colunas com mesmo nome automaticamente
- Botão individual para cada coluna comum
- Download específico por coluna

### **Fluxo de Uso**

1. **Upload** → Carrega Sistema.xlsx e B3.xlsx
2. **Análise** → Verifica datas problemáticas
3. **Cálculo** → Subtrai quantidades iniciais/atuais  
4. **Comparação** → Analisa colunas específicas
5. **Download** → Exporta resultados em CSV
