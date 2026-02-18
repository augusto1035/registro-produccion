import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import base64

# 1. BASE DE DATOS (Mantenemos tu lista de productos)
PRODUCTOS_DATA = [
    {"Codigo": "27101", "Descripcion": "TORTA DE QUESO CRIOLLO PLAZAS", "Seccion": "DECORACIÓN"},
    {"Codigo": "27113", "Descripcion": "TORTA DE NARANJA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27115", "Descripcion": "TORTA DE AREQUIPE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27119", "Descripcion": "TORTA DE ZANAHORIA CON NUECES GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27121", "Descripcion": "TORTA DE ZANAHORIA CON QUESO CREMA GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27127", "Descripcion": "TORTA DE CHOCOLATE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27133", "Descripcion": "TORTA DE PIÑA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27137", "Descripcion": "TORTA DE VAINILLA CON CHOCOLATE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27470", "Descripcion": "PAN DE COCO PLAZAS PAQUETE 4UND", "Seccion": "PANES"},
    {"Codigo": "27471", "Descripcion": "PAN DE AREQUIPE PLAZAS PAQUETE 4UND", "Seccion": "PANES"},
    {"Codigo": "27667", "Descripcion": "PIE DE LIMON PLAZAS", "Seccion": "POSTRE"},
    {"Codigo": "27374", "Descripcion": "RELLENO PARA LEMON PIE KG", "Seccion": "RELLENOS Y CREMAS"}
]

df_productos = pd.DataFrame(PRODUCTOS_DATA)

# --- CONFIGURACIÓN E INYECCIÓN DE ESTILO ---
st.set_page_config(page_title="Gerencia de Alimentos Procesados", layout="wide")

st.markdown("""
    <style>
    /* 1. Blindaje Global contra Modo Oscuro */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 2. Estilo del Encabezado (Logo + Texto) */
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

    /* 3. Botones Verdes Invariables */
    .stButton > button {
        background-color: #36b04b !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }
    .stButton > button p, .stButton > button span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* 4. Visibilidad de Selectores y Listas */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"] *, div[role="listbox"] * {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* 5. Otros Elementos */
    .section-header { 
        background-color: #f0f2f6 !important; 
        color: #333 !important; 
        padding: 8px; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 20px;
        border-radius: 4px;
    }
    .codigo-box { 
        background-color: #f0f0f0 !important; 
        color: black !important; 
        padding: 8px; 
        border: 1px solid #ccc; 
        text-align: center; 
        font-weight: bold; 
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA CARGAR LOGO ---
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
        st.error("⚠️ No se encontró el archivo 'logo_plaza.png'. Asegúrate de subirlo a GitHub.")

render_header("logo_plaza.png")

# --- LÓGICA DE LA APLICACIÓN ---
if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in df_productos['Seccion'].unique()}

col_sup, col_fec = st.columns(2)
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec: fecha_sel = st.date_input("Fecha", datetime.now())

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
            item['Cantidad'] = st.number_input(f"Q_{seccion}_{i}", min_value=0, value=item['Cantidad'], key=f"q_{seccion}_{i}", label_visibility="collapsed")
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir a {seccion.lower()}", key=f"btn_{seccion}"):
        st.session_state.secciones_data[seccion].append({"Codigo": "", "Descripcion": opciones[0], "Cantidad": 0})
        st.rerun()

st.write("---")
st.markdown('<p style="font-weight:bold; color:black;">Observaciones:</p>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Escriba aquí sus notas...", label_visibility="collapsed")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    # (Aquí va tu conexión a GSheets como ya la tienes)
    st.success("¡Datos registrados correctamente!"); st.balloons()
