# Verificador de Movimentações - Sistema vs B3

Sistema web para comparar automaticamente movimentações entre sistema interno e B3. Detecta divergências onde registros existem em um sistema mas não no outro.
<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/10512e3a-21fc-4eaf-849c-9ebd79ca3d06" />
*Interface intuitiva para upload e configuração*

## Funcionalidades

- ** Comparação Automática** - Cruza movimentações por ID
- ** Dashboard Visual** - Métricas em tempo real
- ** Exportação CSV** - Download dos resultados
<img width="1919" height="894" alt="image" src="https://github.com/user-attachments/assets/e081b0ab-fb3c-4690-8fa5-1f99100eaa4b" />
*Dashboard*

## Como Usar

### 1. Upload das Planilhas
```python
# Sistema precisa ter:
# - Coluna de ID (código do cliente)
# - Colunas de quantidade inicial e atual
```
### 2. Configurar Colunas
Selecione as colunas para comparação em cada sistema.
<img width="1916" height="899" alt="image" src="https://github.com/user-attachments/assets/a13323b3-e550-407a-95aa-fb1786255b21" />
*Seleção intuitiva das colunas*

### 3. Analisar Resultados
O sistema gera três categorias:

| Tipo | Descrição | Gravidade |
|------|-----------|-----------|
| Conciliadas | Movimentações em ambos sistemas | - |
| Sistema s/B3 | Só existe no sistema interno | Alta |
| B3 s/Sistema | Só existe na B3 | Alta |

<img width="1777" height="554" alt="image" src="https://github.com/user-attachments/assets/d1ae014d-d722-4f84-82c1-26dd9225012c" />
<img width="1745" height="381" alt="image" src="https://github.com/user-attachments/assets/b1fea7c5-e04a-4574-9cf1-e77680c0ed16" />
*Tabelas detalhadas com opção de download*

## 🔧 Funções Principais

### `calcular_movimentacao()`
Calcula diferença entre quantidades iniciais e atuais.

```python
# Entrada: DataFrame com colunas de quantidade
# Saída: DataFrame com coluna de movimentação
movimentação = quantidade_atual - quantidade_inicial
```

### `comparar_movimentacoes()`
Função principal que executa toda a comparação.

**Fluxo:**
1. Calcula movimentações em cada sistema
2. Filtra registros com movimentação ≠ 0
3. Cruza dados por ID
4. Classifica resultados


## Contribuição

Contribuições são bem-vindas!

## Licença

MIT License
