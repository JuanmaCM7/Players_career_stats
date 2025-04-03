# Proyecto I - EDA / ETL

Este proyecto tiene como objetivo enseñar las bases de un flujo completo de análisis de datos: desde la adquisición de datos (ETL), el análisis exploratorio (EDA), la descripción estadística, hasta la creación de dashboards en Power BI o Tableau.

## Objetivos

- Aplicar un proceso de ETL sobre un conjunto de datos real.
- Realizar un análisis exploratorio de los datos.
- Generar estadísticas descriptivas.
- Crear visualizaciones y dashboards interactivos.
- Organizar el proyecto en un repositorio estructurado.
- Gestionar entornos reproducibles con `requirements.txt` o similar.

## Estructura del Proyecto

```
# Sugerencia, puee llevar otra estructura

├── data/               # Archivos de datos sin procesar y procesados
│   ├── raw/
│   └── processed/
├── notebooks/          # Notebooks de análisis y pruebas
├── dashboards/         # Archivos de Power BI (.pbix) o Tableau
├── src/                # Scripts Python (ETL, estadísticas, etc.)
│   ├── etl.py
│   ├── eda.py
│   └── stats.py
├── requirements.txt    # Dependencias del proyecto
├── .gitignore
└── README.md
```


### 0. Formulación de preguntas de investigación

Antes de comenzar el análisis, es esencial definir claramente los objetivos y las preguntas que se desean responder con los datos. Estas preguntas guiarán todo el flujo del proyecto.

Ejemplos:

- ¿Qué factores están asociados con el aumento o disminución de X?
- ¿Cuáles son las tendencias más relevantes en el tiempo?
- ¿Qué diferencias hay entre distintos grupos (género, edad, regiones, etc.)?
- ¿Podemos predecir una variable de interés con base en los datos disponibles?
- ¿Existen patrones o relaciones no evidentes que puedan descubrirse mediante análisis exploratorio?


### 2. Exploración, transformación y estadística

#### 2.1 Exploración

Entender la estructura, calidad y características básicas de los datos. Algunas preguntas clave que guían esta etapa son:

- ¿Qué tipos de datos tengo? (numéricos, categóricos, fechas, texto libre, etc.)
- ¿Cuál es el dominio del dataset? ¿Conozco el contexto de las variables?
- ¿La fuente de datos es fiable y completa?
- ¿Los datos están agregados o son individuales (nivel de granularidad)?
- ¿Hay valores perdidos? ¿Cuál es su proporción y distribución?
- ¿Existen duplicados o registros anómalos?
- ¿Las variables tienen una distribución esperada? ¿Existen outliers?
- ¿Los formatos de fechas y categorías están normalizados?
- ¿Hay incoherencias entre columnas? (ej. fechas de nacimiento posteriores a eventos)
- ¿Cuáles son las estadísticas básicas (media, mediana, moda, etc.)?

#### 2.2 Estadística

Una vez que comprendemos la estructura básica de los datos, debemos aplicar medidas estadísticas para describir su comportamiento y distribución. Esto incluye:

##### Descriptiva
- Estadísticas de tendencia central: media, mediana, moda
- Medidas de dispersión: rango, varianza, desviación estándar, percentiles
- Distribuciones: histograma, boxplot, KDE
- Estadísticas por subgrupos (segmentación por género, edad, región, etc.)

  
##### Inferencial
- Correlaciones entre variables numéricas
- Contraste de hipótesis: por ejemplo, ¿es diferente la edad del segmento A a la del B?
- Plantear modelo de regresión lineal sobre una variable dependiente en función del resto de datos (por ejemplo  precio de vivienda en función de m2 o numero de habitaciones)
- Unos resultados no-concluyentes, no confirmatorios con la pregunta de investigación inicial o con una muestra muy pequeña son igualmente necesarios siempre que se expliciten las limitaciones. Aunque tengas pocos datos: intenta plantear igualmente estos análisis.

Estas métricas permiten detectar patrones, comportamientos anómalos, y relaciones entre variables que pueden ser clave para responder a las preguntas de investigación.

#### 2.3 Transformación

Transformación de los datos para:
- Poder llevar a cabo los puntos anteriores
- Para poder visualizar los datos con python
- Para poder juntar datos
  - Como hacer un join/merge en pandas
  - Como juntar datos extraídos por una API con un csv
  - Como juntar datos extraídos por web-scrapping con una API
  
Esta etapa puede realizarse con visualizaciones simples y descripciones estadísticas preliminares.

## 3. Descripción a través de SQL (opcional)
Si los datos lo permiten:
- Cargaremos los datos transformados y limpios en tablas de SQL
- No tienen por qué ser tablas relacionadas
- La carga puede ser manual o programática con uan conexión a través de python
- Es un paso que no es necesario, no interrumpe la continuidad del proyecto y es una excusa para poder describir los datos con otra sintaxis y en otra herramienta. 
- Si conseguimos subir los datos (quizá dé problemas de formato), guardaremos un archivo `description.sql` que contenga las queries que nos describan, resuman y expliquen los datos. Estas queries deberían responder a la sección 2 en la medida de lo posible
- Lo dejaremos para el final


## 4. Dashboarding
- Crearemos un dashboard en Tableau o en PowerBI
- Este dashboard tiene que tener un hilo narrativo que empiece explicando las preguntas de investigación y acabe con las conclusiones
- Las visualizaciones tienen que ser auto-descriptivas, sencillas, significativas y que respondan a las preguntas


## 5. Pipeline (opcional)

Si tu proyecto sigue un proceso de pipeline, asegúrate de tener un archivo ejecutable que lo desencadene.


## 6. Repositorio
- Necesitará tener una estructura similar que garantice la modularización del código
- No deberá tener archivos que generen reuido (.DS_Store, .ipynb_checkpoints, __pycache__, etc). 
- No deberá tener archivos como `.env` o que contengan contraseñas o tokens de API


## 7. Documentación
- README.md
- Comentarios en el código (propios)
- Docstrings: funciones documentadas
- Más README.md, siempre se puede completar más


# EXTRA: tips
- Si tu proyecto tiene un arhcivo ejecutable (`main.py`) que extrae, procesa, etc: graba tu pantalla, guarda el vídeo como gif e incr´sutalo en el README.md
- Para el dashboard, haz lo mismo: graba partes de la interactividad del dashboard, guarda como gif e incrusta.
- Si generas gráficas con python, expórtalas y guárdalas en el proyecto. También las puedes incluir en el README.md.
- Haz commit y push con frecuencia. No quieres perder días de trabajo.
- De verdad, haz commits.
- Utiliza el ["rubber duck debugging"](https://en.wikipedia.org/wiki/Rubber_duck_debugging) cuando te atasques o simplemente pierdas el foco del proyecto
- Es un proceso iterativo, no esperes que sea lineal. 
- Igual que necesitas poder explicar el código, necesitarás poder defender la interpretación de los estadísticos: las escalas de la correlación, coeficientes, error, p valor, etc.


# Checklist
#### Proceso
- Has planteaddo preguntas de investigación ✅
- Has explorado los datos ✅
- Has descrito los datos estadísticamente ✅ 
- Has visualizado los datos ✅
- Has aplicado transformaciones ✅

#### Código
- Has encapsulado el código (en funciones) ✅
- Has modularizado el código (en archivos de python) ✅
- Las funciones están descritas con un docstring ✅

#### Repositorio
- Has separado las definiciones y las invocaciones ✅
- Los archivos están agrupados por categoría (código, imágenes, datos, etc) ✅

#### Documentación
- Sólo leyendo el README.md, cualquier persona sabe qué has hecho ✅
- El README.md está apoyado con imágenes, gifs, etc ✅

#### Replicabilidad
- Hay un requirements.txt generado ✅
- Hay instrucciones de cómo replicar el proyecto ✅ (git clone, pip install -r requirements.txt, pyhon main.py, etc)

#### Comunicación
- Tienes un dashboard ✅

#### Entrega
- Haces llegar tu enlace **público** de github ✅



# FAQ
- Los proyectos son individuales
- El tiempo de presentación es limitado: practica, ajústate al tiempo y asegúrate que transmites la información que necesitas transmitir. Menos es más. Transmitir lo necesario en poco tiempo a veces es más valioso.
- La decisión correcta es la que te acerca al objetivo planteado inicialmente.
- Si utilizas código ajeno o generado por IA, asegúrate de entenderlo. Tienes que poder explicar y defender el código.
- Puedes, y te animamos, a que utilices herramientas no vistas durante la formación. Es posible que no podamos darte apoyo si es una herramienta desconocida para nosotros, pero encantados de aprender y de apoyarte.




# Ejemplos de proyecto

### 1. Predicción de Aceptación de Depósitos en Campañas Bancarias
**Fuente de datos**: [Bank Marketing Dataset (UCI)](https://archive.ics.uci.edu/ml/datasets/bank+marketing)

**Objetivo**:  
Predecir si un cliente aceptará un depósito a plazo fijo en función de sus características personales y de comportamiento.

**Actividades**:
- Análisis exploratorio: distribuciones, valores nulos, correlaciones.
- Segmentación: educación, edad, duración de llamada.
- Modelado: Regresión Logística, Árboles de Decisión.
- Evaluación: matriz de confusión, precisión, recall.
- Aplicación: optimizar campañas contactando solo a clientes con alta probabilidad de aceptación.

---

### 2. Predicción de Precios de Acciones con Series Temporales
**Fuente de datos**: [Yahoo Finance](https://finance.yahoo.com/)

**Objetivo**:  
Predecir el precio de cierre de acciones a partir de datos históricos.

**Actividades**:
- Extracción y limpieza de datos desde la API.
- Análisis de tendencias y estacionalidades.
- Modelado: ARIMA, Prophet.
- Evaluación: RMSE, MAE.
- Aplicación: soporte a decisiones de inversión.

---

### 3. Predicción de Rotación de Empleados en Empresas
**Fuente de datos**: [IBM HR Analytics Dataset (Kaggle)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

**Objetivo**:  
Predecir qué empleados tienen mayor probabilidad de abandonar la empresa.

**Actividades**:
- EDA: correlaciones, distribuciones, satisfacción laboral.
- Modelado: Random Forest, Regresión Logística.
- Evaluación: precisión, F1-score.
- Aplicación: prevenir fugas de talento y diseñar estrategias de retención.

---

### 4. Detección de Fraude en Transacciones con Tarjeta de Crédito
**Fuente de datos**: [Credit Card Fraud Detection Dataset (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

**Objetivo**:  
Identificar transacciones fraudulentas usando modelos de clasificación.

**Actividades**:
- Análisis de desbalanceo de clases.
- Técnicas de balanceo: SMOTE, undersampling.
- Modelado: XGBoost, Random Forest.
- Evaluación: ROC-AUC, precisión, recall.
- Aplicación: sistemas antifraude en banca en tiempo real.

---

### 5. Análisis del mercado laboral
**Fuente de datos**: InfoJobs, Adzuna, [INE](https://www.ine.es/), scraping portales empleo.

**Preguntas**:
- ¿Qué sectores tienen más ofertas?
- ¿Cómo varía el salario por región?
- ¿Qué habilidades son más demandadas?

**Dashboard**: evolución temporal, sectores top, mapa de calor regional.

---

### 6. Consumo energético en España
**Fuente de datos**: [REE](https://www.ree.es/), [ESIOS](https://www.esios.ree.es/)

**Preguntas**:
- ¿Cuándo se consume más energía?
- ¿Hay relación con la temperatura?
- ¿Qué diferencias hay entre comunidades?

**Dashboard**: líneas de consumo, comparativa estacional, barras por sector.

---

### 7. Análisis de Accidentes de Tráfico
**Fuente de datos**: [DGT](https://www.dgt.es/), open data europeo.

**Preguntas**:
- ¿Cuáles son los factores más asociados a accidentes graves?
- ¿En qué días/horas ocurren más?
- ¿Qué diferencias hay por tipo de vehículo o conductor?

**Dashboard**: mapa interactivo, histogramas, KPIs.

---

### 8. Análisis de Precios de Vivienda
**Fuente de datos**: Idealista (scraping), [INE](https://www.ine.es/), Catastro.

**Preguntas**:
- ¿Dónde están las viviendas más caras?
- ¿Qué factores influyen más en el precio?

**Dashboard**: mapa de calor, boxplots, comparativas por provincia.

---

### 9. Opiniones de Clientes sobre Productos o Servicios
**Fuente de datos**: Amazon, TripAdvisor, Google Maps (scraping)

**Preguntas**:
- ¿Qué temas aparecen más en las opiniones?
- ¿Cómo ha cambiado el sentimiento a lo largo del tiempo?

**Dashboard**: wordcloud, evolución del sentimiento, opiniones destacadas.

---

## Fuentes de datos sugeridas

- [datos.gob.es](https://datos.gob.es/)
- [INE](https://www.ine.es/)
- [Open Data EU](https://data.europa.eu/)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
