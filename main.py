# main.py — Ejecuta scraping, procesamiento y análisis para Messi y Lamine Yamal

import sys
from pathlib import Path

# -----------------------------------------------
# 📁 CONFIGURACIÓN DEL ENTORNO
# -----------------------------------------------

# Detectamos la raíz del proyecto
project_root = Path(__file__).resolve().parent

# Añadimos la carpeta 'src' al path para poder importar módulos personalizados
src_path = project_root / "src"
sys.path.append(str(src_path))

# -----------------------------------------------
# 📦 IMPORTACIÓN DE FUNCIONES PRINCIPALES
# -----------------------------------------------

# Scraping: obtener datos crudos desde la web
from scraping import scrape_messi_data, scrape_lamine_data

# Procesamiento: limpiar, normalizar y enriquecer los datos
from processing import process_data, process_lamine_data

# Análisis: generar métricas, visualizaciones y gráficos
from analysis import run_analysis, run_analysis_lamine

# -----------------------------------------------
# ▶️ EJECUCIÓN DEL FLUJO COMPLETO
# -----------------------------------------------

if __name__ == "__main__":
    # Paso 1: Scrapeo de datos desde webs externas
    print("🚀 Iniciando scraping...")
    scrape_messi_data()
    scrape_lamine_data()

    # Paso 2: Procesamiento y limpieza de datos
    print("\n🧹 Procesando datos...")
    df_messi = process_data(return_df=True, decimal=",")
    df_lamine = process_lamine_data(return_df=True, decimal=",")

    # Paso 3: Análisis y visualización de resultados
    print("\n📊 Análisis Messi:")
    run_analysis(df_messi)

    print("\n📊 Análisis Lamine Yamal:")
    run_analysis_lamine(df_lamine)

    # Fin del proceso
    print("\n✅ Todo listo. CSVs generados y análisis completos.")



