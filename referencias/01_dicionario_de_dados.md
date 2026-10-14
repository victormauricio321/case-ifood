# Dicionário de dados

## Colunas originais (`dados/ml_project1_data.csv`)

### Dados pessoais

| Coluna | Descrição |
|---|---|
| `ID` | Identificador único do cliente |
| `Year_Birth` | Ano de nascimento do cliente |
| `Education` | Nível de escolaridade: `Basic`, `2n Cycle`, `Graduation`, `Master` ou `PhD` |
| `Marital_Status` | Estado civil do cliente |
| `Income` | Renda anual da família do cliente |
| `Kidhome` | Número de crianças na casa do cliente |
| `Teenhome` | Número de adolescentes na casa do cliente |
| `Dt_Customer` | Data de cadastro do cliente na empresa (dia-mês-ano) |
| `Recency` | Número de dias desde a última compra do cliente |
| `Complain` | 1 se o cliente reclamou nos últimos 2 anos, 0 caso contrário |

### Gastos por categoria (últimos 2 anos)

| Coluna | Descrição |
|---|---|
| `MntWines` | Valor gasto em vinhos |
| `MntFruits` | Valor gasto em frutas |
| `MntMeatProducts` | Valor gasto em carnes |
| `MntFishProducts` | Valor gasto em peixes |
| `MntSweetProducts` | Valor gasto em doces |
| `MntGoldProds` | Valor gasto em produtos *gold* |

### Compras por canal

| Coluna | Descrição |
|---|---|
| `NumDealsPurchases` | Número de compras feitas com desconto |
| `NumWebPurchases` | Número de compras feitas pelo site da empresa |
| `NumCatalogPurchases` | Número de compras feitas pelo catálogo |
| `NumStorePurchases` | Número de compras feitas diretamente nas lojas |
| `NumWebVisitsMonth` | Número de visitas ao site da empresa no último mês |

### Campanhas

| Coluna | Descrição |
|---|---|
| `AcceptedCmp1` a `AcceptedCmp5` | 1 se o cliente aceitou a oferta da 1ª à 5ª campanha, 0 caso contrário |
| `Response` | 1 se o cliente aceitou a oferta da campanha piloto, 0 caso contrário (**variável-alvo**) |
| `Z_CostContact` | Não consta no dicionário original. Vale sempre 3, o custo por contato do case |
| `Z_Revenue` | Não consta no dicionário original. Vale sempre 11, a receita por aceite do case |

## Colunas criadas na engenharia de features

Criadas no notebook [01_eda_e_tratamento](../notebooks/01_eda_e_tratamento.ipynb). A data de referência é a
data de cadastro mais recente da base (29/06/2014).

| Coluna | Cálculo |
|---|---|
| `DaysSinceEnrolled` | Dias entre o cadastro do cliente e a data de referência |
| `YearsSinceEnrolled` | `DaysSinceEnrolled // 365` (anos completos de cadastro) |
| `Age` | Ano da data de referência (2014) − `Year_Birth` |
| `AgeGroup` | Faixa etária: `18-30`, `31-45`, `46-60` ou `61+` |
| `MntTotal` | Soma dos seis gastos por categoria |
| `MntRegularProds` | `MntTotal − MntGoldProds` |
| `Children` | `Kidhome + Teenhome` |
| `HasChildren` | 1 se `Children > 0` |
| `AcceptedCmpTotal` | Soma de `AcceptedCmp1` a `AcceptedCmp5` |
| `HasAcceptedCmp` | 1 se o cliente aceitou pelo menos uma das cinco campanhas anteriores |
| `NumTotalPurchases` | `NumWebPurchases + NumCatalogPurchases + NumStorePurchases` |

`Marital_Status` foi simplificada para `Partner` (casado ou morando junto) e `Single` (demais categorias).
`Year_Birth`, `Dt_Customer`, `Z_CostContact` e `Z_Revenue` foram removidas da base tratada.
