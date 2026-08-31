import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculador MUST & BLUETTI", page_icon="⚡", layout="centered")

st.title("⚡ Calculador de Respaldo MUST & BLUETTI")
st.caption("Dimensionamiento de potencia (W) y energía (Wh) con márgenes de seguridad.")

# Base de Equipos con potencias actualizadas
EQUIPOS_BASE = {
    'Router / módem': {'w': 17, 'arr': 1.0},
    'Bombillo LED 18W': {'w': 18, 'arr': 1.0},
    'Televisor LED 32"': {'w': 45, 'arr': 1.2},
    'Televisor LED 40" / 43"': {'w': 65, 'arr': 1.2},
    'Televisor LED 50"': {'w': 90, 'arr': 1.2},
    'Televisor LED 55"': {'w': 120, 'arr': 1.2},
    'Televisor LED 65"': {'w': 160, 'arr': 1.2},
    'Laptop': {'w': 65, 'arr': 1.0},
    'Ventilador de pedestal': {'w': 80, 'arr': 2.0},
    'Nevera / Congelador': {'w': 200, 'arr': 3.0},
    'Bomba de agua 1/2 HP': {'w': 750, 'arr': 3.0},
    'Aire Acond. 9.000 BTU Inverter': {'w': 900, 'arr': 1.5},
    'Otro (Manual)': {'w': 0, 'arr': 1.0}
}

# Catálogo BLUETTI (Factor útil: 85%)
CATALOGO_BLUETTI = [
    {"modelo": "AC2P", "w": 300, "pico": 600, "wh_nom": 230.4, "wh_util": 195.84},
    {"modelo": "Premium 30 V2", "w": 600, "pico": 1500, "wh_nom": 320.0, "wh_util": 272.00},
    {"modelo": "AC50P", "w": 700, "pico": 1200, "wh_nom": 504.0, "wh_util": 428.40},
    {"modelo": "AC70P", "w": 1000, "pico": 2000, "wh_nom": 864.0, "wh_util": 734.40},
    {"modelo": "Premium 100 V2", "w": 2000, "pico": 3600, "wh_nom": 1024.0, "wh_util": 870.40},
    {"modelo": "Premium 200 V2", "w": 2700, "pico": 3900, "wh_nom": 2073.6, "wh_util": 1762.56},
    {"modelo": "Apex 300", "w": 3840, "pico": 3840, "wh_nom": 2764.8, "wh_util": 2350.08},
]

# Catálogo MUST (Eficiencia 90%, DoD 80%)
CATALOGO_MUST = [
    {"modelo": "EP30-3024 LV2 + batería 24V 100Ah", "w": 3000, "pico": 9000, "wh_nom": 2560, "wh_util": 1843.2},
    {"modelo": "EP30-3024 LV2 + 2x batería 24V 100Ah", "w": 3000, "pico": 9000, "wh_nom": 5120, "wh_util": 3686.4},
    {"modelo": "PV33-6048 TLV + LP16-48100", "w": 6000, "pico": 18000, "wh_nom": 5120, "wh_util": 3686.4},
    {"modelo": "PV33-6048 TLV + LP16-48200", "w": 6000, "pico": 18000, "wh_nom": 10240, "wh_util": 7372.8},
    {"modelo": "PV39-12048 TLV + LP16-48200", "w": 12000, "pico": 36000, "wh_nom": 10240, "wh_util": 7372.8},
    {"modelo": "PV39-12048 TLV + 2x LP16-48200", "w": 12000, "pico": 36000, "wh_nom": 20480, "wh_util": 14745.6},
]

# Configuración de márgenes en la barra lateral
st.sidebar.header("Parámetros de Diseño")
margen_p = st.sidebar.slider("Margen de Potencia (%)", 0, 50, 20) / 100.0
margen_e = st.sidebar.slider("Margen de Energía (%)", 0, 50, 15) / 100.0

st.subheader("1. Selección de Cargas")

if 'cargas' not in st.session_state:
    st.session_state.cargas = [
        {"equipo": "Nevera / Congelador", "cant": 1, "w": 200, "arr": 3.0, "horas": 4.0, "ciclo": 0.5},
        {"equipo": "Router / módem", "cant": 1, "w": 17, "arr": 1.0, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Televisor LED 50\"", "cant": 1, "w": 90, "arr": 1.2, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Bombillo LED 18W", "cant": 6, "w": 18, "arr": 1.0, "horas": 4.0, "ciclo": 1.0},
    ]

# Formulario para agregar cargas
with st.form("add_form"):
    c1, c2, c3 = st.columns([2, 1, 1])
    eq_sel = c1.selectbox("Equipo", list(EQUIPOS_BASE.keys()))
    cant_in = c2.number_input("Cantidad", min_value=1, value=1)
    horas_in = c3.number_input("Horas uso", min_value=0.5, value=4.0, step=0.5)
    
    submitted = st.form_submit_button("➕ Agregar Equipo")
    if submitted:
        w_default = EQUIPOS_BASE[eq_sel]['w']
        arr_default = EQUIPOS_BASE[eq_sel]['arr']
        st.session_state.cargas.append({
            "equipo": eq_sel, "cant": cant_in, "w": w_default, "arr": arr_default, "horas": horas_in, "ciclo": 1.0
        })

# Tabla interactiva de cargas agregadas
if st.session_state.cargas:
    df_cargas = pd.DataFrame(st.session_state.cargas)
    df_cargas['W_Total'] = df_cargas['cant'] * df_cargas['w']
    df_cargas['Wh_Total'] = df_cargas['W_Total'] * df_cargas['horas'] * df_cargas['ciclo']
    df_cargas['Extra_Arranque'] = df_cargas['W_Total'] * (df_cargas['arr'] - 1.0).clip(lower=0)

    st.dataframe(df_cargas[['equipo', 'cant', 'w', 'W_Total', 'horas', 'Wh_Total']], use_container_width=True)

    if st.button("🗑️ Limpiar lista de cargas"):
        st.session_state.cargas = []
        st.rerun()

    # Cálculos globales
    w_continuos = df_cargas['W_Total'].sum()
    peor_arranque = df_cargas['Extra_Arranque'].max() if not df_cargas.empty else 0
    wh_totales = df_cargas['Wh_Total'].sum()

    w_requeridos = w_continuos * (1 + margen_p)
    wh_requeridos = wh_totales * (1 + margen_e)
    pico_requerido = (w_continuos + peor_arranque) * (1 + margen_p)

    st.subheader("2. Resumen del Dimensionamiento")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Potencia Continuas (+20%)", f"{w_requeridos:.1f} W")
    col_b.metric("Energía Requerida (+15%)", f"{wh_requeridos:.1f} Wh")
    col_c.metric("Pico Estimado", f"{pico_requerido:.1f} W")

    # Selección de equipos candidatos
    bluetti_cand = next((b for b in CATALOGO_BLUETTI if b['w'] >= w_requeridos and b['wh_util'] >= wh_requeridos), None)
    must_cand = next((m for m in CATALOGO_MUST if m['w'] >= w_requeridos and m['wh_util'] >= wh_requeridos), None)

    st.subheader("3. Solución Recomendada")
    if bluetti_cand:
        st.success(f"🟢 **BLUETTI Recomendado:** {bluetti_cand['modelo']}")
        st.write(f"- Potencia Continua: {bluetti_cand['w']} W | Energía Útil: {bluetti_cand['wh_util']:.1f} Wh")
    elif must_cand:
        st.warning(f"🟡 **MUST Recomendado:** {must_cand['modelo']}")
        st.write(f"- Potencia Nominal: {must_cand['w']} W | Energía Útil: {must_cand['wh_util']:.1f} Wh")
    else:
        st.error("🔴 Las cargas superan el catálogo comercial disponible.")