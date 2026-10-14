"""Funções de visualização usadas nos notebooks."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.colors import ListedColormap
from matplotlib.ticker import PercentFormatter
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from .config import PASTA_IMAGENS, RANDOM_STATE


def salvar_figura(fig, nome_arquivo, dpi=150):
    """Salva a figura em relatorios/imagens para uso no README e na apresentação."""
    PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)
    fig.savefig(PASTA_IMAGENS / nome_arquivo, dpi=dpi, bbox_inches="tight")


def _finalizar(fig, nome_arquivo):
    if nome_arquivo is not None:
        salvar_figura(fig, nome_arquivo)
    plt.show()


def pairplot(
    dataframe,
    colunas,
    coluna_hue=None,
    alpha=0.5,
    corner=True,
    height=2,
    palette="tab10",
    nome_arquivo=None,
):
    """Pairplot das colunas, com KDE na diagonal e cor definida por coluna_hue."""
    analise = list(colunas) + ([coluna_hue] if coluna_hue else [])

    grid = sns.pairplot(
        dataframe[analise],
        diag_kind="kde",
        hue=coluna_hue,
        plot_kws=dict(alpha=alpha),
        corner=corner,
        height=height,
        palette=palette if coluna_hue else None,
    )

    _finalizar(grid.figure, nome_arquivo)


def plot_cotovelo_silhueta(X, random_state=RANDOM_STATE, intervalo_k=(2, 11), nome_arquivo=None):
    """Gera os gráficos dos métodos do cotovelo (inércia) e da silhueta.

    Parameters
    ----------
    X : array-like
        Dados já pré-processados.
    random_state : int, opcional
        Semente do K-Means, por padrão RANDOM_STATE.
    intervalo_k : tuple, opcional
        Intervalo de quantidades de clusters testadas, por padrão (2, 11).
    """
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4), tight_layout=True)

    valores_k = range(*intervalo_k)
    inercias = []
    silhuetas = []

    for k in valores_k:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        kmeans.fit(X)
        inercias.append(kmeans.inertia_)
        silhuetas.append(silhouette_score(X, kmeans.labels_))

    sns.lineplot(x=list(valores_k), y=inercias, marker="o", ax=axs[0])
    axs[0].set_xlabel("Número de clusters (k)")
    axs[0].set_ylabel("Inércia")
    axs[0].set_title("Método do cotovelo")

    sns.lineplot(x=list(valores_k), y=silhuetas, marker="o", ax=axs[1])
    axs[1].set_xlabel("Número de clusters (k)")
    axs[1].set_ylabel("Coeficiente de silhueta")
    axs[1].set_title("Método da silhueta")

    for ax in axs:
        ax.set_xticks(list(valores_k))

    _finalizar(fig, nome_arquivo)


def plot_clusters_2d(
    dataframe,
    colunas,
    centroides,
    coluna_clusters=None,
    mostrar_pontos=True,
    rotulos_eixos=None,
    titulo="Clusters",
    nome_arquivo=None,
):
    """Gráfico de dispersão 2D dos clusters com os centroides numerados.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dados com as duas colunas a serem plotadas.
    colunas : list[str]
        Nomes das colunas dos eixos x e y.
    centroides : np.ndarray
        Coordenadas dos centroides, no mesmo espaço das colunas.
    coluna_clusters : array-like, opcional
        Rótulo de cluster de cada ponto, usado para colorir.
    mostrar_pontos : bool, opcional
        Se True, plota os pontos além dos centroides, por padrão True.
    rotulos_eixos : tuple[str, str], opcional
        Rótulos dos eixos. Se None, usa os nomes das colunas.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    n_clusters = len(centroides)
    cores = ListedColormap(plt.cm.tab10.colors[:n_clusters])

    if mostrar_pontos:
        pontos = ax.scatter(
            dataframe[colunas[0]],
            dataframe[colunas[1]],
            c=coluna_clusters,
            cmap=cores,
            s=15,
            alpha=0.6,
        )
        ax.legend(*pontos.legend_elements(), title="Cluster", bbox_to_anchor=(1.02, 1), loc="upper left")

    for i, centroide in enumerate(centroides):
        ax.scatter(*centroide, s=500, color="white", edgecolor="black", alpha=0.85)
        ax.text(*centroide, f"{i}", fontsize=16, ha="center", va="center", weight="bold")

    rotulos_eixos = rotulos_eixos or colunas
    ax.set_xlabel(rotulos_eixos[0])
    ax.set_ylabel(rotulos_eixos[1])
    ax.set_title(titulo)

    _finalizar(fig, nome_arquivo)


def _rotular_barras(h, cor="white"):
    for barras in h.containers:
        h.bar_label(
            barras,
            label_type="center",
            labels=[f"{b.get_height():.0%}" if b.get_height() >= 0.04 else "" for b in barras],
            color=cor,
            weight="bold",
            fontsize=10,
        )
    for barra in h.patches:
        barra.set_linewidth(0)


def plot_percentual_por_cluster(
    dataframe,
    colunas,
    linhas_colunas=(2, 3),
    figsize=(15, 8),
    coluna_cluster="Cluster",
    nome_arquivo=None,
):
    """Barras empilhadas: composição de cada cluster segundo cada coluna.

    Cada barra é um cluster e soma 100%. Responde "como é o cluster X?".
    """
    fig, axs = plt.subplots(
        nrows=linhas_colunas[0], ncols=linhas_colunas[1], figsize=figsize, sharey=True
    )
    axs = np.atleast_1d(axs)

    for ax, coluna in zip(axs.flatten(), colunas):
        dados = dataframe[[coluna_cluster, coluna]].copy()
        # colunas numéricas (0, 1, 2...) viram texto para receber cores categóricas
        if pd.api.types.is_numeric_dtype(dados[coluna]):
            dados[coluna] = dados[coluna].astype(str)
        ordem = (
            list(dados[coluna].cat.categories)
            if isinstance(dados[coluna].dtype, pd.CategoricalDtype)
            else sorted(dados[coluna].unique())
        )

        h = sns.histplot(
            x=coluna_cluster,
            hue=coluna,
            hue_order=ordem,
            data=dados,
            ax=ax,
            multiple="fill",
            stat="percent",
            discrete=True,
            shrink=0.8,
            palette="Set2",
        )

        h.set_xticks(range(dataframe[coluna_cluster].nunique()))
        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel("")
        h.set_xlabel("Cluster")
        h.set_title(coluna)
        h.tick_params(axis="both", which="both", length=0)
        _rotular_barras(h, cor="black")
        sns.move_legend(
            h, "upper left", bbox_to_anchor=(1, 1), title=None, frameon=False, fontsize=9
        )

    plt.subplots_adjust(hspace=0.35, wspace=0.45)

    _finalizar(fig, nome_arquivo)


def plot_percentual_cluster_por_coluna(
    dataframe,
    colunas,
    linhas_colunas=(2, 3),
    figsize=(15, 8),
    coluna_cluster="Cluster",
    palette="tab10",
    nome_arquivo=None,
):
    """Barras empilhadas: distribuição dos clusters dentro de cada categoria.

    Cada barra é uma categoria da coluna e soma 100%. Responde "quem são os
    clientes da categoria Y?".
    """
    fig, axs = plt.subplots(
        nrows=linhas_colunas[0], ncols=linhas_colunas[1], figsize=figsize, sharey=True
    )
    axs = np.atleast_1d(axs)

    for ax, coluna in zip(axs.flatten(), colunas):
        h = sns.histplot(
            x=coluna,
            hue=coluna_cluster,
            data=dataframe,
            ax=ax,
            multiple="fill",
            stat="percent",
            discrete=True,
            shrink=0.8,
            palette=palette,
        )

        if pd.api.types.is_numeric_dtype(dataframe[coluna]):
            h.set_xticks(sorted(dataframe[coluna].unique()))

        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel("")
        h.tick_params(axis="both", which="both", length=0)
        _rotular_barras(h)

        legenda = h.get_legend()
        legenda.remove()

    rotulos = [texto.get_text() for texto in legenda.get_texts()]

    fig.legend(
        handles=legenda.legend_handles,
        labels=rotulos,
        loc="upper center",
        ncols=dataframe[coluna_cluster].nunique(),
        title="Cluster",
    )

    plt.subplots_adjust(hspace=0.35, wspace=0.3)

    _finalizar(fig, nome_arquivo)


def plot_comparar_metricas_modelos(df_resultados, nome_arquivo=None):
    """Boxplots das métricas de validação cruzada de cada modelo."""
    fig, axs = plt.subplots(4, 2, figsize=(10, 11), sharex=True)

    metricas = [
        "time_seconds",
        "test_accuracy",
        "test_balanced_accuracy",
        "test_f1",
        "test_precision",
        "test_recall",
        "test_roc_auc",
        "test_average_precision",
    ]

    nomes = [
        "Tempo (s)",
        "Acurácia",
        "Acurácia balanceada",
        "F1",
        "Precisão",
        "Recall",
        "ROC-AUC",
        "AUPRC (average precision)",
    ]

    for ax, metrica, nome in zip(axs.flatten(), metricas, nomes):
        sns.boxplot(x="model", y=metrica, data=df_resultados, ax=ax, showmeans=True)
        ax.set_title(nome)
        ax.set_ylabel(nome)
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()

    _finalizar(fig, nome_arquivo)


def plot_coeficientes(df_coeficientes, titulo="Coeficientes", nome_arquivo=None):
    """Barras horizontais com os coeficientes de um modelo linear."""
    altura = max(4, 0.3 * len(df_coeficientes))
    fig, ax = plt.subplots(figsize=(8, altura))

    cores = np.where(df_coeficientes["coeficiente"] > 0, "tab:blue", "tab:red")
    ax.barh(df_coeficientes.index, df_coeficientes["coeficiente"], color=cores)
    ax.axvline(x=0, color=".5")
    ax.set_title(titulo)
    ax.set_xlabel("Coeficiente")

    _finalizar(fig, nome_arquivo)


def plot_curva_de_lucro(curva, lucro_contatar_todos, ponto_escolhido=None, titulo=None, nome_arquivo=None):
    """Lucro da campanha em função da fração de clientes contatados.

    Parameters
    ----------
    curva : pandas.DataFrame
        Saída de src.modelos.curva_de_lucro.
    lucro_contatar_todos : float
        Lucro ao contatar todos os clientes (estratégia do piloto).
    ponto_escolhido : pandas.Series, opcional
        Linha da curva correspondente ao limiar escolhido, destacada no gráfico.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(curva["pct_contatados"], curva["lucro"], label="Contatar por ordem de score do modelo")
    ax.axhline(lucro_contatar_todos, color="tab:red", linestyle="--", label="Contatar todos (piloto)")
    ax.axhline(0, color=".5", linewidth=0.8)

    if ponto_escolhido is not None:
        ax.scatter(
            ponto_escolhido["pct_contatados"],
            ponto_escolhido["lucro"],
            color="black",
            zorder=3,
            label=f"Limiar escolhido ({ponto_escolhido['pct_contatados']:.0%} da base)",
        )

    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Clientes contatados (ordenados pelo score)")
    ax.set_ylabel("Lucro (MU)")
    ax.set_title(titulo or "Lucro da campanha por fração de clientes contatados")
    ax.legend()

    _finalizar(fig, nome_arquivo)
