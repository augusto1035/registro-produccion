import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN DE ARCHIVO ---
EXCEL_FILE = "Base de datos.xlsx"

# 1. FORZAR MODO CLARO Y ESTÉTICA POWER APPS (Sin celdas negras)
st.set_page_config(page_title="Registro de producción", layout="wide")

st.markdown("""
    <style>
    /* Fondo blanco total */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: white !important;
        color: #31333F !important;
    }
    
    /* Encabezado Verde */
    .header {
        background-color: #36b04b;
        color: white;
        padding: 15px;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 24px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    /* Títulos de Sección */
    .section-header {
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* BOTONES BLANCOS CON BORDE (Estilo Power Apps) */
    .stButton > button {
        background-color: white !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        border-color: #36b04b !important;
        color: #36b04b !important;
    }

    /* Entradas blancas con borde gris */
    input, div[data-baseweb="select"], div[data-baseweb="input"], .stNumberInput div {
        background-color: white !important;
        border: 1px solid #cccccc !important;
        color: black !important;
    }

    /* Quitar sombras negras de fondo */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    </style>
    <div class="header">Registro de producción</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE SESIÓN ---
if 'prod_rows' not in st.session_state: st.session_state.prod_rows = []
if 'dec_rows' not in st.session_state: st.session_state.dec_rows = []

# 1. ENCABEZADO
col1, col2 = st.columns(2)
with col1:
    supervisor = st.selectbox("Seleccione Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col2:
    fecha_sel = st.date_input("Fecha de Registro", datetime.now())

# --- SECCIÓN PRODUCCIÓN ---
st.markdown('<div class="section-header">PRODUCCIÓN</div>', unsafe_allow_html=True)
for i, item in enumerate(st.session_state.prod_rows):
    c1, c2, c3, c4 = st.columns([1, 2.5, 1, 0.4])
    with c1: item['Codigo_Articulo'] = st.text_input("Cód", value=item['Codigo_Articulo'], key=f"p_c_{i}", label_visibility="collapsed", placeholder="Código")
    with c2: item['Descripcion'] = st.selectbox("Desc", ["Base Vainilla pequeña", "Chocolate", "Red Velvet"], key=f"p_d_{i}", label_visibility="collapsed")
    with c3: item['Cantidad'] = st.number_input("Cant", value=item['Cantidad'], min_value=0, key=f"p_q_{i}", label_visibility="collapsed")
    with c4: 
        if st.button("X", key=f"p_x_{i}"):
            st.session_state.prod_rows.pop(i)
            st.rerun()

if st.button("➕ AÑADIR ITEM PRODUCCIÓN", key="add_p"):
    st.session_state.prod_rows.append({"Codigo_Articulo": "", "Descripcion": "Base Vainilla pequeña", "Cantidad": 0})
    st.rerun()

# --- SECCIÓN DECORACIÓN ---
st.markdown('<div class="section-header">DECORACIÓN</div>', unsafe_allow_html=True)
for i, item in enumerate(st.session_state.dec_rows):
    c1, c2, c3, c4 = st.columns([1, 2.5, 1, 0.4])
    with c1: item['Codigo_Articulo'] = st.text_input("Cód", value=item['Codigo_Articulo'], key=f"d_c_{i}", label_visibility="collapsed", placeholder="Código")
    with c2: item['Descripcion'] = st.selectbox("Desc", ["Arequipe", "Coco Arequipe", "Lluvia de Chocolate"], key=f"d_d_{i}", label_visibility="collapsed")
    with c3: item['Cantidad'] = st.number_input("Cant", value=item['Cantidad'], min_value=0, key=f"d_q_{i}", label_visibility="collapsed")
    with c4: 
        if st.button("X", key=f"d_x_{i}"):
            st.session_state.dec_rows.pop(i)
            st.rerun()

if st.button("➕ AÑADIR ITEM DECORACIÓN", key="add_d"):
    st.session_state.dec_rows.append({"Codigo_Articulo": "", "Descripcion": "Arequipe", "Cantidad": 0})
    st.rerun()

st.write("---")
observaciones = st.text_area("Observaciones")

# --- BOTÓN FINALIZAR (CONEXIÓN EXACTA A COLUMNAS EXCEL) ---
if st.button("FINALIZAR Y GUARDAR TODO", use_container_width=True):
    registros = []
    # Unificar todas las filas con los nombres de columna correctos
    for x in st.session_state.prod_rows + st.session_state.dec_rows:
        registros.append({
            "ID_Registro": datetime.now().strftime("%Y%m%d%H%M%S"),
            "Supervisor": supervisor,
            "Fecha_Hora": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "Codigo_Articulo": x['Codigo_Articulo'],
            "Descripcion": x['Descripcion'],
            "Cantidad": x['Cantidad'],
            "Observaciones": observaciones
        })
    
    if registros:
        df_nuevo = pd.DataFrame(registros)
        try:
            if os.path.exists(EXCEL_FILE):
                df_base = pd.read_excel(EXCEL_FILE)
                # Forzar que solo use las columnas que ya existen en tu base de datos
                pd.concat([df_base, df_nuevo], ignore_index=True)[df_base.columns].to_excel(EXCEL_FILE, index=False)
            else:
                df_nuevo.to_excel(EXCEL_FILE, index=False)
            
            st.success("✅ ¡Reporte guardado con éxito en las columnas correctas!")
            st.session_state.prod_rows, st.session_state.dec_rows = [], []
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error: Cierra el archivo Excel. {e}")
    else:
        st.warning("No hay ítems para registrar.")