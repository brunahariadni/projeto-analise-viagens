
import pandas as pd

from config import (
    PASTA_DADOS,
    ARQUIVOS,
    CSV_SEPARADOR,
    CSV_ENCODING,
    TAMANHO_BLOCO,
)

for nome, configuracao in ARQUIVOS.items():

    arquivo = PASTA_DADOS / configuracao["csv"]

    print(f"\nAnalisando: {arquivo.name}")

    maiores_tamanhos = {}

    blocos = pd.read_csv(
        arquivo,
        sep=CSV_SEPARADOR,
        encoding=CSV_ENCODING,
        dtype=str,
        keep_default_na=False,
        chunksize=TAMANHO_BLOCO,
    )

    for bloco in blocos:
        bloco.columns = [col.strip() for col in bloco.columns]

        for coluna in bloco.columns:
            tamanho = bloco[coluna].str.len().max()

            if pd.notna(tamanho):
                maiores_tamanhos[coluna] = max(
                    maiores_tamanhos.get(coluna, 0),
                    int(tamanho)
                )

    encontrados = {
        coluna: tamanho
        for coluna, tamanho in maiores_tamanhos.items()
        if tamanho > 255
    }

    if encontrados:
        for coluna, tamanho in encontrados.items():
            print(f"{coluna}: {tamanho} caracteres")
    else:
        print("Nenhuma coluna ultrapassa 255 caracteres.")
