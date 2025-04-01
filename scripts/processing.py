import pandas as pd

def process_data(input_path="data/raw/messi_raw_data.csv", output_path="data/processed/messi_cleaned_data.csv", return_df=False):
    """Procesa los datos sucios de Messi y los guarda limpios en la carpeta processed."""

    # Leer el CSV original
    df = pd.read_csv(input_path)

    # Crear columnas limpias para Competition y Lineup
    df["Competition"] = df["Competition"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)
    df["Lineup"] = df["Lineup"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)

    # Eliminar columnas innecesarias + las versiones originales
    df.drop(columns=["Index", "Jersey", "Extra"], inplace=True, errors="ignore")

    # Convertir tipos de datos numéricos
    for col in ["Goals", "Assists", "Cards", "Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convertir fecha
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 🚨 Verificar si hay nulos en 'Date' o 'Minutes'
    nulos_date = df["Date"].isna().sum()
    nulos_minutes = df["Minutes"].isna().sum()

    if nulos_date > 0:
        print(f"⚠️ Hay {nulos_date} filas con fecha inválida:")
        print(df[df["Date"].isna()][["Date", "Home Team", "Away Team"]].head())

    if nulos_minutes > 0:
        print(f"⚠️ Hay {nulos_minutes} filas con 'Minutes' inválidos:")
        print(df[df["Minutes"].isna()][["Minutes", "Home Team", "Away Team"]].head())

    # Rellenar nulos numéricos con 0
    df["Minutes"] = df["Minutes"].fillna(0).astype(int)
    df["Goals"] = df["Goals"].fillna(0).astype(int)
    df["Assists"] = df["Assists"].fillna(0).astype(int)
    df["Cards"] = df["Cards"].fillna(0).astype(int)

    # Guardar DataFrame limpio
    df.to_csv(output_path, index=False)
    print(f"✅ Datos procesados guardados en: {output_path}")

    if return_df:
        return df
