"""Funções auxiliares de análise de dados."""

import pandas as pd


def inspecionar_outliers(dataframe, coluna, largura_bigode=1.5):
    """Retorna as linhas cujo valor na coluna está fora dos bigodes do boxplot.

    Usa o critério de Tukey: abaixo de Q1 - 1,5 x IQR ou acima de Q3 + 1,5 x IQR,
    em que IQR = Q3 - Q1 é o intervalo interquartil.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    coluna : str
        Nome da coluna a ser inspecionada.
    largura_bigode : float, opcional
        Multiplicador do IQR que define os limites, por padrão 1.5.

    Returns
    -------
    pandas.DataFrame
        Linhas consideradas outliers.
    """
    q1 = dataframe[coluna].quantile(0.25)
    q3 = dataframe[coluna].quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - largura_bigode * iqr
    limite_superior = q3 + largura_bigode * iqr

    return dataframe[
        (dataframe[coluna] < limite_inferior) | (dataframe[coluna] > limite_superior)
    ]


def dataframe_coeficientes(coeficientes, colunas):
    """Organiza os coeficientes de um modelo linear em um dataframe ordenado.

    Parameters
    ----------
    coeficientes : array-like
        Coeficientes do modelo.
    colunas : array-like
        Nomes das features, na mesma ordem dos coeficientes.

    Returns
    -------
    pandas.DataFrame
        Dataframe com a coluna "coeficiente", ordenado do menor para o maior.
    """
    return pd.DataFrame(
        data=coeficientes, index=colunas, columns=["coeficiente"]
    ).sort_values(by="coeficiente")
