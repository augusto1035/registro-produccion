import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Registro de producción", layout="wide")

# 2. ESTILO VISUAL (Fondo blanco, botones estilo Power Apps, sin sombras)
st.markdown("""
    <style>
    /* Fondo blanco total */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: white !important;
        color: #31333F !important;
    }
    
    /* Encabezado Verde IESA */
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

    /* Títulos de Sección (PRODUCCIÓN / DECORACIÓN) */
    .section-header {
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }

    /* BOTONES BLANCOS CON BORDE OSCURO */
    .stButton > button {
        background-color: white !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 4px !important;
        width: 100% !important;
        height: 40px !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        border-color: #36b04b !important;
        color: #36b04b !important;
    }

    /* Botón X para eliminar (Rojo y sin bordes) */
    div[data-testid="stColumn"] > div > div > div > div > .stButton > button {
        border: none !important;
        color: #cc0000 !important;
        background: transparent !important;
        font-size: 18px !important;
    }

    /* Inputs y Selectores siempre blancos */
    input, div[data-baseweb="select"], div[data-baseweb="input"], .stNumberInput div {
        background-color: white !important;
        color: black !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Eliminar sombras de los bloques */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }
    </style>
    
    <div class="header">Registro de producción</div>
    """, unsafe_allow_html=True)

# 3. INICIALIZACIÓN DE VARIABLES DE SESIÓN
if 'prod' not in st.session_state: st.session_state.prod = []
if 'dec' not in st.session_state: st.session_state.dec = []

# 4. ENCABEZADO DE SUPERVISOR Y FECHA
c1, c2 = st.columns(2)
with c1:
    supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with c2:
    fecha_sel = st.date_input("Fecha de Registro", datetime.now())

# 5. SECCIÓN DE PRODUCCIÓN
st.markdown('<div class="section-header">PRODUCCIÓN</div>', unsafe_allow_html=True)
for i, item in enumerate(st.session_state.prod):
    cols = st.columns([1, 3, 1, 0.3])
    with cols[0]: item['c'] = st.text_input("Cod", value=item['c'], key=f"pc{i}", label_visibility="collapsed", placeholder="Cód")
    with cols[1]: item['d'] = st.selectbox("Desc", ["Base Vainilla pequeña", "Chocolate", "Red Velvet"], index=0, key=f"pd{i}", label_visibility="collapsed")
    with cols[2]: item['q'] = st.number_input("Cant", value=item['q'], min_value=0, key=f"pq{i}", label_visibility="collapsed")
    with cols[3]: 
        if st.button("X", key=f"px{i}"):
            st.session_state.prod.pop(i)
            st.rerun()

if st.button("➕ AÑADIR ITEM PRODUCCIÓN", key="add_p"):
    st.session_state.prod.append({"c": "", "d": "Base Vainilla pequeña", "q": 0})
    st.rerun()

# 6. SECCIÓN DE DECORACIÓN
st.markdown('<div class="section-header">DECORACIÓN</div>', unsafe_allow_html=True)
for i, item in enumerate(st.session_state.dec):
    cols = st.columns([1, 3, 1, 0.3])
    with cols[0]: item['c'] = st.text_input("Cod", value=item['c'], key=f"dc{i}", label_visibility="collapsed", placeholder="Cód")
    with cols[1]: item['d'] = st.selectbox("Desc", ["Arequipe", "Coco Arequipe", "Lluvia de Chocolate"], index=0, key=f"dd{i}", label_visibility="collapsed")
    with cols[2]: item['q'] = st.number_input("Cant", value=item['q'], min_value=0, key=f"dq{i}", label_visibility="collapsed")
    with cols[3]: 
        if st.button("X", key=f"dx{i}"):
            st.session_state.dec.pop(i)
            st.rerun()

if st.button("➕ AÑADIR ITEM DECORACIÓN", key="add_d"):
    st.session_state.dec.append({"c": "", "d": "Arequipe", "q": 0})
    st.rerun()

st.write("---")
# 7. OBSERVACIONES
obs = st.text_area("Observaciones", placeholder="Escriba notas adicionales aquí...")

# 8. BOTÓN FINALIZAR Y GUARDAR (CONEXIÓN GOOGLE SHEETS)
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    res = []
    # Consolidar ambas listas
    for x in st.session_state.prod + st.session_state.dec:
        res.append({
            "ID_Registro": datetime.now().strftime("%Y%m%d%H%M%S"),
            "Supervisor": supervisor,
            "Fecha_Hora": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "Codigo_Articulo": str(x['c']),
            "Descripcion": x['d'],
            "Cantidad": x['q'],
            "Observaciones": obs
        })
    
    if res:
        try:
            # Conexión usando los Secrets configurados
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_actual = conn.read()
            df_nuevo = pd.DataFrame(res)
            
            # Unir datos nuevos con los existentes
            df_final = pd.concat([df_actual, df_nuevo], ignore_index=True)
            
            # Actualizar la hoja de cálculo
            conn.update(data=df_final)
            
            st.success("✅ ¡Datos guardados exitosamente en Google Sheets!")
            st.balloons()
            
            # Limpiar el formulario
            st.session_state.prod = []
            st.session_state.dec = []
            st.rerun()
            
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")
    else:
        st.warning("⚠️ No hay ítems en la lista para guardar.")
