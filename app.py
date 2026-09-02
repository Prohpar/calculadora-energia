import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="Calculador MUST & BLUETTI", page_icon="⚡", layout="centered")

# --- INYECCIÓN DE CSS PARA MARCA DE AGUA DE PRODIMIC ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64_image("logo_prodimic.png")

if logo_b64:
    bg_style = f"data:image/png;base64,{logo_b64}"
else:
    # URL pública de respaldo o nombre de archivo directo
    bg_style = "logo_prodimic.png"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("{bg_style}");
    background-repeat: no-repeat;
    background-position: center 40%;
    background-size: 55% auto;
    opacity: 0.4; /* Opacidad tipo marca de agua (8%) */
    pointer-events: none;
    z-index: 0;
}}
</style>
""", unsafe_allow_html=True)

# --- FIN INYECCIÓN CSS ---

st.title("⚡ Calculador de Respaldo MUST & BLUETTI")
st.caption("Distribuidora Prodimic — Dimensionamiento directo de potencia, energía y picos de arranque.")

# Base de equipos completa (56 items)
EQUIPOS_BASE = {
    'Bombillo LED 18W': {'w': 18, 'arr': 1.0},
    'Router / módem': {'w': 17, 'arr': 1.0},
    'Cargador de teléfono': {'w': 15, 'arr': 1.0},
    'Monitor': {'w': 30, 'arr': 1.1},
    'Impresora de tinta': {'w': 30, 'arr': 1.2},
    'Sistema CCTV': {'w': 60, 'arr': 1.2},
    'Laptop': {'w': 65, 'arr': 1.0},
    'Ventilador': {'w': 80, 'arr': 2.0},
    'Televisor LED 32"': {'w': 45, 'arr': 1.2},
    'Televisor LED 40" / 43"': {'w': 65, 'arr': 1.2},
    'Televisor LED 50"': {'w': 90, 'arr': 1.2},
    'Televisor LED 55"': {'w': 120, 'arr': 1.2},
    'Televisor LED 65"': {'w': 160, 'arr': 1.2},
    'Televisor LED 75"': {'w': 200, 'arr': 1.2},
    'Televisor LED (genérico)': {'w': 100, 'arr': 1.2},
    'Nevera': {'w': 200, 'arr': 3.0},
    'Computadora de escritorio': {'w': 250, 'arr': 1.5},
    'Congelador': {'w': 250, 'arr': 3.0},
    'Licuadora': {'w': 500, 'arr': 2.0},
    'Impresora láser': {'w': 600, 'arr': 2.0},
    'Bomba de agua 1/2 HP': {'w': 750, 'arr': 3.0},
    'Cafetera eléctrica': {'w': 1000, 'arr': 1.0},
    'Microondas': {'w': 1200, 'arr': 1.3},
    'Secador de cabello': {'w': 1500, 'arr': 1.0},
    'Herramienta eléctrica': {'w': 1500, 'arr': 2.5},
    'Aire acondicionado 5.000 BTU — convencional': {'w': 500, 'arr': 3.0},
    'Aire acondicionado 5.000 BTU — inverter': {'w': 500, 'arr': 1.5},
    'Aire acondicionado 6.000 BTU — convencional': {'w': 600, 'arr': 3.0},
    'Aire acondicionado 6.000 BTU — inverter': {'w': 600, 'arr': 1.5},
    'Aire acondicionado 8.000 BTU — convencional': {'w': 800, 'arr': 3.0},
    'Aire acondicionado 8.000 BTU — inverter': {'w': 800, 'arr': 1.5},
    'Aire acondicionado 9.000 BTU — convencional': {'w': 900, 'arr': 3.0},
    'Aire acondicionado 9.000 BTU — inverter': {'w': 900, 'arr': 1.5},
    'Aire acondicionado 10.000 BTU — convencional': {'w': 1000, 'arr': 3.0},
    'Aire acondicionado 10.000 BTU — inverter': {'w': 1000, 'arr': 1.5},
    'Aire acondicionado 12.000 BTU (1 ton) — convencional': {'w': 1200, 'arr': 3.0},
    'Aire acondicionado 12.000 BTU (1 ton) — inverter': {'w': 1200, 'arr': 1.5},
    'Aire acondicionado 15.000 BTU (1,25 ton) — convencional': {'w': 1500, 'arr': 3.0},
    'Aire acondicionado 15.000 BTU (1,25 ton) — inverter': {'w': 1500, 'arr': 1.5},
    'Aire acondicionado 18.000 BTU (1,5 ton) — convencional': {'w': 1800, 'arr': 3.0},
    'Aire acondicionado 18.000 BTU (1,5 ton) — inverter': {'w': 1800, 'arr': 1.5},
    'Aire acondicionado 24.000 BTU (2 ton) — convencional': {'w': 2400, 'arr': 3.0},
    'Aire acondicionado 24.000 BTU (2 ton) — inverter': {'w': 2400, 'arr': 1.5},
    'Aire acondicionado 30.000 BTU (2,5 ton) — convencional': {'w': 3000, 'arr': 3.0},
    'Aire acondicionado 30.000 BTU (2,5 ton) — inverter': {'w': 3000, 'arr': 1.5},
    'Aire acondicionado 36.000 BTU (3 ton) — convencional': {'w': 3600, 'arr': 3.0},
    'Aire acondicionado 36.000 BTU (3 ton) — inverter': {'w': 3600, 'arr': 1.5},
    'Aire acondicionado 42.000 BTU (3,5 ton) — convencional': {'w': 4200, 'arr': 3.0},
    'Aire acondicionado 42.000 BTU (3,5 ton) — inverter': {'w': 4200, 'arr': 1.5},
    'Aire acondicionado 48.000 BTU (4 ton) — convencional': {'w': 4800, 'arr': 3.0},
    'Aire acondicionado 48.000 BTU (4 ton) — inverter': {'w': 4800, 'arr': 1.5},
    'Aire acondicionado 54.000 BTU (4,5 ton) — convencional': {'w': 5400, 'arr': 3.0},
    'Aire acondicionado 54.000 BTU (4,5 ton) — inverter': {'w': 5400, 'arr': 1.5},
    'Aire acondicionado 60.000 BTU (5 ton) — convencional': {'w': 6000, 'arr': 3.0},
    'Aire acondicionado 60.000 BTU (5 ton) — inverter': {'w': 6000, 'arr': 1.5},
    'Otro / manual': {'w': 0, 'arr': 1.0}
}

CATALOGO_BLUETTI = [
    {"modelo": "AC2P", "w": 300, "pico": 600, "wh_util": 195.84},
    {"modelo": "Premium 30 V2", "w": 600, "pico": 1500, "wh_util": 272.00},
    {"modelo": "AC50P", "w": 700, "pico": 1200, "wh_util": 428.40},
    {"modelo": "AC70P", "w": 1000, "pico": 2000, "wh_util": 734.40},
    {"modelo": "Premium 100 V2", "w": 2000, "pico": 3600, "wh_util": 870.40},
    {"modelo": "Premium 200 V2", "w": 2700, "pico": 3900, "wh_util": 1762.56},
    {"modelo": "Apex 300", "w": 3840, "pico": 3840, "wh_util": 2350.08},
]

# Catálogo MUST con picos ajustados: EP30 (9 kVA), PV33 (12 kVA), PV39 (36 kVA)
CATALOGO_MUST = [
    {"modelo": "EP30-3024 LV2 + batería 24V 100Ah", "w": 3000, "pico": 9000, "wh_util": 1843.2},
    {"modelo": "EP30-3024 LV2 + 2x batería 24V 100Ah", "w": 3000, "pico": 9000, "wh_util": 3686.4},
    {"modelo": "PV33-6048 TLV + LP16-48100", "w": 6000, "pico": 12000, "wh_util": 3686.4},
    {"modelo": "PV33-6048 TLV + LP16-48200", "w": 6000, "pico": 12000, "wh_util": 7372.8},
    {"modelo": "PV39-12048 TLV + LP16-48200", "w": 12000, "pico": 36000, "wh_util": 7372.8},
    {"modelo": "PV39-12048 TLV + 2x LP16-48200", "w": 12000, "pico": 36000, "wh_util": 14745.6},
]

st.subheader("1. Selección de Cargas")

if 'cargas' not in st.session_state:
    st.session_state.cargas = [
        {"equipo": "Nevera", "cant": 1, "w": 200, "arr": 3.0, "horas": 4.0, "ciclo": 0.5},
        {"equipo": "Router / módem", "cant": 1, "w": 17, "arr": 1.0, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Televisor LED 50\"", "cant": 1, "w": 90, "arr": 1.2, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Bombillo LED 18W", "cant": 6, "w": 18, "arr": 1.0, "horas": 4.0, "ciclo": 1.0},
    ]

with st.form("add_form"):
    c1, c2, c3 = st.columns([2, 1, 1])
    eq_sel = c1.selectbox("Seleccione Equipo", list(EQUIPOS_BASE.keys()))
    cant_in = c2.number_input("Cantidad", min_value=1, value=1)
    horas_in = c3.number_input("Horas uso", min_value=0.5, value=4.0, step=0.5)
    
    submitted = st.form_submit_button("➕ Agregar a la Lista")
    if submitted:
        st.session_state.cargas.append({
            "equipo": eq_sel,
            "cant": cant_in,
            "w": EQUIPOS_BASE[eq_sel]['w'],
            "arr": EQUIPOS_BASE[eq_sel]['arr'],
            "horas": horas_in,
            "ciclo": 1.0
        })

if st.session_state.cargas:
    st.write("### Lista de Cargas Seleccionadas")
    
    idx_eliminar = None
    
    col_h1, col_h2, col_h3, col_h4, col_h5, col_h6 = st.columns([2.5, 1, 1, 1, 1.2, 0.8])
    col_h1.markdown("**Equipo**")
    col_h2.markdown("**Cant.**")
    col_h3.markdown("**W Tot.**")
    col_h4.markdown("**Horas**")
    col_h5.markdown("**Wh Tot.**")
    col_h6.markdown("**Acción**")
    st.divider()

    for idx, item in enumerate(st.session_state.cargas):
        w_tot = item['cant'] * item['w']
        wh_tot = w_tot * item['horas'] * item['ciclo']
        
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1, 1, 1, 1.2, 0.8])
        col1.write(item['equipo'])
        col2.write(str(item['cant']))
        col3.write(f"{w_tot} W")
        col4.write(f"{item['horas']} h")
        col5.write(f"{wh_tot:.0f} Wh")
        
        if col6.button("🗑️", key=f"del_{idx}"):
            idx_eliminar = idx

    if idx_eliminar is not None:
        st.session_state.cargas.pop(idx_eliminar)
        st.rerun()

    st.write("---")
    if st.button("🗑️ Limpiar Toda la Lista"):
        st.session_state.cargas = []
        st.rerun()

    df = pd.DataFrame(st.session_state.cargas)
    if not df.empty:
        df['W_Total'] = df['cant'] * df['w']
        df['Wh_Total'] = df['W_Total'] * df['horas'] * df['ciclo']
        df['Extra_Arranque'] = df['W_Total'] * (df['arr'] - 1.0).clip(lower=0)

        w_req = df['W_Total'].sum()
        wh_req = df['Wh_Total'].sum()
        peor_arranque = df['Extra_Arranque'].max()
        pico_req = w_req + peor_arranque

        st.subheader("2. Requerimientos Netos del Proyecto")
        col1, col2, col3 = st.columns(3)
        col1.metric("Potencia Continua", f"{w_req:.1f} W")
        col2.metric("Energía Total", f"{wh_req:.1f} Wh")
        col3.metric("Pico de Arranque", f"{pico_req:.1f} VA")

        bluetti = next((b for b in CATALOGO_BLUETTI if b['w'] >= w_req and b['wh_util'] >= wh_req and b['pico'] >= pico_req), None)
        must = next((m for m in CATALOGO_MUST if m['w'] >= w_req and m['wh_util'] >= wh_req and m['pico'] >= pico_req), None)

        st.subheader("3. Equipo Recomendado")
        if bluetti:
            st.success(f"🟢 **BLUETTI:** {bluetti['modelo']} ({bluetti['w']} W continuos | {bluetti['pico']} W pico | {bluetti['wh_util']:.1f} Wh útiles)")
        elif must:
            st.warning(f"🟡 **MUST:** {must['modelo']} ({must['w']} W continuos | {must['pico']} VA pico | {must['wh_util']:.1f} Wh útiles)")
        else:
            st.error("🔴 Se requiere un sistema industrial superior al catálogo comercial estándar.")