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

# --- CSS BLINDADO (REPARACIÓN MODO OSCURO Y SECCIONES DELGADAS) ---
st.markdown("""
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    h1, h2, h3, p, span, label, td, th, div, li, input, select {
        color: #000000 !important;
    }
    .section-header {
        background-color: #36b04b !important;
        padding: 4px 10px !important;
        border-radius: 4px;
        margin: 10px 0px 8px 0px !important;
        width: 100%;
        text-align: center;
    }
    .section-header h3 {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 0.9rem !important;
        font-weight: bold;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #36b04b !important;
    }
    div[data-baseweb="select"] * { color: #000000 !important; }
    .stButton > button {
        background-color: #36b04b !important;
        color: #ffffff !important;
        border: none !important;
    }
    .stButton > button p, .stButton > button span {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    .resumen-box {
        background-color: #ffffff !important;
        padding: 15px;
        border: 2px solid #36b04b;
        border-radius: 8px;
    }
    [data-testid="stTable"] thead th:first-child, 
    [data-testid="stTable"] tbody td:first-child { 
        display: none !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
def render_header():
    try:
        with open("logo_plaza.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; align-items: center; border-bottom: 2px solid #36b04b; padding-bottom: 8px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{data}" style="height: 50px; margin-right: 15px;">
                <div>
                    <h2 style="color:#1a3a63 !important; margin:0; font-size: 1.2rem;">Registro de Producción</h2>
                    <p style="color:#666 !important; margin:0; font-size: 0.7rem;">Gerencia de Alimentos Procesados</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='color:#36b04b !important; margin:0;'>🟢 Registro de Producción Plaza's</h2>", unsafe_allow_html=True)

# --- PRODUCTOS ---
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

# --- ESTADOS ---
if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}
if 'exito' not in st.session_state:
    st.session_state.exito = False
if 'final_data' not in st.session_state:
    st.session_state.final_data = None

# --- VISTA RESUMEN ---
if st.session_state.exito and st.session_state.final_data:
    render_header()
    fd = st.session_state.final_data
    st.markdown('<div class="resumen-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #36b04b;'>REPORTE DE PRODUCCIÓN</h2>", unsafe_allow_html=True)
    st.write(f"**Supervisor:** {fd['supervisor']}")
    st.write(f"**Fecha y Hora:** {fd['fecha_hora']}")
    st.write("---")
    st.table(fd['df'])
    if fd['obs']: st.write(f"**Observaciones:** {fd['obs']}")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Hacer otro registro"):
        st.session_state.exito = False
        st.rerun()
    st.stop()

# --- FORMULARIO ---
render_header()
c_sup, c_fec = st.columns(2)
with c_sup: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado", "Jesus Ramirez"])
with c_fec: fecha_sel = st.date_input("Fecha", hora_actual.date())

def act_prod(sec, idx, key):
    nom = st.session_state[key]
    cod = df_productos[df_productos['Descripcion'] == nom]['Codigo'].values[0]
    st.session_state.secciones_data[sec][idx]['Descripcion'] = nom
    st.session_state.secciones_data[sec][idx]['Codigo'] = cod

for sec in SECCIONES_ORDEN:
    st.markdown(f'<div class="section-header"><h3>{sec}</h3></div>', unsafe_allow_html=True)
    opcs = df_productos[df_productos['Seccion'] == sec]['Descripcion'].tolist()
    
    for i, item in enumerate(st.session_state.secciones_data[sec]):
        col1, col2, col3, col4 = st.columns([1, 4.5, 1.5, 0.5])
        with col1: st.write(item['Codigo'])
        with col2:
            key = f"sel_{sec}_{i}"
            st.selectbox("P", opcs, index=opcs.index(item['Descripcion']), key=key, label_visibility="collapsed", on_change=act_prod, args=(sec, i, key))
        with col3:
            item['Cantidad'] = st.number_input("C", min_value=0, step=1, key=f"q_{sec}_{i}", label_visibility="collapsed")
        with col4:
            if st.button("X", key=f"x_{sec}_{i}"):
                st.session_state.secciones_data[sec].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir {sec}", key=f"add_{sec}"):
        st.session_state.secciones_data[sec].append({"Codigo": df_productos[df_productos['Seccion']==sec].iloc[0]['Codigo'], "Descripcion": opcs[0], "Cantidad": 0})
        st.rerun()

st.write("---")
obs = st.text_area("Observaciones")

# --- GUARDADO CORREGIDO ---
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    f_h = datetime.now(ve_tz).strftime("%d/%m/%Y %I:%M %p")
    id_reg = datetime.now(ve_tz).strftime("%Y%m%d%H%M%S")
    
    filas_hoja = []
    filas_resumen = []
    
    for s, items in st.session_state.secciones_data.items():
        for it in items:
            if it['Cantidad'] > 0:
                # ESTRUCTURA EXACTA DE TU GOOGLE SHEETS (Columnas A a G)
                filas_hoja.append({
                    "ID_Registro": id_reg,
                    "Supervisor": supervisor,
                    "Fecha_Hora": f_h,
                    "Codigo_Articulo": it['Codigo'],
                    "Descripcion": it['Descripcion'],
                    "Cantidad": it['Cantidad'],
                    "Observaciones": obs
                })
                # Estructura visual para el reporte en pantalla
                filas_resumen.append({
                    "Código": it['Codigo'],
                    "Producto": it['Descripcion'],
                    "Cant.": it['Cantidad']
                })

    if filas_hoja:
        try:
            # Leer datos actuales
            df_existente = conn.read(worksheet="Hoja1", ttl=0)
            
            # Asegurar que solo usamos las primeras 7 columnas si hay basura a la derecha
            df_existente = df_existente.iloc[:, :7]
            
            # Crear el nuevo bloque de datos con las mismas columnas
            df_nuevo = pd.DataFrame(filas_hoja)
            
            # Unir y actualizar
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            conn.update(worksheet="Hoja1", data=df_final)
            
            # Guardar para la vista de resumen
            st.session_state.final_data = {
                "df": pd.DataFrame(filas_resumen).set_index("Código"),
                "supervisor": supervisor,
                "fecha_hora": f_h,
                "obs": obs
            }
            st.session_state.secciones_data = {sec: [] for sec in SECCIONES_ORDEN}
            st.session_state.exito = True
            st.rerun()
        except Exception as e:
            st.error(f"Error al conectar: {e}")

