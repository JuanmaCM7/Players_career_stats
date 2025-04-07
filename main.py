from src.scraping import scrape_multiple_urls
from src.processing import process_data
from src.analysis import run_all_analyses

def main():
    print("🚀 Iniciando análisis de la carrera de Messi...")

    # Paso 1: Scraping
    print("\n📥 Paso 1: Scrapear datos...")
    df_raw = scrape_multiple_urls()

    # Paso 2: Procesamiento
    print("\n🧹 Paso 2: Procesar datos...")
    df_clean = process_data(return_df=True)

    # Paso 3: Análisis y visualización
    print("\n📊 Paso 3: Generar análisis y gráficos...")
    run_all_analyses(df_clean, save=True)

    print("\n✅ Todo listo. CSVs generados y visualizaciones guardadas en /images.")

if __name__ == "__main__":
    main()


