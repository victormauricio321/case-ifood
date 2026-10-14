# Dados

## Arquivo original

| Arquivo | Descrição |
|---|---|
| `ml_project1_data.csv` | Base do case de Analista de Dados do iFood: 2.240 clientes, 29 colunas, separada por tabulação |

**Fonte:** case público do processo seletivo de Analista de Dados do iFood. O repositório original
(`ifood/ifood-data-business-analyst-test`) não está mais disponível. Uma cópia do case, com os mesmos dados,
está em [github.com/nailson/ifood-data-business-analyst-test](https://github.com/nailson/ifood-data-business-analyst-test).
Os dados são fictícios e foram disponibilizados publicamente para fins de avaliação e estudo.

Para baixar novamente (a cópia está em .csv e com outro formato de data):

```bash
curl -L -o ml_project1_data_copia.csv https://raw.githubusercontent.com/nailson/ifood-data-business-analyst-test/master/ml_project1_data.csv
```

O significado de cada coluna está no [dicionário de dados](../referencias/01_dicionario_de_dados.md).

## Arquivos gerados pelos notebooks

| Arquivo | Gerado por | Conteúdo |
|---|---|---|
| `clientes_tratados.parquet` | [01_eda_e_tratamento](../notebooks/01_eda_e_tratamento.ipynb) | 2.023 clientes após remover duplicatas, nulos e registros inválidos, com as variáveis criadas na engenharia de features. O `ID` do cliente é o índice |
| `clientes_clusterizados.parquet` | [02_segmentacao_clientes](../notebooks/02_segmentacao_clientes.ipynb) | Base tratada com a coluna `Cluster` (0, 1 ou 2) |

Os arquivos Parquet preservam os tipos das colunas (por exemplo, a ordem das faixas de `AgeGroup`).
