import pandas as pd
from pathlib import Path
from datetime import datetime

def process_data(input_rel="data/raw/messi_raw_data.csv", output_rel="data/processed/messi_cleaned_data.csv", return_df=False):
    """Procesa los datos sucios de Messi y guarda la versión limpia."""

    # Detectar raíz del proyecto
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / input_rel
    output_path = project_root / output_rel

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    # Limpiar texto de Competition y Lineup
    df["Competition"] = df["Competition"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)
    df["Lineup"] = df["Lineup"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)

    # Eliminar columnas irrelevantes
    df.drop(columns=["Index", "Jersey", "Extra"], inplace=True, errors="ignore")

    # Convertir numéricos
    for col in ["Goals", "Assists", "Cards", "Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convertir fechas
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce", dayfirst=True)

    # Crear columna Season (considerando temporada COVID)
    def asignar_temporada(fecha):
        if pd.isna(fecha):
            return None
        if datetime(2019, 8, 15) <= fecha <= datetime(2020, 8, 14):
            return "2019-2020"
        year = fecha.year
        if fecha >= datetime(year, 8, 1):
            return f"{year}-{year + 1}"
        else:
            return f"{year - 1}-{year}"

    df["Season"] = df["Date"].apply(asignar_temporada)

    # Clasificar equipo en el que jugaba Messi por temporada
    def clasificar_equipo(season, competition):
        if pd.isna(season) or pd.isna(competition):
            return "Unknown"
        if "argentina" in competition.lower() or "national" in competition.lower():
            return "Argentina"
        elif season <= "2020-2021":
            return "FC Barcelona"
        elif season in ["2021-2022", "2022-2023"]:
            return "Paris Saint-Germain"
        elif season >= "2023-2024":
            return "Inter Miami"
        return "Unknown"

    # Añadir columna clara con el equipo de Messi
    df["Messi_Team"] = df.apply(lambda row: clasificar_equipo(row["Season"], row["Competition"]), axis=1)

    # Clasificar si jugó como local o visitante
    def fue_local(row):
        if pd.isna(row["Home Team"]) or pd.isna(row["Messi_Team"]):
            return "Unknown"
        return "Home" if row["Home Team"] == row["Messi_Team"] else "Away"

    df["Home/Away"] = df.apply(fue_local, axis=1)

    # Reordenar columnas
    cols = ["Date", "Season", "Messi_Team", "Home/Away"] + [col for col in df.columns if col not in ["Date", "Season", "Messi_Team", "Home/Away"]]
    df = df[cols]

    # Validación de nulos
    if df["Date"].isna().sum() > 0:
        print("⚠️ Fechas inválidas encontradas:")
        print(df[df["Date"].isna()][["Date", "Home Team", "Away Team"]].head())

    if df["Minutes"].isna().sum() > 0:
        print("⚠️ Minutos inválidos encontrados:")
        print(df[df["Minutes"].isna()][["Minutes", "Home Team", "Away Team"]].head())

    # Rellenar nulos numéricos
    df["Minutes"] = df["Minutes"].fillna(0).astype(int)
    df["Goals"] = df["Goals"].fillna(0).astype(int)
    df["Assists"] = df["Assists"].fillna(0).astype(int)
    df["Cards"] = df["Cards"].fillna(0).astype(int)

    # Guardar resultado
    df.to_csv(output_path, index=False)
    print(f"✅ Datos procesados guardados en: {output_path}")

    if return_df:
        return df
