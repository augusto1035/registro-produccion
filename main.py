import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. BASE DE DATOS MAESTRA
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

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Gerencia de Alimentos Procesados", layout="wide")

st.markdown("""
    <style>
    /* 1. Fondo principal y forzado de modo claro */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: white !important;
        color: black !important;
    }

    /* 2. FORZADO DE TEXTO NEGRO EN LISTAS DESPLEGABLES (Flotantes) */
    /* Este es el selector que controla el menú cuando se abre */
    div[data-baseweb="popover"], div[role="listbox"], div[data-baseweb="menu"] {
        background-color: white !important;
    }
    
    div[data-baseweb="popover"] *, div[role="listbox"] *, div[role="option"] * {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* 3. Encabezado */
    .header { background-color: #36b04b !important; padding: 15px; text-align: center; border-radius: 5px; }
    .header-text { color: white !important; -webkit-text-fill-color: white !important; font-weight: bold; font-size: 24px; }
    .header-subtext { color: white !important; -webkit-text-fill-color: white !important; font-size: 14px; }

    /* 4. Títulos de secciones */
    .section-header { background-color: #f0f2f6 !important; color: #333 !important; padding: 10px; font-weight: bold; text-align: center; margin-top: 25px; border-radius: 5px; border: 1px solid #ddd; }

    /* 5. Caja de Código SAP */
    .codigo-box { background-color: #f0f0f0 !important; color: black !important; padding: 8px; border-radius: 4px; text-align: center; font-family: monospace; border: 1px solid #ccc; height: 38px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
    
    /* 6. Botones Negros */
    .stButton > button { 
        background-color: black !important; 
        border: none !important;
    }
    .stButton > button p, .stButton > button div, .stButton > button span {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    /* 7. Inputs y Selectores cerrados */
    div[data-baseweb="select"] > div, input, textarea {
        background-color: white !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
        border: 1px solid #ccc !important;
    }
    
    /* 8. CALENDARIO */
    div[data-baseweb="calendar"] * {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }
    </style>
    
    <div class="header">
        <div class="header-text">Registro de producción</div>
        <div class="header-subtext">Gerencia de Alimentos Procesados</div>
    </div>
    """, unsafe_allow_html=True)

# 2. SECCIONES
SECCIONES = ["BASES, BISCOCHOS Y TARTALETAS", "DECORACIÓN", "PANES", "POSTRE", "RELLENOS Y CREMAS"]

if 'secciones_data' not in st.session_state:
    st.session_state.secciones_data = {sec: [] for sec in SECCIONES}

# Columnas Supervisor y Fecha
col_sup, col_fec = st.columns(2)
with col_sup:
    supervisor = st.selectbox("Supervisor", ["Pedro Navarro", "Ronald Rosales", "Ervis Hurtado"])
with col_fec:
    fecha_sel = st.date_input("Fecha", datetime.now())

# RENDERIZADO
for seccion in SECCIONES:
    st.markdown(f'<div class="section-header">{seccion}</div>', unsafe_allow_html=True)
    opciones = df_productos[df_productos['Seccion'] == seccion]['Descripcion'].tolist()
    
    if not opciones: continue

    for i, item in enumerate(st.session_state.secciones_data[seccion]):
        c1, c2, c3, c4 = st.columns([1, 3.2, 1, 0.3])
        
        with c2:
            seleccion = st.selectbox(f"S_{seccion}_{i}", options=opciones, key=f"sel_{seccion}_{i}", label_visibility="collapsed")
            item['Descripcion'] = seleccion
            match = df_productos[df_productos['Descripcion'] == seleccion]
            item['Codigo'] = match['Codigo'].values[0] if not match.empty else "N/A"

        with c1:
            st.markdown(f'<div class="codigo-box">{item["Codigo"]}</div>', unsafe_allow_html=True)
            
        with c3:
            item['Cantidad'] = st.number_input(f"Q_{seccion}_{i}", min_value=0, value=item['Cantidad'], key=f"q_{seccion}_{i}", label_visibility="collapsed")
            
        with c4:
            if st.button("X", key=f"x_{seccion}_{i}"):
                st.session_state.secciones_data[seccion].pop(i)
                st.rerun()

    if st.button(f"➕ Añadir a {seccion.lower()}", key=f"btn_{seccion}"):
        primera_desc = opciones[0]
        primer_cod = df_productos[df_productos['Descripcion'] == primera_desc]['Codigo'].values[0]
        st.session_state.secciones_data[seccion].append({"Codigo": primer_cod, "Descripcion": primera_desc, "Cantidad": 0})
        st.rerun()

st.write("---")
obs = st.text_area("Observaciones", placeholder="Escriba aquí sus notas...")

if st.button("FINALIZAR Y GUARDAR TODO", type="primary", use_container_width=True):
    all_data = []
    for seccion in SECCIONES:
        for row in st.session_state.secciones_data[seccion]:
            if row['Cantidad'] > 0:
                all_data.append({
                    "ID_Registro": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "Supervisor": supervisor,
                    "Fecha_Hora": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
                    "Codigo_Articulo": row['Codigo'],
                    "Descripcion": row['Descripcion'],
                    "Cantidad": row['Cantidad'],
                    "Observaciones": obs
                })
    
    if all_data:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_actual = conn.read()
            df_final = pd.concat([df_actual, pd.DataFrame(all_data)], ignore_index=True)
            conn.update(data=df_final)
            st.success("¡Guardado exitoso!"); st.balloons()
            for sec in SECCIONES: st.session_state.secciones_data[sec] = []
            st.rerun()
        except Exception as e: st.error(f"Error: {e}")
