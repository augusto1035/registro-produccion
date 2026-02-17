import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# URL de tu Google Sheet
SHEET_URL = "TU_LINK_DE_GOOGLE_SHEETS_AQUÍ"

st.set_page_config(page_title="Registro de produccion", layout="wide")

# ESTÉTICA (Eliminamos tildes internas para evitar errores de codificación)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: white !important; }
    .header { background-color: #36b04b; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 24px; border-radius: 5px; }
    .section-header { color: #333333; font-weight: bold; text-align: center; margin-top: 20px; font-size: 20px; }
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
# Usamos nombres sin tildes internamente para evitar el error 'ascii'
for label, state_key in [("PRODUCCION", st.session_state.prod), ("DECORACION", st.session_state.dec)]:
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)
    for i, item in enumerate(state_key):
        cols = st.columns([1, 2.5, 1, 0.4])
        item['c'] = cols[0].text_input("Cod", key=f"{label}c{i}", label_visibility="collapsed")
        item['d'] = cols[1].selectbox("Desc", ["Base Vainilla", "Chocolate", "Red Velvet", "Arequipe"], key=f"{label}d{i}", label_visibility="collapsed")
        item['q'] = cols[2].number_input("Cant", min_value=0, key=f"{label}q{i}", label_visibility="collapsed")
        if cols[3].button("X", key=f"{label}x{i}"):
            state_key.pop(i)
            st.rerun()
    if st.button(f"Añadir Item {label}"):
        state_key.append({"c": "", "d": "Base Vainilla", "q": 0})
        st.rerun()

st.write("---")
obs = st.text_area("Observaciones")

# GUARDAR
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    data_to_save = []
    for x in st.session_state.prod:
        data_to_save.append([datetime.now().strftime("%Y%m%d%H%M%S"), supervisor, datetime.now().strftime("%d/%m/%Y %I:%M %p"), x['c'], x['d'], x['q'], obs])
    for x in st.session_state.dec:
        data_to_save.append([datetime.now().strftime("%Y%m%d%H%M%S"), supervisor, datetime.now().strftime("%d/%m/%Y %I:%M %p"), x['c'], x['d'], x['q'], obs])
    
    if data_to_save:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # Intentamos leer la hoja
            existing_data = conn.read(spreadsheet=SHEET_URL)
            new_df = pd.DataFrame(data_to_save, columns=existing_data.columns)
            updated_df = pd.concat([existing_data, new_df], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success("Guardado exitoso")
            st.session_state.prod, st.session_state.dec = [], []
            st.rerun()
        except Exception as e:
            st.error(f"Error: Verifique que el link en Secrets sea correcto y la hoja tenga los encabezados. {e}")
