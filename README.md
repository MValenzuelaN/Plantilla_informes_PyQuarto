# 📊 Plantilla de Informes Automáticos en PyQuarto

[![Quarto](https://img.shields.io/badge/Quarto-%234A90E2.svg?style=for-the-badge&logo=quarto&logoColor=white)](https://quarto.org/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Polars](https://img.shields.io/badge/Polars-%233079ab.svg?style=for-the-badge&logo=polars&logoColor=white)](https://pola.rs/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-%23E25A1C.svg?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)

Una plantilla diseñada para la creación estructurada de informes interactivos de analítica y ciencia de datos. Utiliza **Quarto** como motor de renderizado y **Python** para la lógica computacional y visualización de datos.

Este repositorio proporciona un entorno base configurado para facilitar la generación de reportes y centralizar herramientas útiles para el trabajo diario de analítica de datos.

---

## 🌟 Características Principales

*   **Diseño Dual Adaptativo**: Soporte para temas claro y oscuro (`Flatly` / `Darkly`) que permite alternar la visualización con un clic en la esquina superior derecha del reporte.
*   **Interactividad en Bloques de Código**:
    *   Código plegable/desplegable por defecto (`code-fold: true`).
    *   Números de línea y enlaces rápidos de copiado.
    *   Extensión integrada de **Pantalla Completa** (`code-fullscreen`) para expandir y leer con comodidad bloques de código extensos.
*   **Reportes Auto-Contenidos**: Compilación a un único archivo HTML (`embed-resources: true`) que incrusta todo el CSS, Javascript e imágenes. Facilita compartir el archivo de manera directa por correo, chat o almacenamiento local.
*   **Marca de Agua de Autoría**: Firma sutil en el pie de página que indica la procedencia de la plantilla y enlaza al perfil de GitHub del desarrollador.
*   **Tabla de Contenidos**: Menú lateral izquierdo auto-generado que se desplaza de manera sincronizada al navegar por las secciones del informe.

---

## 📂 Estructura del Repositorio

```bash
├── Informe.qmd                      # Plantilla principal del informe de analítica
├── Inicialización.qmd                # Centralización de librerías y funciones utilitarias
├── Informe.html                     # Copia compilada auto-contenida del reporte de ejemplo
├── css/
│   ├── styles.css                   # Estilos visuales complementarios (topbar y cuerpo)
│   └── footer-watermark.html        # Estructura y estilos de la firma/marca de agua en el pie de página
├── Documentación_plantilla/
│   ├── Guia_Quarto.html             # Guía de referencia sobre el uso y sintaxis de Quarto
│   ├── Instalar_Dependencias.bat    # Script de automatización de instalación en Windows
│   └── scripts/
│       ├── generar_requerimientos.py # Script que extrae imports y genera requirements.txt
│       └── requirements.txt         # Lista de paquetes de Python detectados
└── _extensions/                     # Extensiones de Quarto incorporadas
    └── shafayetShafee/
        └── code-fullscreen          # Extensión Lua/JS para ver bloques de código en pantalla completa
```

---

## 🛠️ Utilidades de Analítica (`Inicialización.qmd`)

Al incluir [`Inicialización.qmd`](file:///c:/Users/elitebook%20hp/Documents/GitHub/Plantilla_informes/Inicialización.qmd) en tu reporte principal, se cargan por defecto un conjunto de librerías comunes y tres funciones utilitarias de análisis:

### 1. `pretty_table` (Pseudo-tibble HTML)

Visualizador interactivo de tablas de datos en formato HTML que simula las características de los *tibbles* en R. Detecta automáticamente si la fuente es un DataFrame de **Pandas, Polars o PySpark** y renderiza:
*   Un indicador de la librería de origen (`Pandas`, `Polars` o `Spark`).
*   Las dimensiones de la tabla y número de filas restantes ocultas.
*   Etiquetas (*badges*) de color por columna según el **tipo de variable** (String, Float, Integer, Date, Boolean, etc.).
*   Botones para exportar y descargar el contenido de la tabla directamente en formatos **CSV, Excel, HTML (preservando el estilo visual) o Parquet**.
*   Resaltado condicional opcional de filas (`highlight_col`) o columnas (`highlight_cols`) mediante colores pasteles suaves para facilitar la lectura de los datos.

**Ejemplo de uso:**
```python
# Mostrar las primeras 15 filas, coloreando celdas según los valores de la columna 'Estado'
pretty_table(
    data=df_polars,
    n=15,
    title="Análisis de Ventas",
    highlight_col="Estado",
    highlight_palette={"Completado": "#E6F6FF", "Pendiente": "#FFF9E6", "Cancelado": "#FFF5F5"},
    filename_base="ventas_periodo"
)
```

---

### 2. `query_to_df` (Consulta SQL con Carga por Bloques)

Función diseñada para interactuar con bases de datos relacionales (como SQL Server) a través de `pyodbc`. Incorpora lógica para mitigar el consumo de memoria en consultas extensas.
*   Permite definir el DataFrame resultante deseado (**Polars** o **Pandas**).
*   Soporta extracción por lotes (`chunksize`) para no sobrecargar la memoria RAM.
*   Permite retornar un generador/iterador de DataFrames (`return_iter=True`) en caso de requerir un flujo de streaming/procesamiento ligero registro a registro.

**Ejemplo de uso:**
```python
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=MI_SERVIDOR;Database=MI_BD;Trusted_Connection=yes;"
query = "SELECT * FROM Ventas.Historico"

# Cargar en bloques de 50,000 registros y concatenar directamente a Polars
df_ventas = query_to_df(
    sql=query,
    connection_string=conn_str,
    engine="polars",
    chunksize=50000
)
```

---

### 3. `boxhist_interactivo` (Dashboard Univariado)

Combina visualización y análisis estadístico en un único dashboard interactivo de **Plotly** y **Scipy**. Su objetivo es simplificar la exploración rápida de variables numéricas mediante:
*   **Histograma de densidad**: Barras interactivas agrupadas y apiladas en proporción a la muestra categórica (`color_var`), de modo que el histograma desagregado coincide con la distribución global.
*   **Boxplot**: Diagrama de caja alineado en el eje horizontal que señala la media y los valores atípicos (*outliers*).
*   **Tabla de Estadísticas Descriptivas**: Cuadro lateral que calcula métricas esenciales:
    *   Media (representada con una línea discontinua roja).
    *   Mediana (representada con una línea continua verde).
    *   Desviación Estándar y Coeficiente de Variación (CV%).
    *   Mínimo, Máximo, Q1, Q3, Asimetría, Curtosis y conteo de atípicos.
    *   **Prueba de Normalidad**: Aplica el test de *Shapiro-Wilk* (para $N \le 5000$) o *D'Agostino-Pearson* (para $N > 5000$). Si se rechaza la normalidad ($p < 0.05$), el fondo de la celda de la tabla se colorea en amarillo para advertencia.
*   **Selector Dinámico**: Menú desplegable interno en la gráfica para cambiar la variable analizada de forma inmediata sin necesidad de re-renderizar la celda de Quarto.

**Ejemplo de uso:**
```python
# Gráfica interactiva univariada segmentada por 'Categoria'
fig = boxhist_interactivo(
    data=df_pandas,
    titulo="Análisis de Distribución Financiera",
    color_var="Categoria",
    width=1050,
    height=650
)
fig.show()
```

---

## 📥 Instalación de Dependencias

El repositorio cuenta con una forma automatizada de gestionar las librerías de Python necesarias para evitar inconsistencias en el entorno.

### En Windows (Un Clic)
1. Abre el directorio `Documentación_plantilla/`.
2. Ejecuta el archivo **`Instalar_Dependencias.bat`**.

> **Funcionamiento interno:**
> Este instalador ejecuta en primer lugar [`generar_requerimientos.py`](file:///c:/Users/elitebook%20hp/Documents/GitHub/Plantilla_informes/Documentación_plantilla/scripts/generar_requerimientos.py). Este script escanea estáticamente los archivos `.qmd` y `.py` de la raíz del proyecto para extraer los imports reales y escribir un `requirements.txt` actualizado. Luego, invoca a `pip` para instalar los requerimientos detectados junto con las dependencias base de Jupyter y Quarto (`jupyter`, `ipykernel`, `PyYAML`).

### Manual (Consola)
Si prefieres utilizar la consola de comandos o gestionar un entorno virtual específico, abre tu terminal en el directorio raíz del proyecto y ejecuta:

```bash
# 1. Generar la lista de requerimientos actualizada en base a los scripts y archivos .qmd
python Documentación_plantilla/scripts/generar_requerimientos.py

# 2. Instalar los paquetes con pip
pip install -r Documentación_plantilla/scripts/requirements.txt
```

---

## 🚀 Guía de Inicio Rápido

### 1. Configuración de Metadatos
Abre el archivo [`Informe.qmd`](file:///c:/Users/elitebook%20hp/Documents/GitHub/Plantilla_informes/Informe.qmd) y actualiza los metadatos YAML en la cabecera (título, autor, idioma):

```yaml
title: "Título de tu Informe"
author: "Tu Nombre"
lang: es
```

### 2. Integrar las Utilidades
La plantilla ya viene preconfigurada para incluir y ejecutar el archivo con las utilidades de analítica:
```markdown
{{< include Inicialización.qmd >}}
```
Puedes comenzar a escribir bloques de código de Python (`{python}`) utilizando las funciones de carga (`query_to_df`), análisis visual (`boxhist_interactivo`) o visualización tabular (`pretty_table`).

### 3. Renderizar el Documento
Para generar el reporte interactivo final en HTML, abre la consola en la raíz de la carpeta y ejecuta:

```bash
quarto render Informe.qmd
```

El informe auto-contenido `Informe.html` se creará en el mismo directorio, listo para ser visualizado en cualquier navegador.

---

## ✍️ Créditos y Agradecimientos

### Autoría del Proyecto
Esta plantilla y su suite de utilidades de analítica en Python y Quarto han sido desarrolladas por:

*   **Matías Valenzuela Nuche**
    *   GitHub: [@MValenzuelaN](https://github.com/MValenzuelaN)

### Extensiones de Terceros
El proyecto incorpora y reconoce el trabajo de la comunidad de Quarto, en particular:

*   **code-fullscreen**: Extensión desarrollada por [@shafayetShafee](https://github.com/shafayetShafee) que añade el botón de pantalla completa a los bloques de código. Repositorio original: [shafayetShafee/code-fullscreen](https://github.com/shafayetShafee/code-fullscreen).

---
Cualquier propuesta, reporte de fallos o contribución para expandir las utilidades es bienvenida mediante *pull requests* o *issues* en el repositorio.

---
*Desarrollado para facilitar el análisis de datos con Python y Quarto.*
