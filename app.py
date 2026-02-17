import streamlit as st
import pandas as pd
from io import BytesIO
from model_delanteros import preparar_datos_delanteros
from PIL import Image

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------
st.set_page_config(
    page_title="RCL Scout Group | Intelligence",
    page_icon="⚽",
    layout="wide"
)

# --------------------------------------------------
# ESTILO REFINADO (ALTA VISIBILIDAD)
# --------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    /* Ajuste de contraste para el Sidebar */
    [data-testid="stSidebar"] { background-color: #F1F5F9; border-right: 1px solid #E2E8F0; }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h1 { color: #1E293B !important; }
    h1, h2, h3 { color: #0284C7; font-weight: 800; }
    /* Estilo para los sliders */
    .stSlider { color: #0284C7; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER CON LOGO RCL
# --------------------------------------------------
try:
    logo_path = r"C:\Buscador pro delanteros\BUSCADORDELANTEROS\rcl_scout_group_logo.png"
    logo = Image.open(logo_path)
    st.image(logo, width=200)
except Exception:
    st.title("RCL Scout Group")

st.subheader("Buscador Profesional de Perfiles Ofensivos | Latinoamerica 2025")
st.divider()

# --------------------------------------------------
# CARGA Y PREPARACIÓN DE DATOS
# --------------------------------------------------
@st.cache_data
def cargar_datos():
    return pd.read_excel("delanteros_base.xlsx")

try:
    df_raw = cargar_datos()
    df = preparar_datos_delanteros(df_raw)
except Exception as e:
    st.error(f"Error cargando base de datos: {e}")
    st.stop()

# --------------------------------------------------
# SIDEBAR – FILTROS DE MERCADO
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Parámetros de Scouting")
    
    min_90s = st.slider("Minutos jugados (90s)", 1.0, 30.0, 8.0, 0.5)
    max_age = st.slider("Edad máxima", 15, 40, 23)
    
    st.divider()
    st.header("🎯 Perfil Ofensivo")
    
    # Filtros de rendimiento puro (sin pesos)
    min_goles = st.slider("Goles por 90 min", 0.0, 1.5, 0.3, 0.05)
    min_asist = st.slider("Asistencias por 90 min", 0.0, 1.0, 0.1, 0.05)
    
    n_jugadores = st.slider("Mostrar Top", 5, 100, 15)

# --------------------------------------------------
# LÓGICA DE FILTRADO
# --------------------------------------------------
df_filtrado = df[
    (df["90s"] >= min_90s) &
    (df["Age"] <= max_age) &
    (df["Gls_p90"] >= min_goles) &
    (df["Ast_p90"] >= min_asist)
].copy()

# --------------------------------------------------
# DESPLIEGUE DE RESULTADOS
# --------------------------------------------------
if not df_filtrado.empty:
    # KPIs rápidos
    c1, c2, c3 = st.columns(3)
    c1.metric("Jugadores encontrados", len(df_filtrado))
    c2.metric("Promedio G/90", f"{df_filtrado['Gls_p90'].mean():.2f}")
    c3.metric("Edad Promedio", f"{df_filtrado['Age'].mean():.1f}")

    # Ordenar por Goles por 90 por defecto
    df_resultado = df_filtrado.sort_values("Gls_p90", ascending=False).head(n_jugadores)

    # Formateo de decimales para la tabla (adiós a los ceros de más)
    columnas_mostrar = ["Player", "Squad", "Age", "90s", "Gls_p90", "Ast_p90"]
    df_formateado = df_resultado[columnas_mostrar].copy()
    
    # Aplicar formato de 2 decimales
    df_formateado["Age"] = df_formateado["Age"].astype(int)
    df_formateado["90s"] = df_formateado["90s"].map("{:.1f}".format)
    df_formateado["Gls_p90"] = df_formateado["Gls_p90"].map("{:.2f}".format)
    df_formateado["Ast_p90"] = df_formateado["Ast_p90"].map("{:.2f}".format)

    st.markdown("### 🔥 Resultados del Scouting")
    st.dataframe(df_formateado, use_container_width=True, hide_index=True)

    # Exportación
    def to_excel(df_to_save):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_to_save.to_excel(writer, index=False, sheet_name='Scouting_RCL')
        return output.getvalue()

    st.download_button(
        label="📥 Exportar Selección a Excel",
        data=to_excel(df_resultado[columnas_mostrar]),
        file_name='Reporte_Scouting_RCL.xlsx',
        mime='application/vnd.ms-excel'
    )
else:
    st.warning("No hay jugadores que coincidan con estos filtros.")

st.markdown("<br><p style='text-align:center;color:#94A3B8;'>RCL Scout Group | Intelligence & Data Analysis</p>", unsafe_allow_html=True)