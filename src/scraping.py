import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_messi_data(url, raw_path="data/raw/messi_raw_data.csv"):
    """Scrapea los datos de Messi desde una URL y los agrega a un CSV sin duplicar registros."""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    
    # Extraer encabezados correctamente formateados
    headers = [
        "Index", "Date", "Competition", "Home Team", "Result", "Away Team",
        "Lineup", "Minutes", "Goals", "Assists", "Cards", "Jersey", "Extra"
    ]

    # Extraer datos de la tabla
    for row in soup.find_all("tr"):
        cols = [col.text.strip() for col in row.find_all("td")]
        if cols:
            data.append(cols)

    df_new = pd.DataFrame(data, columns=headers[:len(data[0])])  # Ajustar columnas dinámicamente

    # Verificar si el CSV ya existe
    if os.path.exists(raw_path):
        try:
            df_old = pd.read_csv(raw_path, on_bad_lines='skip', dtype=str)
        except pd.errors.ParserError as e:
            print(f"⚠️ Error leyendo el archivo CSV: {e}")
            df_old = pd.DataFrame(columns=headers)

        # Asegurar que las columnas coinciden antes de concatenar
        if not df_old.empty and list(df_old.columns) != list(df_new.columns):
            print(f"⚠️ Diferente estructura de columnas entre el archivo existente y los nuevos datos.")
            return
        
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    # Eliminar duplicados basados en Date, Home Team y Away Team
    df.drop_duplicates(subset=["Date", "Home Team", "Away Team"], keep='last', inplace=True)

    # Guardar los datos en modo append sin sobrescribir encabezados si ya existe
    df.to_csv(raw_path, mode='w', header=True, index=False, encoding="utf-8")

    print(f"📂 Datos actualizados y guardados en {raw_path}")

    return df
