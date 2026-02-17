import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# URL de tu Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sE01duwpnHp2NmsBoJIOP7Csm-wEpe1M/edit?usp=sharing&ouid=106427842999101731073&rtpof=true&sd=true"

st.set_page_config(page_title="Registro de produccion", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: white !important; }
    .header { background-color: #36b04b; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 24px; border-radius: 5px; }
    .section-header { color: #333333; font-weight: bold; text-align: center; margin-top: 20px; font-size: 18px; }
    .stButton > button { background-color: white !important; border: 1px solid #cccccc !important; width: 100% !important; }
    </style>
    <div class="header">Registro de produccion</div>
    """, unsafe_allow_html=True)

if 'prod' not in st.session_state: st.session_state.prod = []
if 'dec' not in st.session_state: st.session_state.dec = []

# ENCABEZADO
c1, c2 = st.columns(2)
with c1: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with c2: fecha_sel = st.date_input("Fecha", datetime.now())

# SECCIONES
for label, state_key in [("PRODUCCION", st.session_state.prod), ("DECORACION", st.session_state.dec)]:
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)
    for i, item in enumerate(state_key):
        cols = st.columns([1, 2.5, 1, 0.4])
        item['c'] = cols[0].text_input("Cod", key=f"{label}c{i}", label_visibility="collapsed", placeholder="Cod")
        item['d'] = cols[1].selectbox("Desc", ["Base Vainilla", "Chocolate", "Red Velvet", "Arequipe"], key=f"{label}d{i}", label_visibility="collapsed")
        item['q'] = cols[2].number_input("Cant", min_value=0, key=f"{label}q{i}", label_visibility="collapsed")
        if cols[3].button("X", key=f"{label}x{i}"):
            state_key.pop(i)
            st.rerun()
    if st.button(f"Anadir Item {label}"):
        state_key.append({"c": "", "d": "Base Vainilla", "q": 0})
        st.rerun()

st.write("---")
obs = st.text_area("Observaciones")

# GUARDAR
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    res = []
    # Usamos exactamente los nombres de columna de tu tabla de Google Sheets
    for x in st.session_state.prod + st.session_state.dec:
        res.append({
            "ID_Registro": datetime.now().strftime("%Y%m%d%H%M%S"),
            "Supervisor": supervisor,
            "Fecha_Hora": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "Codigo_Articulo": str(x['c']), # Forzamos a texto para evitar errores
            "Descripcion": x['d'],
            "Cantidad": x['q'],
            "Observaciones": obs
        })
    
    if res:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # 1. Leer los datos actuales
            df_actual = conn.read(spreadsheet=SHEET_URL)
            # 2. Crear el nuevo DataFrame con los mismos encabezados
            df_nuevo = pd.DataFrame(res)
            # 3. Unir y actualizar
            df_final = pd.concat([df_actual, df_nuevo], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=df_final)
            
            st.success("Guardado exitoso")
            st.session_state.prod, st.session_state.dec = [], []
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error detectado: {str(e).encode('ascii', 'ignore').decode('ascii')}")
