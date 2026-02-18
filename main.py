import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gerencia de Alimentos Procesados", layout="wide")

# --- INYECCIÓN DE ESTILO RADICAL (BLINDAJE TOTAL) ---
st.markdown("""
    <style>
    /* 1. Fondo Blanco Total */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 2. ENCABEZADO TIPO PLAZA'S */
    .header-container {
        display: flex;
        align-items: center;
        padding: 10px 0px;
        margin-bottom: 25px;
        border-bottom: 3px solid #36b04b;
    }
    .logo-img { height: 90px; margin-right: 25px; }
    .main-title { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1a3a63 !important; 
        font-size: 34px; 
        font-weight: 800;
        margin: 0;
    }
    .sub-title { 
        color: #444444 !important; 
        font-size: 20px; 
        margin: 0;
    }

    /* 3. BLINDAJE DE CUADROS (Fecha, Cantidades, Observaciones y Selectores) */
    /* Forzamos fondo blanco y texto negro con -webkit-text-fill-color */
    div[data-baseweb="input"], input, textarea, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border: 1px solid #CCCCCC !important;
    }

    /* Forzar visibilidad del texto dentro de los cuadros de cantidad y fecha */
    [data-testid="stNumberInput"] input, [data-testid="stDateInput"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 4. BOTONES VERDES INVARIABLES */
    .stButton > button {
        background-color: #36b04b !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton > button p, .stButton > button span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* 5. OTROS ELEMENTOS */
    .section-header { background-color: #f0f2f6 !important; color: #333 !important; padding: 8px; font-weight: bold; text-align: center; border-radius: 4px; }
    .codigo-box { background-color: #f0f0f0 !important; color: black !important; padding: 8px; border: 1px solid #ccc; text-align: center; font-weight: bold; border-radius: 4px; }
    label, p, span { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE LOGO ---
def render_header(logo_path):
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class="header-container">
                <img src="data:image/png;base64,{data}" class="logo-img">
                <div>
                    <div class="main-title">Registro de Producción</div>
                    <div class="sub-title">Gerencia de Alimentos Procesados</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("⚠️ Sube 'logo_plaza.png' a GitHub.")

render_header("logo_plaza.png")

# --- LÓGICA DE DATOS ---
PRODUCTOS_DATA = [
    {"Codigo": "27101", "Descripcion": "TORTA DE QUESO CRIOLLO PLAZAS", "Seccion": "DECORACIÓN"},
    {"Codigo": "27113", "Descripcion": "TORTA DE NARANJA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27374", "Descripcion": "RELLENO PARA LEMON PIE KG", "Seccion": "RELLENOS Y CREMAS"}
    # ... añade el resto de tus productos aquí
]
df_productos = pd.DataFrame(PRODUCTOS_DATA)

if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in df_productos['Seccion'].unique()}

col_sup, col_fec = st.columns(2)
with col_sup:
    supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec:
    # Este cuadro de fecha ahora tiene forzado el texto negro
    fecha_sel = st.date_input("Fecha", datetime.now())

for seccion in df_productos['Seccion'].unique():
    st.markdown(f'<div class="section-header">{seccion}</div>', unsafe_allow_html=True)
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    
    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        c1, c2, c3, c4 = st.columns([1, 3.2, 1, 0.3])
        with c2:
            seleccion = st.selectbox(f"S_{seccion}_{i}", options=opciones, key=f"sel_{seccion}_{i}", label_visibility="collapsed")
            item['Descripcion'] = seleccion
            item['Codigo'] = df_productos[df_productos['Descripcion'] == seleccion]['Codigo'].values[0]
        with c1:
            st.markdown(f'<div class="codigo-box">{item["Codigo"]}</div>', unsafe_allow_html=True)
        with c3:
            # Este cuadro de cantidad ahora tiene forzado el texto negro
            item['Cantidad'] = st.number_input(f"Q_{seccion}_{i}", min_value=0, value=item['Cantidad'], key=f"q_{seccion}_{i}", label_visibility="collapsed")
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir a {seccion.lower()}", key=f"btn_{seccion}"):
        st.session_state.secciones_data[seccion].append({"Codigo": "", "Descripcion": opciones[0], "Cantidad": 0})
        st.rerun()

st.write("---")
# Observaciones con label manual y cuadro forzado a blanco/negro
st.markdown('<p style="color:black !important;">Observaciones:</p>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Escriba aquí sus notas...", label_visibility="collapsed")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    # Aquí va tu lógica de guardado en GSheets
    st.success("¡Registro completado!"); st.balloons()
