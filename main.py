import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Producción Plaza's", layout="wide")

# --- CSS DE "CIRUGÍA PLÁSTICA" PARA LAS CAJAS ---
st.markdown("""
    <style>
    /* 1. MODO CLARO OBLIGATORIO */
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #ffffff !important; color: black !important; }

    /* 2. ELIMINAR LOS MÁRGENES LATERALES PARA GANAR CADA PIXEL */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.1rem !important; /* Casi cero */
        padding-right: 0.1rem !important;
    }

    /* 3. FORZAR LA FILA A NO ROMPERSE (NO WRAP) */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 1px !important;
    }

    /* 4. DEFINICIÓN DE LOS ANCHOS DE LAS CAJAS (AQUÍ ESTÁ LA SOLUCIÓN) */
    
    /* CAJA 1: CÓDIGO (45px Fijos - Solo el ancho del número) */
    div[data-testid="column"]:nth-of-type(1) {
        flex: 0 0 45px !important;
        min-width: 45px !important;
        max-width: 45px !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* CAJA 2: DESCRIPCIÓN (Flexible - Ocupa el resto) */
    div[data-testid="column"]:nth-of-type(2) {
        flex: 1 1 auto !important;
        min-width: 100px !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* CAJA 3: CANTIDAD (50px Fijos - Solo el ancho de 4 dígitos) */
    div[data-testid="column"]:nth-of-type(3) {
        flex: 0 0 50px !important;
        min-width: 50px !important;
        max-width: 50px !important;
        padding: 0 !important;
    }

    /* CAJA 4: BOTÓN X (35px Fijos) */
    div[data-testid="column"]:nth-of-type(4) {
        flex: 0 0 35px !important;
        min-width: 35px !important;
        max-width: 35px !important;
        padding: 0 !important;
    }

    /* 5. ESTILO DE LOS INPUTS (LAS CAJAS EN SÍ MISMAS) */
    
    /* El selector y el input de número deben ser bajitos y sin aire */
    div[data-baseweb="select"] > div, 
    [data-testid="stNumberInput"] input {
        min-height: 35px !important;
        height: 35px !important;
        padding: 0px 2px !important; /* Sin relleno interno */
        font-size: 11px !important;
        background-color: white !important;
        border: 1px solid #aaa !important; /* Borde visible */
        color: black !important;
    }

    /* 6. ESTILO DE LA CAJA DE CÓDIGO (GRIS) */
    .codigo-container {
        background-color: #e0e0e0;
        border: 1px solid #aaa;
        color: black;
        font-weight: bold;
        font-size: 10px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        width: 100%;
        white-space: nowrap; /* Que no se parta el numero */
    }

    /* 7. BOTONES VERDES (PLAZA'S) */
    .stButton > button {
        background-color: #36b04b !important;
        color: white !important;
        border: none !important;
        height: 35px !important;
        width: 100% !important;
        padding: 0 !important;
        border-radius: 4px;
    }
    
    /* 8. HEADER (RESTAURADO) */
    /* Protegemos el header para que las reglas de columnas no lo rompan */
    .header-layout {
        display: flex; 
        align-items: center; 
        padding-bottom: 5px; 
        border-bottom: 3px solid #36b04b; 
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
def render_header(logo_path):
    # Usamos HTML directo para que no le afecten las columnas de Streamlit
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class="header-layout">
                <img src="data:image/png;base64,{data}" style="height: 60px; margin-right: 10px;">
                <div>
                    <div style="color:#1a3a63; font-size:20px; font-weight:800; line-height:1.1;">Registro de Producción</div>
                    <div style="color:#444; font-size:12px;">Gerencia de Alimentos Procesados</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("### Producción Plaza's")

render_header("logo_plaza.png")

# --- DATA ---
PRODUCTOS_DATA = [
    {"Codigo": "27101", "Descripcion": "TORTA DE QUESO CRIOLLO PLAZAS", "Seccion": "DECORACIÓN"},
    {"Codigo": "27113", "Descripcion": "TORTA DE NARANJA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27115", "Descripcion": "TORTA DE AREQUIPE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27119", "Descripcion": "TORTA DE ZANAHORIA CON NUECES GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27121", "Descripcion": "TORTA DE ZANAHORIA CON QUESO CREMA GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27127", "Descripcion": "TORTA DE CHOCOLATE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27133", "Descripcion": "TORTA DE PIÑA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27137", "Descripcion": "TORTA DE VAINILLA CON CHOCOLATE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27179", "Descripcion": "TORTA DE CHOCO MANI PLAZAS PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27180", "Descripcion": "TORTA DE CHOCO MANI PLAZAS GDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27198", "Descripcion": "TORTA CHOCO MANI VAINILLA PLAZAS PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27216", "Descripcion": "PAN DULCE PLAZAS", "Seccion": "PANES"},
    {"Codigo": "27284", "Descripcion": "TORTA DE NARANJA PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27285", "Descripcion": "TORTA DE AREQUIPE PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27287", "Descripcion": "TORTA DE ZANAHORIA CON NUECES PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27289", "Descripcion": "TORTA DE PIÑA PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27290", "Descripcion": "TORTA DE VAINILLA CON CHOCOLATE PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27291", "Descripcion": "TORTA DE ZANAHORIA CON QUESO CREMA PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27294", "Descripcion": "TORTA DE CHOCOLATE PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27315", "Descripcion": "TORTA DE COCO PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27316", "Descripcion": "TORTA DE COCO GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27323", "Descripcion": "TORTA MARMOLEADA GRANDE", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27324", "Descripcion": "TORTA MARMOLEADA PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27347", "Descripcion": "TORTA PLAZAS CHOCO AREQUIPE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27348", "Descripcion": "TORTA PLAZAS CHOCO AREQUIPE PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27349", "Descripcion": "TORTA RED VELVET PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27350", "Descripcion": "TORTA PLAZAS DE COCO Y DULCE DE LECHE GRANDE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27365", "Descripcion": "TORTA PLAZAS DE COCO Y DULCE DE LECHE PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27366", "Descripcion": "TORTA PLAZAS HALLOWEEN CHOCOLATE PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27368", "Descripcion": "TORTA BLACK FRIDAY VAINILLA CHOCOLAT PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27371", "Descripcion": "TORTA DE VAINILLA CON CHOCOLATE PEQUEÑA ESPCIAL", "Seccion": "DECORACIÓN"},
    {"Codigo": "27470", "Descripcion": "PAN DE COCO PLAZAS PAQUETE 4UND", "Seccion": "PANES"},
    {"Codigo": "27471", "Descripcion": "PAN DE AREQUIPE PLAZAS PAQUETE 4UND", "Seccion": "PANES"},
    {"Codigo": "27476", "Descripcion": "TORTA PLAZAS TROPICAL PEQUEÑA", "Seccion": "DECORACIÓN"},
    {"Codigo": "27478", "Descripcion": "TORTA PINGÜINO CHOCOLATE PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27511", "Descripcion": "TORTA DE BANANA PEQ", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27657", "Descripcion": "TORTA DE CAMBUR PLAZAS CHISPAS DE CHOCOLATE", "Seccion": "DECORACIÓN"},
    {"Codigo": "27658", "Descripcion": "TORTA VAINILLA CHOCOTINA Y NUECES PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27659", "Descripcion": "TORTA VAINILLA CREMA BLANCA CHOCO LLUVIA PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27660", "Descripcion": "TORTA VAINILLA AREQUIPE CHOCO GOTAS PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27661", "Descripcion": "TORTA VAINILLA AREQUIPE CHOCO LLUVIA PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27662", "Descripcion": "TORTA VAINILLA CREMA BLANCA NUECES PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27663", "Descripcion": "TORTA VAINILLA CHOCOKRON CHOCO LLUVIA PEQ", "Seccion": "DECORACIÓN"},
    {"Codigo": "27667", "Descripcion": "PIE DE LIMON PLAZAS", "Seccion": "POSTRE"},
    {"Codigo": "27673", "Descripcion": "QUESILLO INDIVIDUAL PLAZAS", "Seccion": "POSTRE"},
    {"Codigo": "27637", "Descripcion": "MINI TORTA PLAZAS UND (UN)", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27676", "Descripcion": "PIE DE PARCHITA PLAZAS", "Seccion": "POSTRE"},
    {"Codigo": "27678", "Descripcion": "GELATINA PLAZAS FRESA Y LECHE UND", "Seccion": "POSTRE"},
    {"Codigo": "27679", "Descripcion": "GELATINA PLAZAS FRAMBUESA Y LECHE UND", "Seccion": "POSTRE"},
    {"Codigo": "27680", "Descripcion": "GELATINA PLAZAS PINA Y LECHE UND", "Seccion": "POSTRE"},
    {"Codigo": "27681", "Descripcion": "GELATINA PLAZAS LIMON UND", "Seccion": "POSTRE"},
    {"Codigo": "27682", "Descripcion": "GELATINA PLAZAS FRAMBUESA UND", "Seccion": "POSTRE"},
    {"Codigo": "27683", "Descripcion": "GELATINA PLAZAS PINA UND", "Seccion": "POSTRE"},
    {"Codigo": "27684", "Descripcion": "GELATINA PLAZAS FRESA UND", "Seccion": "POSTRE"},
    {"Codigo": "27116", "Descripcion": "TORTA VAINILLA PLAZAS AREQUIPE PORCION", "Seccion": "DECORACIÓN"},
    {"Codigo": "27128", "Descripcion": "TORTA DE CHOCOLATE PLAZAS PORCION", "Seccion": "DECORACIÓN"},
    {"Codigo": "27138", "Descripcion": "TORTA VAINILLA CUB CHOCOL PLAZAS PORCION", "Seccion": "DECORACIÓN"},
    {"Codigo": "27377", "Descripcion": "TORTA CHOCO AREQUIPE PLAZAS PORCION", "Seccion": "DECORACIÓN"},
    {"Codigo": "27697", "Descripcion": "GALLETAS CRAQUELADAS PLAZAS CHOCOLATE", "Seccion": "POSTRE"},
    {"Codigo": "27702", "Descripcion": "SUSPIROS MULTICOLOR PLAZAS UND", "Seccion": "POSTRE"},
    {"Codigo": "27677", "Descripcion": "PUDIN DE CHOCOLATE", "Seccion": "POSTRE"},
    {"Codigo": "27695", "Descripcion": "NUBE DE CHOCOLATE", "Seccion": "POSTRE"},
    {"Codigo": "27696", "Descripcion": "MARQUESA DE ALMENDRA", "Seccion": "POSTRE"},
    {"Codigo": "27688", "Descripcion": "ARROZ CON LECHE", "Seccion": "POSTRE"},
    {"Codigo": "27686", "Descripcion": "MARQUESA DE CHOCOLATE", "Seccion": "POSTRE"},
    {"Codigo": "27687", "Descripcion": "MARQUESA DE COCO", "Seccion": "POSTRE"},
    {"Codigo": "27685", "Descripcion": "TRES LECHE", "Seccion": "POSTRE"},
    {"Codigo": "27293", "Descripcion": "BIZCOCHO DE VAINILLA PEQ (BASE)", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27480", "Descripcion": "BIZCOCHO DE CHOCOLATE PEQ (BASE)", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27111", "Descripcion": "BIZCOCHO DE VAINILLA GRANDE (BASE)", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27374", "Descripcion": "RELLENO PARA LEMON PIE KG", "Seccion": "RELLENOS Y CREMAS"},
    {"Codigo": "27698", "Descripcion": "PASTA SECA PLAZAS 200G UND", "Seccion": "POSTRE"},
    {"Codigo": "27391", "Descripcion": "RELLENO PARA PIE DE PARCHITA KG", "Seccion": "RELLENOS Y CREMAS"},
    {"Codigo": "27700", "Descripcion": "RECETA BASE PLANCHA GRUES TRES LECHES UN", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27703", "Descripcion": "BASE PARA TARTALETAS (MASA DULCE) KG", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "27145", "Descripcion": "CREMA DE QUESO CREMA PARA TORTA", "Seccion": "RELLENOS Y CREMAS"},
    {"Codigo": "27701", "Descripcion": "BIZCOCHUELO DE VAINILLA UND (BASE)", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "1", "Descripcion": "BASE DE COCO COCO PEQUEÑA", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"},
    {"Codigo": "2", "Descripcion": "BASE DE RED VELVET", "Seccion": "BASES, BISCOCHOS Y TARTALETAS"}
]

df_productos = pd.DataFrame(PRODUCTOS_DATA)
SECCIONES_ORDEN = ["BASES, BISCOCHOS Y TARTALETAS", "DECORACIÓN", "PANES", "POSTRE", "RELLENOS Y CREMAS"]

if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}

# SUPERVISOR Y FECHA (FUERA DEL LOOP DE PRODUCTOS PARA QUE NO SE ROMPA)
# Usamos columnas estándar aquí porque no necesitamos el ajuste micrométrico de la tabla
col_sup, col_fec = st.columns(2)
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec: fecha_sel = st.date_input("Fecha", datetime.now())

# RENDERIZADO
for seccion in SECCIONES_ORDEN:
    st.markdown(f'<div style="background:#f0f2f6; padding:4px; text-align:center; font-weight:bold; margin-top:15px; border-radius:4px; color:black; font-size:12px;">{seccion}</div>', unsafe_allow_html=True)
    
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    if not opciones: continue

    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        # AQUÍ USAMOS ST.COLUMNS(4) PERO EL CSS "HACKEA" SUS ANCHOS
        c1, c2, c3, c4 = st.columns(4) 
        
        with c1:
            st.markdown(f'<div class="codigo-container">{item["Codigo"]}</div>', unsafe_allow_html=True)
        with c2:
            seleccion = st.selectbox(f"s_{seccion}_{i}", options=opciones, key=f"sel_{seccion}_{i}", label_visibility="collapsed")
            item['Descripcion'] = seleccion
            item['Codigo'] = df_productos[df_productos['Descripcion'] == seleccion]['Codigo'].values[0]
        with c3:
            item['Cantidad'] = st.number_input(f"q_{seccion}_{i}", min_value=0, step=1, key=f"q_{seccion}_{i}", label_visibility="collapsed")
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir a {seccion.lower()}", key=f"btn_{seccion}"):
        st.session_state.secciones_data[seccion].append({"Codigo": opciones[0], "Descripcion": opciones[0], "Cantidad": 0})
        st.rerun()

st.write("---")
st.markdown('<p style="font-weight:bold; font-size:12px;">Observaciones:</p>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Notas...", label_visibility="collapsed")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    st.success("¡Registro completado!"); st.balloons()
if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    st.success("¡Registro completado!"); st.balloons()

