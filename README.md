# ⚽ RCL Scout Group: Buscador Profesional de Delanteros 2025

Este proyecto es una herramienta de inteligencia deportiva diseñada para optimizar procesos de scouting en ligas latinoamericanas. Permite identificar perfiles ofensivos específicos mediante el análisis de métricas normalizadas de producción y volumen.

## 🚀 Características Técnicas
- **Data Source:** Los datos han sido extraídos íntegramente de **FBRef** mediante técnicas avanzadas de **Web Scraping**.
- **Ingeniería de Datos:** Utilicé **Beautiful Soup** para la captura de datos y **Pandas** para la limpieza, normalización y transformación de los datasets.
- **Normalización:** La herramienta prioriza métricas por cada 90 minutos jugados ($Gls/90$, $Ast/90$), eliminando el sesgo que produce el total de goles en jugadores con disparidad de minutos.
- **Visualización:** Desplegado con **Streamlit**, ofreciendo una interfaz reactiva y profesional para la toma de decisiones.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **Librerías de Datos:** Pandas, Openpyxl, XlsxWriter.
- **Librerías de Scraping:** Beautiful Soup 4, Requests.
- **Framework Web:** Streamlit.

## 📂 Estructura del Proyecto
- `app.py`: Archivo principal con la lógica de la interfaz y filtros.
- `model_delanteros.py`: Backend lógico para la limpieza y preparación del dataframe.
- `delanteros_base.xlsx`: Dataset maestro extraído de FBRef.
- `requirements.txt`: Dependencias necesarias para el despliegue en Streamlit Cloud.

## 👤 Autor
**Diego Gutiérrez Data Analyst en RCL Group**
*Desarrollador de soluciones basadas en datos para el ecosistema del fútbol profesional.*
