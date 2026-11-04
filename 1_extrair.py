import pandas as pd
import zipfile
import gdown
import shutil

from config import (
    PASTA_DADOS,
    ARQUIVOS,
    TAMANHO_BLOCO,
    CSV_SEPARADOR,
    CSV_ENCODING,
)
from banco import conectar, executar, inserir_em_lote

def baixar_e_extrair():
    """
    Baixa o ZIP do Google Drive e extrai os CSVs para a pasta data.
    """

    from config import DRIVE_FILE_ID

    PASTA_DADOS.mkdir(parents=True, exist_ok=True)

    caminho_zip = PASTA_DADOS / "dados_viagens.zip"

    print("\nBaixando arquivo do Google Drive...")

    url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"

    resultado = gdown.download(
        url,
        str(caminho_zip),
        quiet=False
    )

    if resultado is None:
        raise RuntimeError("Não foi possível baixar o arquivo ZIP.")

    print("Download concluído!")
    print("Extraindo arquivos...")

    with zipfile.ZipFile(caminho_zip, "r") as arquivo:
        arquivo.extractall(PASTA_DADOS)

    for configuracao in ARQUIVOS.values():
        nome_csv = configuracao["csv"]

        encontrados = list(PASTA_DADOS.rglob(nome_csv))

        if not encontrados:
            raise FileNotFoundError(
                f"Arquivo {nome_csv} não encontrado no ZIP."
            )

        origem = encontrados[0]
        destino = PASTA_DADOS / nome_csv

        if origem != destino:
            shutil.copy2(origem, destino)

    print("Extração concluída!")

def importar_csv(conexao, nome_csv, tabela_raw):
    """
    Importa um arquivo CSV para sua tabela Raw em blocos.
    """

    caminho_csv = PASTA_DADOS / nome_csv

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_csv}"
        )

    print(f"\nIniciando importação: {nome_csv}")

    cabecalho = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARADOR,
        encoding=CSV_ENCODING,
        dtype=str,
        nrows=0,
    )

    colunas = [coluna.strip() for coluna in cabecalho.columns]

    nomes_colunas = ", ".join(
        f"`{coluna}`" for coluna in colunas
    )

    marcadores = ", ".join(["%s"] * len(colunas))

    sql_insert = (
        f"INSERT INTO `{tabela_raw}` ({nomes_colunas}) "
        f"VALUES ({marcadores})"
    )

    executar(
        conexao,
        f"TRUNCATE TABLE `{tabela_raw}`"
    )

    total_registros = 0

    blocos = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARADOR,
        encoding=CSV_ENCODING,
        dtype=str,
        keep_default_na=False,
        chunksize=TAMANHO_BLOCO,
    )

    for numero_bloco, bloco in enumerate(blocos, start=1):

        bloco.columns = [
            coluna.strip() for coluna in bloco.columns
        ]

        linhas = list(
            bloco.itertuples(index=False, name=None)
        )

        inserir_em_lote(
            conexao,
            sql_insert,
            linhas
        )

        total_registros += len(linhas)

        print(
            f"Bloco {numero_bloco} importado: "
            f"{len(linhas)} registros"
        )

    print(
        f"Importação concluída: {total_registros} "
        f"registros em {tabela_raw}"
    )


def main():
    """
    Executa o download, a extração e a importação dos quatro CSVs.
    """

    conexao = None

    try:
        baixar_e_extrair()

        print("\nConectando ao banco de dados...")

        conexao = conectar()

        print("Conexão realizada com sucesso!")

        for nome, configuracao in ARQUIVOS.items():

            nome_csv = configuracao["csv"]
            tabela_raw = configuracao["tabela_raw"]

            importar_csv(
                conexao,
                nome_csv,
                tabela_raw
            )

        print("\nTodas as importações foram concluídas!")

    except Exception as erro:
        print(f"\nERRO durante a extração: {erro}")
        raise

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão com o banco encerrada.")


if __name__ == "__main__":
    main()
