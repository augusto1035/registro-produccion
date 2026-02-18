import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Producción Plaza's", layout="wide")

# --- CSS INTELIGENTE (WEB NORMAL vs MÓVIL FORZADO) ---
st.markdown("""
    <style>
    /* 1. MODO CLARO OBLIGATORIO */
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #ffffff !important; color: black !important; }

    /* 2. HEADER Y CINTILLO (GLOBAL) */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* 3. ESTILOS DE COMPONENTES (BLANCO Y NEGRO) */
    div[data-baseweb="select"] > div, 
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #999 !important;
        border-radius: 4px !important;
        font-size: 13px !important;
    }

    /* Caja de Código Base */
    .codigo-box {
        background-color: #e0e0e0;
        border: 1px solid #999;
        color: black;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        width: 100%;
        height: 100%;
        min-height: 40px;
        font-size: 11px;
    }

    /* Botones Verdes */
    .stButton > button {
        background-color: #36b04b !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #2a8a3b !important; }

    /* ============================================================
       4. MEDIA QUERY: REGLAS SOLO PARA MÓVIL (< 640px)
       Aquí prohibimos el apilamiento
       ============================================================ */
    @media (max-width: 640px) {
        
        /* A. DETECTAR FILAS DE 4 COLUMNAS (PRODUCTOS) Y FORZAR FILA ÚNICA */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(4)) {
            flex-direction: row !important; /* OBLIGAR HORIZONTAL */
            flex-wrap: nowrap !important;   /* PROHIBIR APILAR */
            display: flex !important;
            gap: 2px !important;
        }

        /* B. PERMITIR QUE LAS COLUMNAS SE ENCOJAN AL MÁXIMO */
        [data-testid="column"] {
            min-width: 0px !important;
            width: auto !important;
            padding: 0px !important;
        }

        /* C. ANCHOS EXACTOS PIXEL POR PIXEL (SOLO MÓVIL) */
        
        /* Columna 1: CÓDIGO (45px - Solo el numero) */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(4)) > [data-testid="column"]:nth-child(1) {
            flex: 0 0 45px !important;
            width: 45px !important;
            overflow: hidden !important;
        }

        /* Columna 2: DESCRIPCIÓN (Flexible - Todo lo que sobra) */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(4)) > [data-testid="column"]:nth-child(2) {
            flex: 1 1 auto !important;
            overflow: hidden !important;
        }

        /* Columna 3: CANTIDAD (50px - Solo 4 digitos) */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(4)) > [data-testid="column"]:nth-child(3) {
            flex: 0 0 50px !important;
            width: 50px !important;
        }

        /* Columna 4: X (35px) */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(4)) > [data-testid="column"]:nth-child(4) {
            flex: 0 0 35px !important;
            width: 35px !important;
        }

        /* D. REDUCIR ALTURA DE COMPONENTES EN MÓVIL */
        div[data-baseweb="select"] > div, 
        [data-testid="stNumberInput"] input,
        .codigo-box,
        .stButton > button {
            min-height: 35px !important;
            height: 35px !important;
            font-size: 10px !important;
            padding: 0px 2px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (HTML Puro) ---
def render_header(logo_path):
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding-bottom: 10px; border-bottom: 3px solid #36b04b; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" style="height: 70px; margin-right: 15px;">
                <div>
                    <div style="color:#1a3a63; font-size:22px; font-weight:800; line-height:1.1;">Registro de Producción</div>
                    <div style="color:#444; font-size:13px;">Gerencia de Alimentos Procesados</div>
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

# SUPERVISOR Y FECHA (Estos usan columnas estándar de Streamlit)
col_sup, col_fec = st.columns(2)
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec: fecha_sel = st.date_input("Fecha", datetime.now())

# RENDERIZADO
for seccion in SECCIONES_ORDEN:
    st.markdown(f'<div style="background:#f0f2f6; padding:4px; text-align:center; font-weight:bold; margin-top:15px; border-radius:4px; color:black; font-size:14px;">{seccion}</div>', unsafe_allow_html=True)
    
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    if not opciones: continue

    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        # COLUMNAS: En Web se verá normal, en móvil el CSS las fuerza.
        c1, c2, c3, c4 = st.columns(4) 
        
        with c1:
            st.markdown(f'<div class="codigo-box">{item["Codigo"]}</div>', unsafe_allow_html=True)
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
st.markdown('<p style="font-weight:bold; font-size:12px; color:black;">Observaciones:</p>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Notas...", label_visibility="collapsed")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    st.success("¡Registro completado!"); st.balloons()

