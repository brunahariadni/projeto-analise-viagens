
import pandas as pd

from config import PASTA_DADOS, CSV_ENCODING, CSV_SEPARADOR

arquivo = PASTA_DADOS / "2025_Viagem.csv"

df = pd.read_csv(
    arquivo,
    sep=CSV_SEPARADOR,
    encoding=CSV_ENCODING,
    dtype=str,
    keep_default_na=False,
    usecols=["Motivo"]
)

tamanhos = df["Motivo"].str.len()

print("Maior quantidade de caracteres:", tamanhos.max())

print("\nExemplo do maior texto:")
print(df.loc[tamanhos.idxmax(), "Motivo"])
