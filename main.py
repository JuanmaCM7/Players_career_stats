
# main.py — Ejecuta scraping y procesamiento completo

import sys
from pathlib import Path

# Añadir carpeta 'src' al path
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
sys.path.append(str(src_path))

from scraping import scrape_messi_data, scrape_lamine_data
from processing import process_data, process_lamine_data
from analysis import run_analysis, run_analysis_lamine

if __name__ == "__main__":
    print("🚀 Iniciando scraping...")
    scrape_messi_data()
    scrape_lamine_data()

    print("\n🧹 Procesando datos...")
    df_messi = process_data(return_df=True)
    df_lamine = process_lamine_data(return_df=True)

    print("\n📊 Análisis Messi:")
    run_analysis(df_messi)

    print("\n📊 Análisis Lamine Yamal:")
    run_analysis_lamine(df_lamine)

    print("\n✅ Todo listo. CSVs generados y análisis completos.")



