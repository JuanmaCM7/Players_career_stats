import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Detectar la raíz del proyecto
project_root = Path(__file__).resolve().parent.parent
raw_path = project_root / "data/raw/messi_raw_data.csv"
raw_path.parent.mkdir(parents=True, exist_ok=True)

# Lista de URLs que querés scrapear
URL_LIST = [
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

def scrape_messi_data(url):
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

    if not data:
        return pd.DataFrame()  # Nada que agregar

    df_new = pd.DataFrame(data, columns=headers[:len(data[0])])
    return df_new

def scrape_multiple_urls(url_list=URL_LIST):
    all_data = []

    for url in url_list:
        print(f"🌐 Scrapeando: {url}")
        df_url = scrape_messi_data(url)
        if not df_url.empty:
            all_data.append(df_url)

    if not all_data:
        print("⚠️ No se encontraron datos.")
        return

    df_total = pd.concat(all_data, ignore_index=True)

    if raw_path.exists():
        df_existing = pd.read_csv(raw_path, dtype=str, on_bad_lines='skip')
        df_combined = pd.concat([df_existing, df_total], ignore_index=True)
    else:
        df_combined = df_total

    # Eliminar duplicados por campos clave
    df_combined.drop_duplicates(subset=["Date", "Home Team", "Away Team"], keep="last", inplace=True)
    df_combined.to_csv(raw_path, index=False, encoding="utf-8")
    print(f"✅ CSV actualizado: {raw_path} con {len(df_combined)} registros.")
    return df_combined
