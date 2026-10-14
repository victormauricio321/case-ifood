"""Caminhos e constantes compartilhados pelos notebooks do projeto."""

from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parents[2]

# dados
PASTA_DADOS = PASTA_PROJETO / "dados"
DADOS_ORIGINAIS = PASTA_DADOS / "ml_project1_data.csv"
DADOS_TRATADOS = PASTA_DADOS / "clientes_tratados.parquet"
DADOS_CLUSTERIZADOS = PASTA_DADOS / "clientes_clusterizados.parquet"

# modelos
PASTA_MODELOS = PASTA_PROJETO / "modelos"
MODELO_FINAL = PASTA_MODELOS / "modelo_propensao.joblib"

# relatórios e figuras
PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"
PASTA_IMAGENS = PASTA_RELATORIOS / "imagens"

# reprodutibilidade
RANDOM_STATE = 42

# economia da campanha (valores do case, também presentes nas colunas Z_CostContact e Z_Revenue)
CUSTO_CONTATO = 3  # MU gastas por cliente contatado
RECEITA_ACEITE = 11  # MU recebidas por cliente que aceita a oferta
