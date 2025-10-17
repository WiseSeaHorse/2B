Comparador de Planilhas - Sistema vs B3
📋 Descrição
Este é um aplicativo web desenvolvido em Streamlit que permite comparar planilhas do Sistema com as da B3, identificando divergências, calculando diferenças entre quantidades e gerando relatórios automáticos de análise.

🚀 Funcionalidades
1. Subtração entre Quantidades
Calcula a diferença entre quantidade inicial e atual

Compara resultados entre Sistema e B3

Gera relatório automático com insights

2. Comparação de Colunas com Nomes Diferentes
Permite comparar colunas que não possuem o mesmo nome

Identifica registros iguais e diferentes

Relatório de análise da correspondência

3. Comparação Automática de Colunas Comuns
Detecta automaticamente colunas com mesmo nome

Compara valores linha por linha

Gera estatísticas de correspondência

🛠️ Tecnologias Utilizadas
Python 3.8+

Streamlit - Interface web

Pandas - Manipulação de dados

OpenPyXL - Leitura de arquivos Excel

📁 Estrutura do Projeto
text
comparador-planilhas/
│
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências do projeto
├── Sistema.xlsx          # Planilha do Sistema (exemplo)
├── B3.xlsx              # Planilha da B3 (exemplo)
└── README.md            # Este arquivo
🔧 Instalação e Uso
Pré-requisitos
Python 3.8 ou superior

Pip (gerenciador de pacotes do Python)

Instalação
Clone o repositório:

bash
git clone https://github.com/seu-usuario/comparador-planilhas.git
cd comparador-planilhas
Instale as dependências:

bash
pip install -r requirements.txt
Execute a aplicação:

bash
streamlit run app.py
Para uso no Google Colab
python
!pip install streamlit pyngrok pandas openpyxl
!wget -O Sistema.xlsx "URL_DA_PLANILHA_SISTEMA"
!wget -O B3.xlsx "URL_DA_PLANILHA_B3"
!streamlit run app.py --server.port 8501 --server.headless true
📊 Como Usar
1. Preparação dos Arquivos
Coloque as planilhas Sistema.xlsx e B3.xlsx no diretório do projeto

Certifique-se que as colunas estejam nomeadas corretamente

2. Subtração entre Quantidades
Selecione as colunas de quantidade inicial e atual para ambas as planilhas

Clique em "Calcular Subtrações"

Visualize os resultados e baixe o CSV

3. Comparação de Colunas
Use a seção de comparação customizada para colunas com nomes diferentes

Ou use a comparação automática para colunas com mesmo nome

Analise os relatórios gerados automaticamente

🎯 Exemplos de Uso
Caso 1: Comparação de Códigos
python
# Compara a coluna "codigo" do Sistema com "codigo" da B3
# Relatório mostrará percentual de correspondência
Caso 2: Cálculo de Variações
python
# Calcula diferença entre "qtd_inicial" e "qtd_atual"
# Identifica tendências de aumento/diminuição
Caso 3: Auditoria de Dados
python
# Compara múltiplas colunas automaticamente
# Gera relatório consolidado da qualidade dos dados
📈 Saídas e Relatórios
Relatório de Subtrações
Totais de variação por sistema

Quantidade de registros positivos/negativos

Análise comparativa entre Sistemas

Insights automáticos

Relatório de Comparação
Percentual de correspondência

Classificação da qualidade dos dados

Recomendações para ajustes

Estatísticas detalhadas

🔍 Exemplo de Análise Gerada
text
RELATÓRIO DE ANÁLISE - CODIGO_EXTERNO

Estatísticas:
- Total de registros: 150
- Registros iguais: 135 (90.0%)
- Registros diferentes: 15 (10.0%)

Análise:
- Excelente correspondência (>90% iguais)
- Poucas divergências (<10%)
🚨 Tratamento de Erros
Verificação de existência dos arquivos

Validação de colunas selecionadas

Tratamento de dados ausentes

Mensagens de erro descritivas

📝 Personalização
Adicionar Novas Análises
python
def nova_analise(dados_sistema, dados_b3):
    # Implemente sua análise personalizada
    return resultado
Modificar Critérios de Relatório
python
# No arquivo app.py, modifique as funções:
# - gerar_relatorio_comparacao()
# - gerar_relatorio_subtracao()
