import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gerencia de Alimentos Procesados", layout="wide")

# --- INYECCIÓN DE ESTILO "SMART MOBILE" (SIN DESBORDE) ---
st.markdown("""
    <style>
    /* 1. FORZAR FILA ÚNICA SIN DESBORDE */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* No salta de línea */
        align-items: center !important;
        gap: 4px !important; /* Espacio mínimo entre columnas */
        width: 100% !important;
    }

    [data-testid="column"] {
        min-width: 0 !important; /* Permite que la columna se encoja */
        flex-shrink: 1 !important;
    }

    /* 2. AJUSTES DE TEXTO Y TAMAÑO PARA MÓVIL */
    input, div[data-baseweb="select"] > div, .codigo-box-forzado {
        font-size: 12px !important; /* Texto más pequeño para ganar espacio */
        height: 35px !important;
        padding: 2px !important;
    }

    /* 3. BLINDAJE DE COLORES (Siempre Blanco/Negro) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    div[data-baseweb="select"] *, div[data-baseweb="popover"] *, input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* 4. ENCABEZADO PLAZA'S */
    .header-container {
        display: flex;
        align-items: center;
        padding: 10px 0px;
        margin-bottom: 15px;
        border-bottom: 3px solid #36b04b;
    }
    .logo-img { height: 60px; margin-right: 10px; }
    .main-title { color: #1a3a63 !important; font-size: 22px; font-weight: 800; margin: 0; }
    .sub-title { color: #444444 !important; font-size: 12px; margin: 0; }

    /* 5. CAJA DE CÓDIGOS ULTRA-COMPACTA */
    .codigo-box-forzado {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        border: 1px solid #cccccc;
        text-align: center;
        font-weight: bold;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 6. BOTONES VERDES */
    .stButton > button {
        background-color: #36b04b !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        padding: 0px !important;
    }
    .stButton > button * { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }

    .section-header { background-color: #f0f2f6 !important; color: #000 !important; padding: 3px; text-align: center; font-size: 13px; border-radius: 4px; margin-top: 8px;}
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
    except:
        st.write("### Plaza's - Producción")

render_header("logo_plaza.png")

# --- BASE DE DATOS (Misma lista anterior) ---
PRODUCTOS_DATA = [
    {"Codigo": "27101", "Descripcion": "TORTA DE QUESO CRIOLLO PLAZAS", "Seccion": "DECORACIÓN"},
    {"Codigo": "27113", "Descripcion": "TORTA DE NARANJA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    # ... (incluir aquí los 79 productos)
    {"Codigo": "2", "Descripcion": "BASE DE RED VELVET", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"}
]
df_productos = pd.DataFrame(PRODUCTOS_DATA)
SECCIONES_ORDEN = ["BASES, BISCOCHOS Y TARTALETAS", "DECORACIÓN", "PANES", "POSTRE", "RELLENOS Y CREMAS"]

if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}

# Fila Superior Compacta
col_sup, col_fec = st.columns([1, 1])
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec: fecha_sel = st.date_input("Fecha", datetime.now())

# --- RENDERIZADO ---
for seccion in SECCIONES_ORDEN:
    st.markdown(f'<div class="section-header">{seccion}</div>', unsafe_allow_html=True)
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    
    if not opciones: continue

    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        # DISTRIBUCIÓN DE "AJUSTE PERFECTO"
        # 0.6 para Código (solo números), 2.8 para Descripción, 0.8 para Cantidad, 0.3 para X
        c1, c2, c3, c4 = st.columns([0.6, 2.8, 0.8, 0.3])
        with c1:
            st.markdown(f'<div class="codigo-box-forzado">{item["Codigo"]}</div>', unsafe_allow_html=True)
        with c2:
            seleccion = st.selectbox(f"S_{seccion}_{i}", options=opciones, key=f"sel_{seccion}_{i}", label_visibility="collapsed")
            item['Descripcion'] = seleccion
            item['Codigo'] = df_productos[df_productos['Descripcion'] == seleccion]['Codigo'].values[0]
        with c3:
            item['Cantidad'] = st.number_input(f"Q_{seccion}_{i}", min_value=0, step=1, key=f"q_{seccion}_{i}", label_visibility="collapsed")
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir a {seccion.lower()}", key=f"btn_{seccion}"):
        st.session_state.secciones_data[seccion].append({"Codigo": opciones[0], "Descripcion": opciones[0], "Cantidad": 0})
        st.rerun()

st.write("---")
st.markdown('<p style="color:black !important; font-weight:bold; font-size:12px;">Observaciones:</p>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Notas...", label_visibility="collapsed")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    st.success("¡Registro completado!"); st.balloons()
