# Proyecto: Análisis Comparativo de las Carreras de Messi y Lamine Yamal

Este proyecto forma parte de una entrega académica que integra los conocimientos adquiridos en procesos ETL, análisis exploratorio de datos (EDA), estadística descriptiva, visualización interactiva y presentación narrativa de resultados.

El objetivo principal es **extraer, procesar, analizar y visualizar** los datos de carrera de **Lionel Messi** y **Lamine Yamal**, comparando sus trayectorias desde una perspectiva estadística y visual.

---

## 🌍 Contexto y Justificación

Ambos jugadores representan momentos muy distintos del espectro futbolístico: uno en el ocaso de su carrera con una trayectoria legendaria; el otro, una promesa emergente. Este contraste lo hace ideal para aplicar herramientas de ciencia de datos:

- Evaluar **rendimiento individual** y tendencias temporales.
- Comparar el impacto de la edad, los equipos y el contexto de los partidos.
- Aplicar visualizaciones interactivas para comunicar hallazgos de forma clara.

---

## 🔄 Flujo del Proyecto y Componentes

### 1. Extracción de Datos (ETL)

**Archivo:** `src/scraping.py`

- **Messi:** datos obtenidos de [messistats.com](https://messistats.com), temporada por temporada.
- **Lamine Yamal:** datos de partidos extraídos de [fbref.com](https://fbref.com) mediante `pandas.read_html()`.
- Se automatiza la descarga y guardado en formato `.csv` en la carpeta `data/raw/`.
- Uso de `time.sleep` y validaciones para evitar bloqueos por scraping.

> Resultado: `messi_raw_data.csv` y `lamine_raw_data.csv`

---

### 2. Procesamiento y Limpieza

**Archivo:** `src/processing.py`

- Limpieza de columnas con saltos de línea o nombres inconsistentes.
- Conversión de fechas al formato datetime y generación de columna "Season".
- Cálculo de **edad** al momento de cada partido.
- Asignación del equipo correspondiente según año y competición.
- Clasificación local/visitante, y determinación del rival.
- Homologación de nombres de clubes, resultados y competiciones para Lamine.

> Resultado: `messi_cleaned_data.csv` y `lamine_cleaned_data.csv` en `data/processed/`

---

### 3. Análisis Estadístico y Exploratorio (EDA)

**Archivo:** `src/analysis.py`

El análisis se divide entre Messi y Lamine, y genera tanto estadísticas como gráficas:

#### ✅ Messi
- **Total de goles y asistencias**
- **Goles por año calendario** y **temporada futbolística**
- **Promedio de goles por partido y por minuto**
- **Goles por competición (Liga, Champions, etc.)**
- **Comparación local vs visitante**
- **Distribución mensual de goles**

#### ✅ Lamine
- Total de partidos, goles y asistencias
- Goles y asistencias por edad
- Minutos jugados por temporada
- Distribución de partidos como titular vs suplente
- Local vs visitante
- Minutos jugados por edad (gráfico de dispersión)

> Las imágenes generadas se guardan en la carpeta `images/`

---

### 4. Dashboard Interactivo (Power BI)

**Archivo:** `dashboard/Players_career_data.pbix`

Este archivo contiene un informe en Power BI con:

- Indicadores clave (KPI) como promedio de goles, asistencias, edad, etc.
- Visualizaciones temporales: líneas de goles/asistencias por temporada.
- Comparación por tipo de competición y condición de juego (local/visitante).
- Análisis de madurez deportiva (edad vs minutos jugados).

Este dashboard complementa las visualizaciones estáticas con interactividad y permite un storytelling fluido.

---

### 5. Notebook de Pruebas

**Archivo:** `notebooks/Tests.ipynb`

Cuaderno de pruebas usado para explorar datos de forma rápida, probar funciones individuales o validar formatos durante el desarrollo.

---

### 6. Entorno y Dependencias

**Archivos:**
- `requirements.txt`
- `environment.yml`

Incluyen todas las dependencias necesarias para reproducir el entorno: pandas, matplotlib, beautifulsoup4, requests, etc.

---

## 📆 Estructura del Repositorio

```
proyecto/
├── dashboard/                      # Archivo .pbix (Power BI)
├── designs/                        # Imagen de portada y branding
├── data/
│   ├── raw/                        # Datos obtenidos por scraping
│   └── processed/                 # Datos limpios y transformados
├── images/                         # Gráficas estáticas generadas
├── notebooks/
│   └── Tests.ipynb                # Exploración preliminar
├── src/
│   ├── scraping.py                # Obtención de datos web
│   ├── processing.py              # Limpieza y transformación
│   ├── analysis.py                # Análisis y visualizaciones
│   ├── db.py                      # Conexión con base de datos (opcional)
│   └── main.py                    # Flujo ejecutable del proyecto
├── requirements.txt
├── environment.yml
├── Instrucciones_proy_abril.md    # Enunciado del proyecto
└── README.md                      # Documentación general
```

---

## 🤖 Reproducibilidad

```bash
# 1. Clona el repositorio
$ git clone https://github.com/tu_usuario/tu_repositorio.git
$ cd tu_repositorio

# 2. Crea entorno e instala dependencias
$ pip install -r requirements.txt

# 3. Ejecuta el proyecto completo (si main.py está configurado)
$ python src/main.py
```

---

## 🔹 Resultados Destacados

- **Messi**: supera los 700 goles con un promedio de un gol cada XX minutos.
- **Lamine**: destaca por su carga de minutos a edad temprana, especialmente en selección.
- Los gráficos comparativos permiten visualizar estilos de carrera opuestos pero igualmente prometedores.
- Se observa un patrón de mayor productividad de Messi como local, mientras que Lamine mantiene consistencia en ambos contextos.

---

## 📈 Capturas y Visuales

> Aquí puedes incrustar capturas del dashboard, de las gráficas generadas o un video/gif de navegación por el dashboard en Power BI.

Ejemplo:
```
![Dashboard Overview](designs/BG%20profile.png)
```

---

## 💚 Transparencia

Este proyecto ha sido desarrollado de forma individual, con comprensión plena de cada línea de código, incluyendo funciones sugeridas por IA. Se ha hecho especial énfasis en la limpieza de datos, validación de resultados y narrativa visual.

---

## 🎓 Autor

- **Nombre:** Juan Manuel Cano Mayor
- **Email:** juacanom@gmail.com
- **Curso:** Data Science & AI - Abril 2025
- **Profesorado:** Evolve Academy

---

¡Gracias por tu tiempo y atención! 🌟



