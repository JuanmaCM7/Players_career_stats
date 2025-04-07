import pandas as pd
from pathlib import Path
from datetime import datetime

def process_data(input_rel="data/raw/messi_raw_data.csv", output_rel="data/processed/messi_cleaned_data.csv", return_df=False):
    """Procesa los datos sucios de Messi y guarda la versión limpia."""

    # Detectar raíz del proyecto (asumimos que este archivo está en /src)
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / input_rel
    output_path = project_root / output_rel

    # Crear carpeta processed si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Leer el CSV original
    df = pd.read_csv(input_path)

    # Limpiar Competition y Lineup
    df["Competition"] = df["Competition"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)
    df["Lineup"] = df["Lineup"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)

    # Eliminar columnas innecesarias
    df.drop(columns=["Index", "Jersey", "Extra"], inplace=True, errors="ignore")

    # Convertir columnas numéricas
    for col in ["Goals", "Assists", "Cards", "Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convertir la columna 'Date' a datetime con tolerancia
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce", dayfirst=True)

    # Función para asignar temporada incluyendo excepción COVID
    def asignar_temporada(fecha):
        if pd.isna(fecha):
            return None

        # Excepción temporada COVID: 16/08/2019 - 14/08/2020
        if datetime(2019, 8, 15) <= fecha <= datetime(2020, 8, 14):
            return "2019-2020"

        # Temporadas normales: 1 agosto - 15 junio
        year = fecha.year
        temporada_inicio = datetime(year, 8, 1)
        temporada_fin = datetime(year + 1, 6, 15)

        if fecha >= temporada_inicio and fecha <= datetime(year + 1, 12, 31):
            return f"{year}-{year + 1}"
        elif fecha <= temporada_fin:
            return f"{year - 1}-{year}"
        else:
            return None

    # Crear columna Season
    df["Season"] = df["Date"].apply(asignar_temporada)

    # Reordenar columnas
    cols = ["Date", "Season"] + [col for col in df.columns if col not in ["Date", "Season"]]
    df = df[cols]

    # Validar nulos
    nulos_date = df["Date"].isna().sum()
    nulos_minutes = df["Minutes"].isna().sum()

    if nulos_date > 0:
        print(f"⚠️ {nulos_date} fechas inválidas:")
        print(df[df["Date"].isna()][["Date", "Home Team", "Away Team"]].head())

    if nulos_minutes > 0:
        print(f"⚠️ {nulos_minutes} minutos inválidos:")
        print(df[df["Minutes"].isna()][["Minutes", "Home Team", "Away Team"]].head())

    # Rellenar nulos con 0
    df["Minutes"] = df["Minutes"].fillna(0).astype(int)
    df["Goals"] = df["Goals"].fillna(0).astype(int)
    df["Assists"] = df["Assists"].fillna(0).astype(int)
    df["Cards"] = df["Cards"].fillna(0).astype(int)

    # Guardar
    df.to_csv(output_path, index=False)
    print(f"✅ Datos procesados guardados en: {output_path}")

    if return_df:
        return df
