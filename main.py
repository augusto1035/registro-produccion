import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# URL de tu Google Sheet (PEGA AQUÍ EL LINK QUE COPIASTE EN EL PASO 1)
SHEET_URL = "AQUÍ_PEGA_TU_LINK_DE_GOOGLE_SHEETS"

# CONFIGURACIÓN ESTÉTICA (Estilo Power Apps - Blanco)
st.set_page_config(page_title="Registro de producción", layout="wide")
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: white !important; }
    .header { background-color: #36b04b; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 24px; border-radius: 5px; }
    .section-header { color: #333333; font-weight: bold; text-align: center; margin-top: 20px; }
    .stButton > button { background-color: white !important; border: 1px solid #cccccc !important; width: 100% !important; }
    </style>
    <div class="header">Registro de producción</div>
    """, unsafe_allow_html=True)

if 'prod' not in st.session_state: st.session_state.prod = []
if 'dec' not in st.session_state: st.session_state.dec = []

# ENCABEZADO
c1, c2 = st.columns(2)
with c1: supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with c2: fecha_sel = st.date_input("Fecha", datetime.now())

# SECCIONES (Producción y Decoración)
for label, state_key in [("PRODUCCIÓN", st.session_state.prod), ("DECORACIÓN", st.session_state.dec)]:
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)
    for i, item in enumerate(state_key):
        cols = st.columns([1, 2.5, 1, 0.4])
        item['c'] = cols[0].text_input("C", key=f"{label}c{i}", label_visibility="collapsed")
        item['d'] = cols[1].selectbox("D", ["Base Vainilla", "Chocolate", "Red Velvet", "Arequipe"], key=f"{label}d{i}", label_visibility="collapsed")
        item['q'] = cols[2].number_input("Q", min_value=0, key=f"{label}q{i}", label_visibility="collapsed")
        if cols[3].button("X", key=f"{label}x{i}"):
            state_key.pop(i)
            st.rerun()
    if st.button(f"➕ AÑADIR ITEM {label}"):
        state_key.append({"c": "", "d": "Base Vainilla", "q": 0})
        st.rerun()

st.write("---")
obs = st.text_area("Observaciones")

# GUARDAR EN GOOGLE SHEETS
if st.button("FINALIZAR Y GUARDAR TODO", type="primary"):
    data_to_save = []
    for x in st.session_state.prod + st.session_state.dec:
        data_to_save.append([
            datetime.now().strftime("%Y%m%d%H%M%S"), supervisor, 
            datetime.now().strftime("%d/%m/%Y %I:%M %p"), x['c'], x['d'], x['q'], obs
        ])
    
    if data_to_save:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_data = conn.read(spreadsheet=SHEET_URL)
            new_df = pd.DataFrame(data_to_save, columns=existing_data.columns)
            updated_df = pd.concat([existing_data, new_df], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success("✅ Guardado en Google Sheets")
            st.session_state.prod, st.session_state.dec = [], []
            st.rerun()
        except Exception as e: st.error(f"Error de conexión: {e}")
        except Exception as e:
            st.error(f"Error: Cierra el archivo Excel. {e}")
    else:

        st.warning("No hay ítems para registrar.")
