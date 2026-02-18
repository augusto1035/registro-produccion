import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Producción Plaza's", layout="wide")

# --- CSS DE CIRUGÍA (SOLUCIÓN DEFINITIVA DE ANCHOS) ---
st.markdown("""
    <style>
    /* 1. MODO CLARO OBLIGATORIO */
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #ffffff !important; color: black !important; }

    /* 2. ESPACIO MÁXIMO (Casi al borde) */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.1rem !important;
        padding-right: 0.1rem !important;
    }

    /* 3. LÓGICA DE FILA: Solo aplicamos anchos fijos a filas de 4 columnas (PRODUCTOS) */
    /* El selector :has comprueba si la fila tiene una 4ta columna. Si sí, aplica reglas. */
    [data-testid="stHorizontalBlock"]:has([data-testid="column"]:nth-child(4)) {
        flex-wrap: nowrap !important;
        gap: 1px !important;
        align-items: center !important;
        width: 100% !important;
    }

    /* COLUMNA 1 (CÓDIGO): Fijo 45px */
    [data-testid="stHorizontalBlock"]:has([data-testid="column"]:nth-child(4)) [data-testid="column"]:nth-child(1) {
        flex: 0 0 45px !important;
        min-width: 45px !important;
        max-width: 45px !important;
        overflow: hidden !important;
        padding: 0 !important;
    }

    /* COLUMNA 2 (DESCRIPCIÓN): El resto del espacio */
    [data-testid="stHorizontalBlock"]:has([data-testid="column"]:nth-child(4)) [data-testid="column"]:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 50px !important;
        overflow: hidden !important;
        padding: 0 !important;
    }

    /* COLUMNA 3 (CANTIDAD): Fijo 50px */
    [data-testid="stHorizontalBlock"]:has([data-testid="column"]:nth-child(4)) [data-testid="column"]:nth-child(3) {
        flex: 0 0 50px !important;
        min-width: 50px !important;
        max-width: 50px !important;
        overflow: hidden !important;
        padding: 0 !important;
    }

    /* COLUMNA 4 (X): Fijo 35px */
    [data-testid="stHorizontalBlock"]:has([data-testid="column"]:nth-child(4)) [data-testid="column"]:nth-child(4) {
        flex: 0 0 35px !important;
        min-width: 35px !important;
        max-width: 35px !important;
        padding: 0 !important;
    }

    /* 4. AJUSTE DE LOS INPUTS (LAS CAJAS) PARA QUE QUEPAN EN LOS TAMAÑOS FIJOS */
    div[data-baseweb="select"] > div, 
    [data-testid="stNumberInput"] input {
        min-height: 35px !important;
        height: 35px !important;
        padding: 0px 1px !important; /* Cero aire */
        font-size: 11px !important;
        background-color: white !important;
        border: 1px solid #aaa !important;
        color: black !important;
        text-align: center !important;
    }
    
    /* El selector de descripción alineado a la izquierda */
    div[data-baseweb="select"] > div { text-align: left !important; }

    /* 5. CAJA DE CÓDIGO (GRIS) */
    .codigo-box {
        background-color: #e0e0e0;
        border: 1px solid #aaa;
        color: black;
        font-weight: bold;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        border-radius: 4px;
        width: 100%;
        line-height: 1;
    }

    /* 6. BOTONES (TODOS VERDES) */
    .stButton > button {
        background-color: #36b04b !important;
        color: white !important;
        border: none !important;
        height: 35px !important;
        min-height: 35px !important;
        width: 100% !important;
        padding: 0 !important;
    }
    .stButton > button:hover { background-color: #2a8a3b !important; }

    /* 7. ENCABEZADO (NO TOCADO POR LAS REGLAS DE ARRIBA) */
    .header-layout {
        display: flex; 
        align-items: center; 
        padding-bottom: 10px; 
        border-bottom: 3px solid #36b04b; 
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (HTML PURO PARA EVITAR CONFLICTOS) ---
def render_header(logo_path):
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class="header-layout">
                <img src="data:image/png;base64,{data}" style="height: 60px; margin-right: 15px;">
                <div>
                    <div style="color:#1a3a63; font-size:20px; font-weight:800; line-height:1.2;">Registro de Producción</div>
                    <div style="color:#444; font-size:12px;">Gerencia de Alimentos Procesados</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("### Producción Plaza's

