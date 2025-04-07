# scraping.py — Messi + Lamine

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import os
import time

# Detectar la raíz del proyecto
project_root = Path(__file__).resolve().parent.parent
messi_raw_path = project_root / "data/raw/messi_raw_data.csv"
lamine_raw_path = project_root / "data/raw/lamine_raw_data.csv"
messi_raw_path.parent.mkdir(parents=True, exist_ok=True)

# -------------------- MESSI --------------------

URL_LIST_MESSI = [
    "https://www.messistats.com/en/games/0/0/all/0/2/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/3/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/4/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/5/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/6/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/7/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/8/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/9/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/10/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/11/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/12/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/13/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/14/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/15/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/16/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/17/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/18/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/19/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/20/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/21/0/t/0/0/0/1",
    "https://www.messistats.com/en/games/0/0/all/0/24/0/t/0/0/0/1",
]

def scrape_messi_data():
    all_data = []

    for url in URL_LIST_MESSI:
        print(f"🌐 Scrapeando Messi: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        headers = [
            "Index", "Date", "Competition", "Home Team", "Result", "Away Team",
            "Lineup", "Minutes", "Goals", "Assists", "Cards", "Jersey", "Extra"
        ]

        data = []
        for row in soup.find_all("tr"):
            cols = [col.text.strip() for col in row.find_all("td")]
            if cols:
                data.append(cols)

        if data:
            df = pd.DataFrame(data, columns=headers[:len(data[0])])
            all_data.append(df)

    if not all_data:
        print("⚠️ No se encontraron datos.")
        return

    df_total = pd.concat(all_data, ignore_index=True)

    if messi_raw_path.exists():
        df_existing = pd.read_csv(messi_raw_path, dtype=str, on_bad_lines='skip')
        df_combined = pd.concat([df_existing, df_total], ignore_index=True)
    else:
        df_combined = df_total

    df_combined.drop_duplicates(subset=["Date", "Home Team", "Away Team"], keep="last", inplace=True)
    df_combined.to_csv(messi_raw_path, index=False, encoding="utf-8")
    print(f"✅ CSV actualizado: {messi_raw_path} con {len(df_combined)} registros.")

# -------------------- LAMINE --------------------

LAMINE_URLS = [
    "https://fbref.com/en/players/82ec26c1/matchlogs/2022-2023/Lamine-Yamal-Match-Logs",
    "https://fbref.com/en/players/82ec26c1/matchlogs/2023-2024/Lamine-Yamal-Match-Logs",
    "https://fbref.com/en/players/82ec26c1/matchlogs/2024-2025/Lamine-Yamal-Match-Logs"
]

def scrape_lamine_data():
    all_data = []

    for url in LAMINE_URLS:
        print(f"🌍 Scrapeando Lamine: {url}")
        try:
            df = pd.read_html(url, attrs={"id": "matchlogs_all"})[0]

            if df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(-1)

            df = df[df["Date"].notna()]
            season = url.split("/")[-2]
            df["Season"] = season
            all_data.append(df)

        except Exception as e:
            print(f"❌ Error en {url}: {e}")

        time.sleep(1)

    if not all_data:
        print("⚠️ No se encontraron datos de Lamine.")
        return

    df_yamal = pd.concat(all_data, ignore_index=True)
    df_yamal.to_csv(lamine_raw_path, index=False)
    print(f"✅ CSV guardado en {lamine_raw_path} con {len(df_yamal)} filas.")

if __name__ == "__main__":
    scrape_messi_data()
    scrape_lamine_data()
