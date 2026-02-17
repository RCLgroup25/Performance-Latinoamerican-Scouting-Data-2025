import pandas as pd
from sklearn.preprocessing import MinMaxScaler


import pandas as pd

COLUMNAS_MODELO = [
    "Player",
    "Squad",
    "Age",
    "90s",
    "Gls_p90",
    "Ast_p90"
]

def cargar_datos(path_excel: str) -> pd.DataFrame:
    df = pd.read_excel(path_excel)

    # Normalizar nombres (por si vienen con espacios raros)
    df.columns = df.columns.str.strip()

    return df


def preparar_datos_delanteros(df: pd.DataFrame) -> pd.DataFrame:
    # Validar columnas necesarias
    columnas_faltantes = [c for c in COLUMNAS_MODELO if c not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas en el dataset: {columnas_faltantes}")

    # Selección limpia
    df = df[COLUMNAS_MODELO].copy()

    # Convertir a numérico
    for col in ["Age", "90s", "Gls_p90", "Ast_p90"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar filas inválidas
    df = df.dropna()

    return df


def calcular_score(df, peso_goles, peso_asist):
    """
    Calcula un score ofensivo ponderado para delanteros
    """
    df = df.copy()

    df["Score"] = (
        df["Gls_p90"] * peso_goles +
        df["Ast_p90"] * peso_asist
    )

    return df