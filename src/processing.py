# processing.py — Messi + Lamine

import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# -------------------- MESSI --------------------

def process_data(input_rel="data/raw/messi_raw_data.csv", output_rel="data/processed/messi_cleaned_data.csv", return_df=False):
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / input_rel
    output_path = project_root / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    df["Competition"] = df["Competition"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)
    df["Lineup"] = df["Lineup"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)

    df.drop(columns=["Index", "Jersey", "Extra"], inplace=True, errors="ignore")

    for col in ["Goals", "Assists", "Cards", "Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce", dayfirst=True)

    def asignar_temporada(fecha):
        if pd.isna(fecha):
            return None
        if datetime(2019, 8, 15) <= fecha <= datetime(2020, 8, 14):
            return "2019-2020"
        year = fecha.year
        return f"{year}-{year + 1}" if fecha.month >= 8 else f"{year - 1}-{year}"

    df["Season"] = df["Date"].apply(asignar_temporada)

    birthdate = pd.to_datetime("1987-06-24")
    df["Age"] = df["Date"].apply(lambda d: round((d - birthdate).days / 365.25, 2) if pd.notna(d) else None)

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

    df["Messi_Team"] = df.apply(lambda row: clasificar_equipo(row["Season"], row["Competition"]), axis=1)

    def fue_local(row):
        if pd.isna(row["Home Team"]) or pd.isna(row["Messi_Team"]):
            return "Unknown"
        return "Home" if row["Home Team"] == row["Messi_Team"] else "Away"

    df["Home/Away"] = df.apply(fue_local, axis=1)

    cols = ["Date", "Season", "Age", "Messi_Team", "Home/Away"] + [col for col in df.columns if col not in ["Date", "Season", "Age", "Messi_Team", "Home/Away"]]
    df = df[cols]

    df["Minutes"] = df["Minutes"].fillna(0).astype(int)
    df["Goals"] = df["Goals"].fillna(0).astype(int)
    df["Assists"] = df["Assists"].fillna(0).astype(int)
    df["Cards"] = df["Cards"].fillna(0).astype(int)

    df.to_csv(output_path, index=False)
    print(f"✅ Datos procesados guardados en: {output_path}")
    if return_df:
        return df

# -------------------- LAMINE --------------------

def process_lamine_data(input_rel="data/raw/lamine_raw_data.csv", output_rel="data/processed/lamine_cleaned_data.csv", return_df=True):
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / input_rel
    output_path = project_root / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_yamal = pd.read_csv(input_path)
    birthdate = pd.to_datetime("2007-07-13")

    df_yamal["Date"] = pd.to_datetime(df_yamal["Date"], errors="coerce")

    def asignar_temporada(fecha):
        if pd.isna(fecha):
            return None
        year = fecha.year
        return f"{year}-{year + 1}" if fecha.month >= 8 else f"{year - 1}-{year}"

    df_yamal["Season"] = df_yamal["Date"].apply(asignar_temporada)
    df_yamal["Age"] = df_yamal["Date"].apply(lambda d: round((d - birthdate).days / 365.25, 2) if pd.notna(d) else None)
    df_yamal["Home/Away"] = df_yamal["Venue"].apply(lambda v: "Home" if v == "Home" else "Away")
    df_yamal["Lineup"] = df_yamal["Start"].apply(lambda s: "Starter" if s == "Y" else "Substitute")
    df_yamal["Squad"] = df_yamal["Squad"].str.replace(r"^[a-z]{2}\s", "", regex=True)
    df_yamal["Opponent"] = df_yamal["Opponent"].str.replace(r"^[a-z]{2}\s", "", regex=True)

    TEAM_NAME_FIXES = {
        "Barcelona": "FC Barcelona",
        "Betis": "Real Betis",
        "Athletic Club": "Athletic de Bilbao",
        "Celta Vigo": "Celta de Vigo",
        "Paris S-G": "Paris Saint-Germain",
        "Shakhtar": "Shakhtar Donetsk",
        "Almeria": "UD Almería",
        "Porto": "FC Porto",
        "Mallorca": "Real Mallorca",
        "Antwerp": "Antwerp",
        "Osasuna": "Osasuna",
        "Napoli": "Napoli",
        "Las Palmas": "Las Palmas",
        "Granada": "Granada",
        "Valencia": "Valencia",
        "Real Sociedad": "Real Sociedad",
        "Atlético Madrid": "Atlético Madrid",
        "Real Madrid": "Real Madrid",
        "Sevilla": "Sevilla",
        "Girona": "Girona",
        "Alavés": "Alavés",
        "Rayo Vallecano": "Rayo Vallecano",
        "Getafe": "Getafe",
        "Cádiz": "Cádiz"
    }

    df_yamal["Squad"] = df_yamal["Squad"].replace(TEAM_NAME_FIXES)
    df_yamal["Opponent"] = df_yamal["Opponent"].replace(TEAM_NAME_FIXES)

    def limpiar_resultado(valor):
        if pd.isna(valor):
            return None
        valor = str(valor).strip()
        if valor.startswith(("W", "D", "L")):
            partes = valor.split(" ")
            return partes[1] if len(partes) > 1 else None
        return valor.replace("–", "-")

    df_yamal["Result"] = df_yamal["Result"].apply(limpiar_resultado)

    COMP_FIXES = {
        "La Liga": "La Liga",
        "Champions Lg": "UEFA Champions League",
        "Copa del Rey": "Copa del Rey",
        "Supercopa de España": "Spanish Super Cup",
        "Friendlies (M)": "International friendly",
        "UEFA Nations League": "UEFA Nations League",
        "UEFA Euro Qualifying": "UEFA Euro Qualification",
        "UEFA Euro": "UEFA Euro"
    }
    df_yamal["Comp"] = df_yamal["Comp"].replace(COMP_FIXES)

    df_cleaned_yamal = pd.DataFrame()
    df_cleaned_yamal["Date"] = df_yamal["Date"]
    df_cleaned_yamal["Season"] = df_yamal["Season"]
    df_cleaned_yamal["Age"] = df_yamal["Age"]
    df_cleaned_yamal["Messi_Team"] = "FC Barcelona"
    df_cleaned_yamal["Home/Away"] = df_yamal["Home/Away"]
    df_cleaned_yamal["Competition"] = df_yamal["Comp"]
    df_cleaned_yamal["Home Team"] = df_yamal.apply(lambda row: row["Squad"] if row["Venue"] == "Home" else row["Opponent"], axis=1)
    df_cleaned_yamal["Result"] = df_yamal["Result"]
    df_cleaned_yamal["Away Team"] = df_yamal.apply(lambda row: row["Opponent"] if row["Venue"] == "Home" else row["Squad"], axis=1)
    df_cleaned_yamal["Lineup"] = df_yamal["Lineup"]

    for col in ["Min", "Gls", "Ast", "CrdY"]:
        df_cleaned_yamal[col] = pd.to_numeric(df_yamal.get(col, 0), errors="coerce").fillna(0).astype(int)

    df_cleaned_yamal.rename(columns={
        "Min": "Minutes",
        "Gls": "Goals",
        "Ast": "Assists",
        "CrdY": "Cards"
    }, inplace=True)

    df_cleaned_yamal.to_csv(output_path, index=False)
    print(f"✅ Datos procesados guardados en: {output_path}")
    if return_df:
        return df_cleaned_yamal

if __name__ == "__main__":
    process_data()
    process_lamine_data()


