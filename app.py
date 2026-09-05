import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(page_title="Calculador MUST & BLUETTI", page_icon="⚡", layout="centered")

# --- INYECCIÓN DE CSS PARA MARCA DE AGUA DE PRODIMIC AL 80% DE OPACIDAD ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64_image("logo_prodimic.png")
bg_style = f"data:image/png;base64,{logo_b64}" if logo_b64 else "logo_prodimic.png"

st.markdown(f'''
<style>
/* Fondo en marca de agua (Opacidad al 80%) */
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
    background-size: 65% auto;
    opacity: 0.80;
    pointer-events: none;
    z-index: 0;
}}

/* Responsividad para móviles */
@media (max-width: 640px) {{
    .block-container {{
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 1rem !important;
    }}
    h1 {{
        font-size: 1.5rem !important;
    }}
}}
</style>
''', unsafe_allow_html=True)

# --- CABECERA CON LOGO DE PRODIMIC (Ancho total del contenedor) ---
if os.path.exists("logo_prodimic.png"):
    st.image("logo_prodimic.png", use_container_width=True)

st.title("⚡Selección MUST & BLUETTI⚡")
st.caption("Distribuidora Prodimic — Dimensionamiento directo de potencia, energía y picos de arranque.")

# Base de equipos completa
EQUIPOS_BASE = {
    'Bombillo LED 18W': {'w': 18, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Router / módem': {'w': 17, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Cargador de teléfono': {'w': 15, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Monitor': {'w': 30, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Impresora de tinta': {'w': 30, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Sistema CCTV': {'w': 60, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Laptop': {'w': 65, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Ventilador': {'w': 80, 'arr': 2.0, 'v': 120, 'btu': 0},
    'Televisor LED 32"': {'w': 45, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED 40" / 43"': {'w': 65, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED 50"': {'w': 90, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED 55"': {'w': 120, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED 65"': {'w': 160, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED 75"': {'w': 200, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Televisor LED (genérico)': {'w': 100, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Nevera': {'w': 200, 'arr': 3.0, 'v': 120, 'btu': 0},
    'Computadora de escritorio': {'w': 250, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Congelador': {'w': 250, 'arr': 3.0, 'v': 120, 'btu': 0},
    'Licuadora': {'w': 500, 'arr': 2.0, 'v': 120, 'btu': 0},
    'Impresora láser': {'w': 600, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Bomba de agua 1/2 HP': {'w': 750, 'arr': 3.0, 'v': 120, 'btu': 0},
    'Cafetera eléctrica': {'w': 1000, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Microondas': {'w': 1200, 'arr': 1.3, 'v': 120, 'btu': 0},
    'Secador de cabello': {'w': 1500, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Herramienta eléctrica': {'w': 1500, 'arr': 2.5, 'v': 120, 'btu': 0},
    
    # Acondicionadores de Aire <= 12.000 BTU
    'Aire acondicionado 5.000 BTU — convencional': {'w': 500, 'arr': 3.0, 'v': 120, 'btu': 5000},
    'Aire acondicionado 5.000 BTU — inverter': {'w': 500, 'arr': 1.5, 'v': 120, 'btu': 5000},
    'Aire acondicionado 6.000 BTU — convencional': {'w': 600, 'arr': 3.0, 'v': 120, 'btu': 6000},
    'Aire acondicionado 6.000 BTU — inverter': {'w': 600, 'arr': 1.5, 'v': 120, 'btu': 6000},
    'Aire acondicionado 8.000 BTU — convencional': {'w': 800, 'arr': 3.0, 'v': 120, 'btu': 8000},
    'Aire acondicionado 8.000 BTU — inverter': {'w': 800, 'arr': 1.5, 'v': 120, 'btu': 8000},
    'Aire acondicionado 9.000 BTU — convencional': {'w': 900, 'arr': 3.0, 'v': 120, 'btu': 9000},
    'Aire acondicionado 9.000 BTU — inverter': {'w': 900, 'arr': 1.5, 'v': 120, 'btu': 9000},
    'Aire acondicionado 10.000 BTU — convencional': {'w': 1000, 'arr': 3.0, 'v': 120, 'btu': 10000},
    'Aire acondicionado 10.000 BTU — inverter': {'w': 1000, 'arr': 1.5, 'v': 120, 'btu': 10000},
    
    # Modelos 12.000 BTU desglosados por voltaje (120V y 220V)
    'Aire acondicionado 12.000 BTU (1 ton) 120V — convencional': {'w': 1200, 'arr': 3.0, 'v': 120, 'btu': 12000},
    'Aire acondicionado 12.000 BTU (1 ton) 120V — inverter': {'w': 1200, 'arr': 1.5, 'v': 120, 'btu': 12000},
    'Aire acondicionado 12.000 BTU (1 ton) 220V — convencional': {'w': 1200, 'arr': 3.0, 'v': 220, 'btu': 12000},
    'Aire acondicionado 12.000 BTU (1 ton) 220V — inverter': {'w': 1200, 'arr': 1.5, 'v': 220, 'btu': 12000},
    
    # Acondicionadores de Aire > 12.000 BTU (220V)
    'Aire acondicionado 15.000 BTU (1,25 ton) — convencional': {'w': 1500, 'arr': 3.0, 'v': 220, 'btu': 15000},
    'Aire acondicionado 15.000 BTU (1,25 ton) — inverter': {'w': 1500, 'arr': 1.5, 'v': 220, 'btu': 15000},
    'Aire acondicionado 18.000 BTU (1,5 ton) — convencional': {'w': 1800, 'arr': 3.0, 'v': 220, 'btu': 18000},
    'Aire acondicionado 18.000 BTU (1,5 ton) — inverter': {'w': 1800, 'arr': 1.5, 'v': 220, 'btu': 18000},
    'Aire acondicionado 24.000 BTU (2 ton) — convencional': {'w': 2400, 'arr': 3.0, 'v': 220, 'btu': 24000},
    'Aire acondicionado 24.000 BTU (2 ton) — inverter': {'w': 2400, 'arr': 1.5, 'v': 220, 'btu': 24000},
    'Aire acondicionado 30.000 BTU (2,5 ton) — convencional': {'w': 3000, 'arr': 3.0, 'v': 220, 'btu': 30000},
    'Aire acondicionado 30.000 BTU (2,5 ton) — inverter': {'w': 3000, 'arr': 1.5, 'v': 220, 'btu': 30000},
    'Aire acondicionado 36.000 BTU (3 ton) — convencional': {'w': 3600, 'arr': 3.0, 'v': 220, 'btu': 36000},
    'Aire acondicionado 36.000 BTU (3 ton) — inverter': {'w': 3600, 'arr': 1.5, 'v': 220, 'btu': 36000},
    'Aire acondicionado 42.000 BTU (3,5 ton) — convencional': {'w': 4200, 'arr': 3.0, 'v': 220, 'btu': 42000},
    'Aire acondicionado 42.000 BTU (3,5 ton) — inverter': {'w': 4200, 'arr': 1.5, 'v': 220, 'btu': 42000},
    'Aire acondicionado 48.000 BTU (4 ton) — convencional': {'w': 4800, 'arr': 3.0, 'v': 220, 'btu': 48000},
    'Aire acondicionado 48.000 BTU (4 ton) — inverter': {'w': 4800, 'arr': 1.5, 'v': 220, 'btu': 48000},
    'Aire acondicionado 54.000 BTU (4,5 ton) — convencional': {'w': 5400, 'arr': 3.0, 'v': 220, 'btu': 54000},
    'Aire acondicionado 54.000 BTU (4,5 ton) — inverter': {'w': 5400, 'arr': 1.5, 'v': 220, 'btu': 54000},
    'Aire acondicionado 60.000 BTU (5 ton) — convencional': {'w': 6000, 'arr': 3.0, 'v': 220, 'btu': 60000},
    'Aire acondicionado 60.000 BTU (5 ton) — inverter': {'w': 6000, 'arr': 1.5, 'v': 220, 'btu': 60000},
    'Otro / manual': {'w': 0, 'arr': 1.0, 'v': 120, 'btu': 0}
}

# Catálogo BLUETTI
CATALOGO_BLUETTI = [
    {"modelo": "AC2P", "w": 300, "pico": 300, "wh_util": 195.84, "v220": False, 
     "fichas": [{"nombre": "Estación AC2P", "base": "fichas/bluetti_ac2p"}]},
    {"modelo": "Premium 30 V2", "w": 600, "pico": 600, "wh_util": 272.00, "v220": False, 
     "fichas": [{"nombre": "Estación Premium 30 V2", "base": "fichas/bluetti_premium30"}]},
    {"modelo": "AC50P", "w": 700, "pico": 700, "wh_util": 428.40, "v220": False, 
     "fichas": [{"nombre": "Estación AC50P", "base": "fichas/bluetti_ac50p"}]},
    {"modelo": "AC70P", "w": 1000, "pico": 1000, "wh_util": 734.40, "v220": False, 
     "fichas": [{"nombre": "Estación AC70P", "base": "fichas/bluetti_ac70p"}]},
    {"modelo": "AC180P", "w": 1800, "pico": 1800, "wh_util": 1224.00, "v220": False, 
     "fichas": [{"nombre": "Estación AC180P", "base": "fichas/bluetti_ac180p"}]},
    {"modelo": "Premium 100 V2", "w": 2000, "pico": 2000, "wh_util": 870.40, "v220": False, 
     "fichas": [{"nombre": "Estación Premium 100 V2", "base": "fichas/bluetti_premium100"}]},
    {"modelo": "Premium 200 V2", "w": 2700, "pico": 2700, "wh_util": 1762.56, "v220": False, 
     "fichas": [{"nombre": "Estación Premium 200 V2", "base": "fichas/bluetti_premium200"}]},
    {"modelo": "Apex 300", "w": 3840, "pico": 3840, "wh_util": 2350.08, "v220": True, 
     "fichas": [{"nombre": "Estación Apex 300", "base": "fichas/bluetti_apex300"}]},
    {"modelo": "Apex 300 + B300K", "w": 3840, "pico": 3840, "wh_util": 4700.16, "v220": True, 
     "fichas": [
         {"nombre": "Estación Apex 300", "base": "fichas/bluetti_apex300"},
         {"nombre": "Batería B300K", "base": "fichas/bluetti_b300k"}
     ]},
    {"modelo": "Apex 300 + 2x B300K", "w": 3840, "pico": 3840, "wh_util": 7050.24, "v220": True, 
     "fichas": [
         {"nombre": "Estación Apex 300", "base": "fichas/bluetti_apex300"},
         {"nombre": "Batería B300K", "base": "fichas/bluetti_b300k"}
     ]},
    {"modelo": "Apex 300 + 3x B300K", "w": 3840, "pico": 3840, "wh_util": 9400.32, "v220": True, 
     "fichas": [
         {"nombre": "Estación Apex 300", "base": "fichas/bluetti_apex300"},
         {"nombre": "Batería B300K", "base": "fichas/bluetti_b300k"}
     ]},
    {"modelo": "Apex 300 + 4x B300K", "w": 3840, "pico": 3840, "wh_util": 11750.40, "v220": True, 
     "fichas": [
         {"nombre": "Estación Apex 300", "base": "fichas/bluetti_apex300"},
         {"nombre": "Batería B300K", "base": "fichas/bluetti_b300k"}
     ]},
]

# Catálogo MUST Generado Dinámicamente (DoD al 90%)
CATALOGO_MUST = []

# EP30-3024 LV2 (1 a 5 baterías de 24V 100Ah -> 2400Wh nominal * 0.90 DoD = 2160 Wh útiles por batería)
FOR_MUST_24V_WH_UTIL_PER_BAT = 2400 * 0.90
for n in range(1, 6):
    cant_str = f"{n}x " if n > 1 else ""
    CATALOGO_MUST.append({
        "modelo": f"EP30-3024 LV2 + {cant_str}batería 24V 100Ah",
        "w": 3000,
        "pico": 9000,
        "wh_util": round(FOR_MUST_24V_WH_UTIL_PER_BAT * n, 1),
        "v220": False,
        "bat_type": "24V100",
        "fichas": [
            {"nombre": "Inversor EP30-3024 LV2", "base": "fichas/must_ep30"},
            {"nombre": "Batería 24V 100Ah", "base": "fichas/must_bat_24v100"}
        ]
    })

# PV33-6048 TLV (6000W) con LP16-48100 (1 a 10 baterías -> 5120Wh nominal * 0.90 DoD = 4608 Wh útiles por batería)
FOR_MUST_48100_WH_UTIL_PER_BAT = 5120 * 0.90
for n in range(1, 11):
    cant_str = f"{n}x " if n > 1 else ""
    CATALOGO_MUST.append({
        "modelo": f"PV33-6048 TLV + {cant_str}LP16-48100",
        "w": 6000,
        "pico": 12000,
        "wh_util": round(FOR_MUST_48100_WH_UTIL_PER_BAT * n, 1),
        "v220": True,
        "bat_type": "LP16-48100",
        "fichas": [
            {"nombre": "Inversor PV33-6048 TLV", "base": "fichas/must_pv33"},
            {"nombre": "Batería Serie LP16", "base": "fichas/must_lp16"}
        ]
    })

# PV33-6048 TLV (6000W) con LP16-48200 (1 a 10 baterías -> 10240Wh nominal * 0.90 DoD = 9216 Wh útiles por batería)
FOR_MUST_48200_WH_UTIL_PER_BAT = 10240 * 0.90
for n in range(1, 11):
    cant_str = f"{n}x " if n > 1 else ""
    CATALOGO_MUST.append({
        "modelo": f"PV33-6048 TLV + {cant_str}LP16-48200",
        "w": 6000,
        "pico": 12000,
        "wh_util": round(FOR_MUST_48200_WH_UTIL_PER_BAT * n, 1),
        "v220": True,
        "bat_type": "LP16-48200",
        "fichas": [
            {"nombre": "Inversor PV33-6048 TLV", "base": "fichas/must_pv33"},
            {"nombre": "Batería Serie LP16", "base": "fichas/must_lp16"}
        ]
    })

# PV39-12048 TLV (12000W) con LP16-48100 (1 a 10 baterías -> 4608 Wh útiles por batería)
for n in range(1, 11):
    cant_str = f"{n}x " if n > 1 else ""
    CATALOGO_MUST.append({
        "modelo": f"PV39-12048 TLV + {cant_str}LP16-48100",
        "w": 12000,
        "pico": 36000,
        "wh_util": round(FOR_MUST_48100_WH_UTIL_PER_BAT * n, 1),
        "v220": True,
        "bat_type": "LP16-48100",
        "fichas": [
            {"nombre": "Inversor PV39-12048 TLV", "base": "fichas/must_pv39"},
            {"nombre": "Batería Serie LP16", "base": "fichas/must_lp16"}
        ]
    })

# PV39-12048 TLV (12000W) con LP16-48200 (1 a 10 baterías -> 9216 Wh útiles por batería)
for n in range(1, 11):
    cant_str = f"{n}x " if n > 1 else ""
    CATALOGO_MUST.append({
        "modelo": f"PV39-12048 TLV + {cant_str}LP16-48200",
        "w": 12000,
        "pico": 36000,
        "wh_util": round(FOR_MUST_48200_WH_UTIL_PER_BAT * n, 1),
        "v220": True,
        "bat_type": "LP16-48200",
        "fichas": [
            {"nombre": "Inversor PV39-12048 TLV", "base": "fichas/must_pv39"},
            {"nombre": "Batería Serie LP16", "base": "fichas/must_lp16"}
        ]
    })

# Ordenamiento por potencia y capacidad de energía ascendente
CATALOGO_MUST.sort(key=lambda x: (x['w'], x['wh_util']))

# --- FUNCIÓN PARA MOSTRAR FICHAS TÉCNICAS Y BOTONES DE DESCARGA ---
def desplegar_fichas_tecnicas(lista_fichas, key_prefix):
    extensiones = [".jpg", ".png", ".jpeg", ".pdf"]
    
    for idx, item in enumerate(lista_fichas):
        nombre_comp = item["nombre"]
        base_path = item["base"]
        archivo_encontrado = None
        ext_encontrada = None

        for ext in extensiones:
            path_test = f"{base_path}{ext}"
            if os.path.exists(path_test):
                archivo_encontrado = path_test
                ext_encontrada = ext
                break

        if archivo_encontrado:
            if ext_encontrada in [".jpg", ".png", ".jpeg"]:
                with st.expander(f"👁️ Ficha Técnica: {nombre_comp}"):
                    st.image(archivo_encontrado, use_container_width=True)
                    with open(archivo_encontrado, "rb") as file_bytes:
                        st.download_button(
                            label=f"💾 Descargar Ficha ({nombre_comp})",
                            data=file_bytes,
                            file_name=os.path.basename(archivo_encontrado),
                            mime=f"image/{ext_encontrada.replace('.', '')}",
                            use_container_width=True,
                            key=f"{key_prefix}_{idx}_dl_img"
                        )
            elif ext_encontrada == ".pdf":
                with open(archivo_encontrado, "rb") as file_bytes:
                    st.download_button(
                        label=f"📄 Descargar Ficha PDF ({nombre_comp})",
                        data=file_bytes,
                        file_name=os.path.basename(archivo_encontrado),
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"{key_prefix}_{idx}_dl_pdf"
                    )
        else:
            st.caption(f"ℹ️ Ficha pendiente por cargar en GitHub: `{base_path}.jpg`")

# --- RENDERIZADO COMPLETO POR CADA PROPUESTA (CARD + BARRAS % + FICHAS INMEDIATAS) ---
def render_propuesta(rec, w_req, wh_req, tipo_marca, key_prefix):
    pct_w = min(w_req / rec['w'], 1.0)
    pct_wh = min(wh_req / rec['wh_util'], 1.0)
    
    if tipo_marca == "BLUETTI":
        st.success(f"🟢 **BLUETTI:** {rec['modelo']} ({rec['w']} W continuos | {rec['pico']} W pico | {rec['wh_util']:.1f} Wh útiles)")
    else:
        st.warning(f"🟡 **MUST (DoD 90%):** {rec['modelo']} ({rec['w']} W continuos | {rec['pico']} VA pico | {rec['wh_util']:.1f} Wh útiles)")
    
    # Barras de porcentaje de potencia y energía
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.caption(f"⚡ **Potencia:** {w_req:.0f} W / {rec['w']} W ({pct_w*100:.1f}%)")
        st.progress(pct_w)
    with col_b2:
        st.caption(f"🔋 **Energía:** {wh_req:.0f} Wh / {rec['wh_util']:.1f} Wh ({pct_wh*100:.1f}%)")
        st.progress(pct_wh)

    # Enlaces de descarga y visualización de fichas inmediatamente debajo
    desplegar_fichas_tecnicas(rec['fichas'], key_prefix)
    st.write("---")

st.subheader("1. Selección de Cargas")

if 'cargas' not in st.session_state:
    st.session_state.cargas = [
        {"equipo": "Nevera", "cant": 1, "w": 200, "arr": 3.0, "v": 120, "btu": 0, "horas": 4.0, "ciclo": 0.5},
        {"equipo": "Router / módem", "cant": 1, "w": 17, "arr": 1.0, "v": 120, "btu": 0, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Televisor LED 50\"", "cant": 1, "w": 90, "arr": 1.0, "v": 120, "btu": 0, "horas": 4.0, "ciclo": 1.0},
        {"equipo": "Bombillo LED 18W", "cant": 6, "w": 18, "arr": 1.0, "v": 120, "btu": 0, "horas": 4.0, "ciclo": 1.0},
    ]

with st.form("add_form"):
    eq_sel = st.selectbox("Seleccione Equipo", list(EQUIPOS_BASE.keys()))
    col_f1, col_f2 = st.columns(2)
    cant_in = col_f1.number_input("Cantidad", min_value=1, value=1)
    horas_in = col_f2.number_input("Horas uso", min_value=0.5, value=4.0, step=0.5)
    
    submitted = st.form_submit_button("➕ Agregar a la Lista", use_container_width=True)
    if submitted:
        eq_data = EQUIPOS_BASE[eq_sel]
        st.session_state.cargas.append({
            "equipo": eq_sel,
            "cant": cant_in,
            "w": eq_data['w'],
            "arr": eq_data['arr'],
            "v": eq_data['v'],
            "btu": eq_data['btu'],
            "horas": horas_in,
            "ciclo": 1.0
        })

if st.session_state.cargas:
    st.write("### Lista de Cargas Seleccionadas")
    idx_eliminar = None

    for idx, item in enumerate(st.session_state.cargas):
        w_tot = item['cant'] * item['w']
        wh_tot = w_tot * item['horas'] * item['ciclo']
        
        with st.container(border=True):
            c_card1, c_card2 = st.columns([0.82, 0.18])
            with c_card1:
                st.markdown(f"**{item['equipo']}**")
                st.caption(f"Cantidad: **{item['cant']}** | Potencia: **{w_tot} W**")
                st.caption(f"Uso: **{item['horas']} h** | Energía: **{wh_tot:.0f} Wh**")
            with c_card2:
                if st.button("🗑️", key=f"del_{idx}"):
                    idx_eliminar = idx

    if idx_eliminar is not None:
        st.session_state.cargas.pop(idx_eliminar)
        st.rerun()

    st.write("---")
    if st.button("🗑️ Limpiar Toda la Lista", use_container_width=True):
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

        requiere_alta_capacidad = any(item.get('v') == 220 or item.get('btu', 0) > 12000 for item in st.session_state.cargas)

        st.subheader("2. Requerimientos Netos")
        col1, col2, col3 = st.columns(3)
        col1.metric("Potencia", f"{w_req:.0f} W")
        col2.metric("Energía", f"{wh_req:.0f} Wh")
        col3.metric("Pico", f"{pico_req:.0f} VA")

        if requiere_alta_capacidad:
            st.info("⚡ **Filtro 220V / Carga Comercial:** Búsqueda limitada a Apex 300, PV33 y PV39.")
            cat_bluetti_eval = [b for b in CATALOGO_BLUETTI if b['v220']]
            cat_must_eval = [m for m in CATALOGO_MUST if m['v220']]
        else:
            cat_bluetti_eval = CATALOGO_BLUETTI
            cat_must_eval = CATALOGO_MUST

        st.subheader("3. Equipos Recomendados")

        # --- EVALUACIÓN DE BLUETTI ---
        bluetti_rec = next(
            (b for b in cat_bluetti_eval if b['w'] >= w_req and b['wh_util'] >= wh_req and b['pico'] >= pico_req), 
            None
        )

        # --- EVALUACIÓN Y FILTRADO INTELIGENTE DE MUST ---
        MIN_UTIL_W = 0.25  # Requerir al menos 25% de uso del inversor MUST

        # Buscar candidatos MUST que cumplan cargas Y tengan un uso de potencia razonable (>= 25%)
        candidatos_must = [
            m for m in cat_must_eval 
            if m['w'] >= w_req and m['wh_util'] >= wh_req and m['pico'] >= pico_req
            and (w_req / m['w']) >= MIN_UTIL_W
        ]

        # Si no hay candidato con >= 25% pero tampoco existe BLUETTI, relajamos la restricción
        if not candidatos_must and not bluetti_rec:
            candidatos_must = [
                m for m in cat_must_eval 
                if m['w'] >= w_req and m['wh_util'] >= wh_req and m['pico'] >= pico_req
            ]

        # Seleccionar ÚNICAMENTE la combinación MUST más ajustada
        must_rec = candidatos_must[0] if candidatos_must else None

        # --- REGLA EXCLUSIVA DE CARGAS LIVIANAS (< 1800W) ---
        # Si la demanda es pequeña y BLUETTI satisface la carga, ocultar MUST si está muy sobredimensionado (< 35% de uso)
        if w_req <= 1800 and bluetti_rec and must_rec:
            if (w_req / must_rec['w']) < 0.35:
                must_rec = None

        # --- MOSTRAR RESULTADOS RECOMENDADOS ---
        if not bluetti_rec and not must_rec:
            st.error("🔴 Se requiere un sistema industrial superior al catálogo comercial estándar.")
        else:
            if bluetti_rec:
                render_propuesta(bluetti_rec, w_req, wh_req, "BLUETTI", "bluetti")

            if must_rec:
                render_propuesta(must_rec, w_req, wh_req, "MUST", "must_optima")