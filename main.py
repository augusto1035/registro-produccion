import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from streamlit_gsheets import GSheetsConnection
import pytz

# --- CONFIGURACIÓN DE ZONA HORARIA VENEZUELA ---
ve_tz = pytz.timezone('America/Caracas')
hora_actual = datetime.now(ve_tz)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Producción Plaza's", layout="wide")

# --- CSS VISUAL ---
st.markdown("""
    <style>
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8f9fa !important; color: black !important; }
    .block-container { padding-top: 3.5rem !important; max-width: 100% !important; }
    .section-header {
        background: #36b04b; color: white; padding: 8px; text-align: center;
        font-weight: bold; border-radius: 4px; margin-top: 20px; margin-bottom: 10px;
    }
    .resumen-box {
        background-color: #ffffff; padding: 20px; border: 2px solid #36b04b;
        border-radius: 10px; color: #1a3a63; margin-top: 20px;
    }
    .stButton > button {
        background-color: #36b04b !important; color: white !important;
        font-weight: bold; width: 100%; min-height: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DEFINICIÓN DE SECCIONES ---
SECCIONES_ORDEN = ["BASES, BISCOCHOS Y TARTALETAS", "DECORACIÓN", "PANES", "POSTRE", "RELLENOS Y CREMAS"]

# --- INICIALIZACIÓN DE ESTADOS ---
if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}
if 'exito' not in st.session_state:
    st.session_state.exito = False
if 'ultimo_resumen' not in st.session_state:
    st.session_state.ultimo_resumen = None

# --- HEADER ---
def render_header(logo_path):
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding-bottom: 10px; border-bottom: 4px solid #36b04b; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" style="height: 70px; margin-right: 15px;">
                <div>
                    <h2 style="color:#1a3a63; margin:0; font-weight:900; font-size: 20px;">Registro de Producción</h2>
                    <p style="color:#666; margin:0; font-size: 12px;">Gerencia de Alimentos Procesados</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.title("Registro de Producción Plaza's")

render_header("logo_plaza.png")

# --- MOSTRAR RESUMEN SI HUBO ÉXITO ---
if st.session_state.exito and st.session_state.ultimo_resumen is not None:
    st.balloons()
    st.markdown('<div class="resumen-box">', unsafe_allow_html=True)
    st.subheader("📋 Resumen de Registro Exitoso")
    st.write(f"**Supervisor:** {st.session_state.ultimo_resumen['supervisor']}")
    st.write(f"**Fecha/Hora:** {st.session_state.ultimo_resumen['fecha_hora']}")
    
    # Tabla simple para el capture
    df_res = pd.DataFrame(st.session_state.ultimo_resumen['productos'])
    st.table(df_res[['Cantidad', 'Descripcion']])
    
    if st.session_state.ultimo_resumen['obs']:
        st.info(f"**Observaciones:** {st.session_state.ultimo_resumen['obs']}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("👆 *Puedes tomar un capture a este cuadro para tu reporte.*")
    
    if st.button("🔄 Crear nuevo registro"):
        st.session_state.exito = False
        st.session_state.ultimo_resumen = None
        st.rerun()
    st.stop() # Detiene el renderizado del formulario para mostrar solo el resumen

# --- FORMULARIO PRINCIPAL ---
col_sup, col_fec = st.columns(2)
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado", "Jesus Ramirez"])
with col_fec: fecha_sel = st.date_input("Fecha", hora_actual.date())

# (Carga de productos omitida por brevedad, usa tu lista de PRODUCTOS_DATA aquí)
# ... [AQUÍ VA TU PRODUCTOS_DATA Y EL BUCLE DE RENDERIZADO QUE YA TIENES] ...

# --- BOTÓN GUARDAR ---
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    registros = []
    resumen_productos = []
    ahora_ve = datetime.now(ve_tz)
    fecha_hora_unificada = ahora_ve.strftime("%d/%m/%Y %I:%M %p")
    
    for seccion, items in st.session_state.secciones_data.items():
        for item in items:
            if item['Cantidad'] > 0:
                # Datos para Google Sheets
                registros.append({
                    "ID_Registro": ahora_ve.strftime("%Y%m%d%H%M%S"), 
                    "Supervisor": supervisor,
                    "Fecha_Hora": fecha_hora_unificada,
                    "Codigo_Articulo": item['Codigo'], 
                    "Descripcion": item['Descripcion'],
                    "Cantidad": item['Cantidad'], 
                    "Observaciones": st.session_state.obs_input
                })
                # Datos para el resumen visual
                resumen_productos.append({"Cantidad": item['Cantidad'], "Descripcion": item['Descripcion']})
    
    if not registros:
        st.warning("No hay productos con cantidad > 0.")
    else:
        try:
            # Guardar en Sheets
            df_nuevo = pd.DataFrame(registros)
            df_existente = conn.read(worksheet="Hoja1", ttl=0) 
            df_total = pd.concat([df_existente, df_nuevo], ignore_index=True)
            conn.update(worksheet="Hoja1", data=df_total)
            
            # Guardar datos en el estado para el resumen visual
            st.session_state.ultimo_resumen = {
                "supervisor": supervisor,
                "fecha_hora": fecha_hora_unificada,
                "productos": resumen_productos,
                "obs": st.session_state.obs_input
            }
            
            st.session_state.exito = True
            st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

