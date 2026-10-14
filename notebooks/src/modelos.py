"""Construção, validação e avaliação financeira dos modelos de classificação."""

import numpy as np
import pandas as pd

from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV, cross_validate

from .config import CUSTO_CONTATO, RANDOM_STATE, RECEITA_ACEITE

METRICAS = [
    "accuracy",
    "balanced_accuracy",
    "f1",
    "precision",
    "recall",
    "roc_auc",
    "average_precision",
]


def construir_pipeline_classificador(
    classificador, preprocessador=None, k="all", undersampling=True
):
    """Monta o pipeline de classificação.

    Etapas: pré-processamento, seleção das k melhores features (teste F da ANOVA),
    undersampling da classe majoritária e classificador. O pipeline do
    imbalanced-learn garante que o undersampling só é aplicado no treino de cada fold.

    Parameters
    ----------
    classificador : estimador do scikit-learn
        Modelo de classificação.
    preprocessador : ColumnTransformer, opcional
        Transformações das colunas. Se None, não há pré-processamento nem seleção
        de features (útil para o DummyClassifier).
    k : int ou "all", opcional
        Quantidade de features mantidas pelo SelectKBest, por padrão "all".
    undersampling : bool, opcional
        Se True, inclui o RandomUnderSampler, por padrão True.

    Returns
    -------
    imblearn.pipeline.Pipeline
        Pipeline pronto para treino.
    """
    etapas = []

    if preprocessador is not None:
        etapas.append(("preprocessor", preprocessador))
        etapas.append(("feature_select", SelectKBest(f_classif, k=k)))

    if undersampling:
        etapas.append(("sampler", RandomUnderSampler(random_state=RANDOM_STATE)))

    etapas.append(("clf", classificador))

    return Pipeline(etapas)


def treinar_e_validar_classificador(
    X, y, cv, classificador, preprocessador=None, k="all", undersampling=True
):
    """Avalia um classificador com validação cruzada nas métricas de METRICAS.

    Returns
    -------
    dict
        Resultado do cross_validate (tempos e uma lista de scores por métrica).
    """
    modelo = construir_pipeline_classificador(
        classificador, preprocessador, k=k, undersampling=undersampling
    )

    return cross_validate(modelo, X, y, cv=cv, scoring=METRICAS, n_jobs=-1)


def grid_search_classificador(
    classificador,
    param_grid,
    cv,
    preprocessador=None,
    k="all",
    undersampling=True,
    metrica_refit="average_precision",
    return_train_score=False,
):
    """Cria um GridSearchCV sobre o pipeline de classificação.

    Os nomes dos hiperparâmetros seguem o padrão do pipeline, por exemplo
    "clf__C" e "feature_select__k".
    """
    modelo = construir_pipeline_classificador(
        classificador, preprocessador, k=k, undersampling=undersampling
    )

    return GridSearchCV(
        modelo,
        param_grid=param_grid,
        cv=cv,
        scoring=METRICAS,
        refit=metrica_refit,
        n_jobs=-1,
        return_train_score=return_train_score,
    )


def organizar_resultados(resultados):
    """Transforma o dicionário {modelo: resultado do cross_validate} em um dataframe.

    Cada linha corresponde a um fold de um modelo. A coluna "time_seconds" soma
    os tempos de treino e de predição.
    """
    for valor in resultados.values():
        valor["time_seconds"] = valor["fit_time"] + valor["score_time"]

    df_resultados = (
        pd.DataFrame(resultados).T.reset_index().rename(columns={"index": "model"})
    )

    df_expandido = df_resultados.explode(
        df_resultados.columns[1:].to_list()
    ).reset_index(drop=True)

    colunas_numericas = df_expandido.columns.drop("model")
    df_expandido[colunas_numericas] = df_expandido[colunas_numericas].apply(
        pd.to_numeric
    )

    return df_expandido


def lucro_campanha(
    y_verdadeiro, contatar, custo=CUSTO_CONTATO, receita=RECEITA_ACEITE
):
    """Calcula o lucro de uma campanha.

    Cada cliente contatado custa `custo`; cada cliente contatado que aceita gera
    `receita`.

    Parameters
    ----------
    y_verdadeiro : array-like de 0 e 1
        Se o cliente aceitou a oferta.
    contatar : array-like de bool
        Se o cliente seria contatado.

    Returns
    -------
    float
        Lucro em MU.
    """
    y_verdadeiro = np.asarray(y_verdadeiro)
    contatar = np.asarray(contatar, dtype=bool)

    aceites = y_verdadeiro[contatar].sum()
    return receita * aceites - custo * contatar.sum()


def curva_de_lucro(
    y_verdadeiro, scores, custo=CUSTO_CONTATO, receita=RECEITA_ACEITE
):
    """Calcula o lucro para cada quantidade de clientes contatados.

    Os clientes são ordenados do maior para o menor score e contatados nessa
    ordem. Cada linha do resultado corresponde a contatar os n primeiros.

    Returns
    -------
    pandas.DataFrame
        Colunas: limiar, contatados, pct_contatados, aceites, precisao, recall, lucro.
    """
    y_verdadeiro = np.asarray(y_verdadeiro)
    scores = np.asarray(scores)

    ordem = np.argsort(-scores, kind="stable")
    y_ordenado = y_verdadeiro[ordem]
    scores_ordenados = scores[ordem]

    contatados = np.arange(1, len(y_ordenado) + 1)
    aceites = np.cumsum(y_ordenado)

    curva = pd.DataFrame(
        {
            "limiar": scores_ordenados,
            "contatados": contatados,
            "pct_contatados": contatados / len(y_ordenado),
            "aceites": aceites,
            "precisao": aceites / contatados,
            "recall": aceites / y_verdadeiro.sum(),
            "lucro": receita * aceites - custo * contatados,
        }
    )

    # clientes com o mesmo score não podem ser separados por um limiar
    return curva.drop_duplicates(subset="limiar", keep="last").reset_index(drop=True)
