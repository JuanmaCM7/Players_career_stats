from src.scraping import scrape_multiple_urls
from src.processing import process_data
from src.analysis import run_analysis  # <- esta función ejecuta tus visualizaciones

def main():
    print("🚀 Scrapeando datos...")
    scrape_multiple_urls()
    
    print("🧼 Procesando datos...")
    df = process_data(return_df=True)
    
    print("📊 Ejecutando análisis...")
    run_analysis(df)

    print("✅ Proyecto ejecutado correctamente.")

if __name__ == "__main__":
    main()



