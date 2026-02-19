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

# --- CSS VISUAL BLINDADO (PARA MODO CLARO Y OSCURO) ---
st.markdown("""
    <style>
    /* 1. Forzar fondo blanco en todas las capas posibles */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }

    /* 2. Forzar texto negro en TODO (Supervisor, Fecha, Tablas, Markdown) */
    * {
        color: #000000 !important;
    }

    /* 3. Excepción para el texto dentro de los encabezados verdes (Secciones) */
    .section-header, .section-header * {
        background-color: #36b04b !important;
        color: #ffffff !important;
    }

    /* 4. Estilo de los inputs (Para que se vea lo que escriben) */
    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: #f1f3f5 !important;
        color: #000000 !important;
        border: 1px solid #ced4da !important;
    }

    /* 5. Estilo de los Botones (Texto Blanco Siempre) */
    .stButton > button {
        background-color: #36b04b !important;
        border: none !important;
    }
    .stButton > button p, .stButton > button span {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* 6. Cuadro de Resumen para Capture */
    .resumen-box {
        background-color: #ffffff !important;
        padding: 20px;
        border: 3px solid #36b04b;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* 7. Ajuste de las cajas de código */
    .codigo-box {
        background-color: #e9ecef !important;
        color: #000000 !important;
        font-weight: bold;
        padding: 5px;
        text-align: center;
        border-radius: 4px;
        min-height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 8. Quitar el índice de las tablas de Streamlit */
    [data-testid="stTable"] thead th:first-child { display: none; }
    [data-testid="stTable"] tbody td:first-child { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN CARGAR LOGO ---
def render_header():
    try:
        with open("logo_plaza.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding-bottom: 10px; border-bottom: 4px solid #36b04b; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" style="height: 70px; margin-right: 15px; object-fit: contain;">
                <div>
                    <h2 style="color:#1a3a63 !important; margin:0; font-weight:900; font-size: 20px;">Registro de Producción</h2>
                    <p style="color:#666 !important; margin:0; font-size: 12px;">Gerencia de Alimentos Procesados</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='color:#36b04b;'>Registro de Producción Plaza's</h2>", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in ["BASES, BISCOCHOS Y TARTALETAS", "DECORACIÓN", "PANES", "POSTRE", "RELLENOS Y CREMAS"]}
if 'exito' not in st.session_state:
    st.session_state.exito = False
if 'datos_finales' not in st.session_state:
    st.session_state.datos_finales = None

# --- VISTA DE RESUMEN (CAPTURE) ---
if st.session_state.exito and st.session_state.datos_finales:
    render_header()
    df_res = st.session_state.datos_finales['df']
    meta = st.session_state.datos_finales['meta']

    st.markdown('<div class="resumen-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #36b04b;'>✓ REPORTE DE PRODUCCIÓN</h2>", unsafe_allow_html=True)
    st.write(f"**Supervisor:** {meta['supervisor']}")
    st.write(f"**Fecha y Hora:** {meta['fecha_hora']}")
    st.write("---")
    
    st.table(df_res)
    
    if meta['obs']:
        st.markdown(f"**Observaciones:** {meta['obs']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("📸 *Toma un capture para WhatsApp.*")
    if st.button("Nuevo Registro"):
        st.session_state.exito = False
        st.session_state.datos_finales = None
        st.rerun()
    st.stop()

# --- FORMULARIO PRINCIPAL ---
render_header()
col_sup, col_fec = st.columns(2)
with col_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado", "Jesus Ramirez"])
with col_fec: fecha_sel = st.date_input("Fecha", hora_actual.date())

# DATA PRODUCTOS (Lista original)
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

def actualizar_producto(seccion_key, index_key, selectbox_key):
    nuevo_nombre = st.session_state[selectbox_key]
    nuevo_codigo = df_productos[df_productos['Descripcion'] == nuevo_nombre]['Codigo'].values[0]
    st.session_state.secciones_data[seccion_key][index_key]['Descripcion'] = nuevo_nombre
    st.session_state.secciones_data[seccion_key][index_key]['Codigo'] = nuevo_codigo

for seccion in SECCIONES_ORDEN:
    st.markdown(f'<div class="section-header">{seccion}</div>', unsafe_allow_html=True)
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    
    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        c1, c2, c3, c4 = st.columns([2, 5, 2, 1])
        with c1: st.markdown(f'<div class="codigo-box">{item["Codigo"]}</div>', unsafe_allow_html=True)
        with c2:
            key_sel = f"sel_{seccion}_{i}"
            st.selectbox("d", opciones, index=opciones.index(item['Descripcion']), key=key_sel, label_visibility="collapsed", on_change=actualizar_producto, args=(seccion, i, key_sel))
        with c3:
            item['Cantidad'] = st.number_input(f"Cant", min_value=0, step=1, key=f"q_{seccion}_{i}", label_visibility="collapsed")
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir {seccion}", key=f"add_{seccion}"):
        st.session_state.secciones_data[seccion].append({"Codigo": df_productos[df_productos['Seccion']==seccion].iloc[0]['Codigo'], "Descripcion": opciones[0], "Cantidad": 0})
        st.rerun()

st.write("---")
obs_input = st.text_area("Observaciones", placeholder="Notas...")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    f_h = datetime.now(ve_tz).strftime("%d/%m/%Y %I:%M %p")
    
    filas_hoja = []
    filas_resumen = []
    
    for sec, items in st.session_state.secciones_data.items():
        for it in items:
            if it['Cantidad'] > 0:
                filas_hoja.append({
                    "ID_Registro": datetime.now(ve_tz).strftime("%Y%m%d%H%M%S"),
                    "Supervisor": supervisor, "Fecha_Hora": f_h,
                    "Codigo_Articulo": it['Codigo'], "Descripcion": it['Descripcion'],
                    "Cantidad": it['Cantidad'], "Observaciones": obs_input
                })
                filas_resumen.append({
                    "Código": it['Codigo'],
                    "Producto": it['Descripcion'],
                    "Cant.": it['Cantidad']
                })

    if filas_hoja:
        df_total = pd.concat([conn.read(worksheet="Hoja1", ttl=0), pd.DataFrame(filas_hoja)], ignore_index=True)
        conn.update(worksheet="Hoja1", data=df_total)
        st.session_state.datos_finales = {"df": pd.DataFrame(filas_resumen), "meta": {"supervisor": supervisor, "fecha_hora": f_h, "obs": obs_input}}
        st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}
        st.session_state.exito = True
        st.rerun()
    else:
        st.warning("Sin registros.")
