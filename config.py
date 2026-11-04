import os
from pathlib import Path

PASTA_RAIZ = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_RAIZ / "data"

def carregar_env():
    """Le o arquivo .env (se existir) e joga as variaveis para os.environ."""
    arquivo_env = PASTA_RAIZ / ".env"
    if not arquivo_env.exists():
        return
    for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        # ignora linhas vazias e comentarios
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


carregar_env()

MYSQL_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "transparencia"),
}

ANO = "2025"

DRIVE_FILE_ID = "1pQjKacyHdIsyteknQbwKGM5_4hL5V4RV"


TAMANHO_BLOCO = 50_000

ARQUIVOS = {
    "viagem":     {"csv": f"{ANO}_Viagem.csv",     "tabela_raw": "raw_viagem"},
    "pagamento":  {"csv": f"{ANO}_Pagamento.csv",  "tabela_raw": "raw_pagamento"},
    "passagem":   {"csv": f"{ANO}_Passagem.csv",   "tabela_raw": "raw_passagem"},
    "trecho":     {"csv": f"{ANO}_Trecho.csv",     "tabela_raw": "raw_trecho"},
}

CSV_SEPARADOR = ";"
CSV_ENCODING = "latin-1"   # acentuacao no padrao ISO-8859-1
