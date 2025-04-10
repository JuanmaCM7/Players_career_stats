import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# -------------------- FUNCIONES AUXILIARES --------------------

# Determina el equipo del jugador en base a temporada, competición y equipos implicados
def deducir_equipo_jugador(row, jugador="Messi"):
    temporada = row["Season"]
    comp = str(row["Competition"])
    home = row["Home Team"]
    away = row["Away Team"]

    if pd.isna(temporada) or pd.isna(comp):
        return "Unknown"

    if jugador == "Messi":
        # Argentina en cualquier competición internacional
        if "argentina" in comp.lower() or home == "Argentina" or away == "Argentina":
            return "Argentina"
        elif temporada <= "2020-2021":
            return "FC Barcelona"
        elif temporada in ["2021-2022", "2022-2023"]:
            return "Paris Saint-Germain"
        elif temporada >= "2023-2024":
            return "Inter Miami CF"
    elif jugador == "Lamine":
        # Si el partido es con selección, asignamos "Spain"
        if "spain" in comp.lower() or home == "Spain" or away == "Spain":
            return "Spain"
        else:
            return "FC Barcelona"

    return "Unknown"

# Extrae el equipo rival según la posición del jugador (local/visitante)
def obtener_rival(row):
    player_team = row["Player_Team"]
    home = row["Home Team"]
    away = row["Away Team"]

    if pd.isna(player_team) or pd.isna(home) or pd.isna(away):
        return None

    if player_team == home and away != player_team:
        return away
    elif player_team == away and home != player_team:
        return home
    else:
        return None

# -------------------- MESSI --------------------

def process_data(input_rel="data/raw/messi_raw_data.csv", output_rel="data/processed/messi_cleaned_data.csv", return_df=False, decimal=","):
    # Crea rutas relativas a raíz del proyecto
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / input_rel
    output_path = project_root / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Carga CSV crudo
    df = pd.read_csv(input_path)

    # Limpieza de columnas que vienen con saltos de línea
    df["Competition"] = df["Competition"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)
    df["Lineup"] = df["Lineup"].apply(lambda x: x.split("\n")[1].strip() if isinstance(x, str) and "\n" in x else x)

    # Eliminar columnas innecesarias si existen
    df.drop(columns=["Index", "Jersey", "Extra"], inplace=True, errors="ignore")

    # Asegurar que valores numéricos estén bien tipados
    for col in ["Goals", "Assists", "Cards", "Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convertir fechas
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce", dayfirst=True)

    # Crear columna de temporada (usando lógica de temporada futbolística)
    def asignar_temporada(fecha):
        if pd.isna(fecha):
            return None
        if datetime(2019, 8, 15) <= fecha <= datetime(2020, 8, 14):
            return "2019-2020"
        year = fecha.year
        return f"{year}-{year + 1}" if fecha.month >= 8 else f"{year - 1}-{year}"

    df["Season"] = df["Date"].apply(asignar_temporada)

    # Edad de Messi en cada partido
    birthdate = pd.to_datetime("1987-06-24")
    df["Age"] = df["Date"].apply(lambda d: round((d - birthdate).days / 365.25, 2) if pd.notna(d) else None)
    df["Player"] = "Leo Messi"  # columna fija de jugador

    # Determinar equipo y local/visitante
    df["Player_Team"] = df.apply(lambda row: deducir_equipo_jugador(row, "Messi"), axis=1)
    df["Home/Away"] = df.apply(lambda row: "Home" if row["Home Team"] == row["Player_Team"] else "Away", axis=1)

    # Obtener nombre del equipo rival
    df["Rival_Team_Name"] = df.apply(obtener_rival, axis=1)

    # Formatear edad con coma como decimal
    df["Age"] = df["Age"].apply(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")

    # Reordenar columnas
    cols = ["Date", "Season", "Age", "Player", "Player_Team", "Home/Away", "Competition", "Home Team", "Result", "Away Team", "Rival_Team_Name", "Lineup", "Minutes", "Goals", "Assists", "Cards"]
    df = df[cols]

    # Guardar CSV limpio
    df.to_csv(output_path, index=False, sep=",", decimal=decimal, encoding="utf-8")
    print(f"✅ Datos procesados guardados en: {output_path}")
    if return_df:
        return df

# -------------------- LAMINE --------------------

def process_lamine_data(input_rel="data/raw/lamine_raw_data.csv", output_rel="data/processed/lamine_cleaned_data.csv", return_df=True, decimal=","):
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
    df_yamal["Lineup"] = df_yamal["Start"].apply(lambda s: "Starter" if s == "Y" else "Substitute")

    # Limpiar nombres de equipos (ej: "eng England" -> "England")
    df_yamal["Squad"] = df_yamal["Squad"].str.replace(r"^[a-z]{2,3}\s", "", regex=True)
    df_yamal["Opponent"] = df_yamal["Opponent"].str.replace(r"^[a-z]{2,3}\s", "", regex=True)

    # Corrección de nombres de equipos
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
        "Cádiz": "Cádiz",
        "Bayern Munich": "Bayern München",
        "Young Boys": "Young Boys",
        "Dortmund": "Borussia Dortmund",
        "Red Star": "Red Star Belgrade",
        "Valladolid": "Real Valladolid",
        "Andorra": "Andorra",
        "Cyprus": "Cyprus",
        "Georgia": "Georgia",
        "Denmark": "Denmark",
        "Serbia": "Serbia",
        "Monaco": "AS Monaco",
        "Atalanta": "Atalanta",
        "England": "England",
        "Northern Ireland": "Northern Ireland"
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
        if valor.isdigit():
            return f"{valor}-{valor}"
        return valor.replace("–", "-")

    df_yamal["Result"] = df_yamal["Result"].apply(limpiar_resultado)

    # Correcciones de nombres de competiciones
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

    # Construcción del nuevo dataframe limpio
    df_cleaned = pd.DataFrame()
    df_cleaned["Date"] = df_yamal["Date"]
    df_cleaned["Season"] = df_yamal["Season"]
    df_cleaned["Age"] = df_yamal["Age"].apply(lambda x: f"{x:.2f}".replace(".", ",") if pd.notna(x) else "")
    df_cleaned["Player"] = "Lamine Yamal"

    df_cleaned["Home Team"] = df_yamal.apply(lambda row: row["Squad"] if row["Venue"] == "Home" else row["Opponent"], axis=1)
    df_cleaned["Away Team"] = df_yamal.apply(lambda row: row["Opponent"] if row["Venue"] == "Home" else row["Squad"], axis=1)
    df_cleaned["Competition"] = df_yamal["Comp"]
    df_cleaned["Result"] = df_yamal["Result"]
    df_cleaned["Lineup"] = df_yamal["Lineup"]

    # Conversión y renombrado de columnas numéricas
    for col in ["Min", "Gls", "Ast", "CrdY"]:
        df_cleaned[col] = pd.to_numeric(df_yamal.get(col, 0), errors="coerce").fillna(0).astype(int)

    df_cleaned.rename(columns={
        "Min": "Minutes",
        "Gls": "Goals",
        "Ast": "Assists",
        "CrdY": "Cards"
    }, inplace=True)

    # Deducción del equipo de Lamine
    df_cleaned["Player_Team"] = df_cleaned.apply(lambda row: "Spain" if "international" in row["Competition"].lower() else "FC Barcelona", axis=1)
    df_cleaned["Home/Away"] = df_cleaned.apply(lambda row: "Home" if row["Home Team"] == row["Player_Team"] else "Away", axis=1)
    df_cleaned["Rival_Team_Name"] = df_cleaned.apply(lambda row: row["Away Team"] if row["Player_Team"] == row["Home Team"] else row["Home Team"], axis=1)

    # Guardar CSV limpio
    df_cleaned.to_csv(output_path, index=False, sep=",", encoding="utf-8", decimal=decimal)
    print(f"✅ Datos procesados guardados en: {output_path}")
    if return_df:
        return df_cleaned

# -------------------- EJECUCIÓN --------------------

if __name__ == "__main__":
    process_data()
    process_lamine_data()
