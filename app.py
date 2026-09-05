import streamlit as st
import pandas as pd
import base64
import os
import urllib.parse
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="Calculador MUST & BLUETTI", page_icon="⚡", layout="centered")

# --- FUNCIONES AUXILIARES PARA ARCHIVOS E IMÁGENES ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

IMAGEN_CABECERA = "logo_prodimic.png"
IMAGEN_FONDO = "fondo_agua.png"

bg_b64 = get_base64_image(IMAGEN_FONDO)
bg_style = f"data:image/png;base64,{bg_b64}" if bg_b64 else IMAGEN_FONDO

# --- ESTILOS CSS ---
st.markdown(f'''
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
    background-size: 65% auto;
    opacity: 0.80;
    pointer-events: none;
    z-index: 0;
}}

div[data-testid="stImage"] {{
    margin-bottom: -2.8rem !important;
}}

h1 {{
    margin-top: -2.0rem !important;
    padding-top: 0rem !important;
    margin-bottom: 0.2rem !important;
}}

@media (max-width: 640px) {{
    .block-container {{
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 0.5rem !important;
    }}
    h1 {{
        font-size: 1.5rem !important;
    }}
}}
</style>
''', unsafe_allow_html=True)

# --- CABECERA EN PANTALLA ---
if os.path.exists(IMAGEN_CABECERA):
    st.image(IMAGEN_CABECERA, use_container_width=True)

st.title("⚡ Calculador de Respaldo MUST & BLUETTI")
st.caption("Distribuidora Prodimic — Dimensionamiento directo de potencia, energía y picos de arranque.")

# Base de equipos completa
EQUIPOS_BASE = {
    'Bombillo LED 4W': {'w': 4, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Bombillo LED 9W': {'w': 9, 'arr': 1.0, 'v': 120, 'btu': 0},
    'Bombillo LED 12W': {'w': 12, 'arr': 1.0, 'v': 120, 'btu': 0},
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
    
    # Modelos 12.000 BTU (120V y 220V)
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
    'Otro / Personalizado': {'w': 0, 'arr': 1.0, 'v': 120, 'btu': 0}
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

CATALOGO_MUST.sort(key=lambda x: (x['w'], x['wh_util']))

# --- FUNCIÓN PARA GENERAR IMAGEN CON OPACIDAD DEL 30% PARA EL PDF ---
def obtener_marca_agua_pdf(opacidad=0.30):
    ruta = IMAGEN_FONDO if os.path.exists(IMAGEN_FONDO) else (IMAGEN_CABECERA if os.path.exists(IMAGEN_CABECERA) else None)
    if not ruta:
        return None
    try:
        img = Image.open(ruta).convert("RGBA")
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        r, g, b, a = img.split()
        a = a.point(lambda p: int(p * opacidad))
        img.putalpha(a)
        blended = Image.alpha_composite(white_bg, img).convert("RGB")
        temp_path = "temp_marca_agua_pdf.png"
        blended.save(temp_path, "PNG")
        return temp_path
    except Exception:
        return None

# --- FUNCIÓN GENERADORA DE PDF CON MARCA DE AGUA CENTRADA ---
def generar_pdf_propuesta(cargas, w_req, wh_req, pico_req, bluetti_rec, must_rec):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Marca de agua centrada en el documento con 30% de opacidad
    wm_file = obtener_marca_agua_pdf(opacidad=0.30)
    if wm_file and os.path.exists(wm_file):
        pdf.image(wm_file, x=35, y=75, w=140)

    pdf.set_y(15)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "PROPUESTA DE RESPALDO ELECTRICO", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "Distribuidora Prodimic C.A. - Asesoria tecnica", ln=True, align="C")
    pdf.ln(10)

    # 1. Requerimientos Calculados
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "1. Resumen de Requerimientos del Cliente", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 6, f"Potencia Continua: {w_req:.0f} W", border=1)
    pdf.cell(60, 6, f"Energia Requerida: {wh_req:.0f} Wh", border=1)
    pdf.cell(60, 6, f"Pico de Arranque: {pico_req:.0f} VA", border=1, ln=True)
    pdf.ln(6)

    # 2. Detalle de Cargas
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. Detalle de Equipos a Respaldar", ln=True)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(85, 6, "Equipo", border=1)
    pdf.cell(20, 6, "Cant.", border=1, align="C")
    pdf.cell(25, 6, "Pot. (W)", border=1, align="C")
    pdf.cell(25, 6, "Horas", border=1, align="C")
    pdf.cell(25, 6, "Energia (Wh)", border=1, align="C", ln=True)

    pdf.set_font("Helvetica", "", 9)
    for c in cargas:
        w_tot = c['cant'] * c['w']
        wh_tot = w_tot * c['horas'] * c['ciclo']
        nombre_clean = c['equipo'].encode('latin-1', 'replace').decode('latin-1').replace('?', '')
        pdf.cell(85, 6, nombre_clean[:45], border=1)
        pdf.cell(20, 6, str(c['cant']), border=1, align="C")
        pdf.cell(25, 6, f"{w_tot:.0f}", border=1, align="C")
        pdf.cell(25, 6, f"{c['horas']:.1f}", border=1, align="C")
        pdf.cell(25, 6, f"{wh_tot:.0f}", border=1, align="C", ln=True)
    
    pdf.ln(8)

    # 3. Equipos Recomendados
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "3. Sistemas de Respaldo Recomendados", ln=True)
    pdf.set_font("Helvetica", "", 10)

    if bluetti_rec:
        pct_w = min(w_req / bluetti_rec['w'], 1.0) * 100
        pct_wh = min(wh_req / bluetti_rec['wh_util'], 1.0) * 100
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, f"Opcion Estacion Portatil BLUETTI: {bluetti_rec['modelo']}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"- Capacidad: {bluetti_rec['w']}W Continuos | {bluetti_rec['wh_util']:.0f}Wh Utiles | Uso Potencia: {pct_w:.1f}% | Uso Energia: {pct_wh:.1f}%", ln=True)
        pdf.ln(3)

    if must_rec:
        pct_w = min(w_req / must_rec['w'], 1.0) * 100
        pct_wh = min(wh_req / must_rec['wh_util'], 1.0) * 100
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, f"Opcion Sistema Estacionario MUST: {must_rec['modelo']}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"- Capacidad: {must_rec['w']}W Continuos | {must_rec['wh_util']:.0f}Wh Utiles | Uso Potencia: {pct_w:.1f}% | Uso Energia: {pct_wh:.1f}%", ln=True)

    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, "Distribuidora Prodimic C.A. - Documento generado automaticamente para fines de cotizacion.", align="C")
    
    return bytes(pdf.output())

# --- FUNCIÓN PARA MOSTRAR FICHAS TÉCNICAS ---
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

# --- RENDERIZADO DE PROPUESTAS ---
def render_propuesta(rec, w_req, wh_req, tipo_marca, key_prefix):
    pct_w = min(w_req / rec['w'], 1.0)
    pct_wh = min(wh_req / rec['wh_util'], 1.0)
    
    if tipo_marca == "BLUETTI":
        st.success(f"🟢 **BLUETTI:** {rec['modelo']} ({rec['w']} W continuos | {rec['pico']} W pico | {rec['wh_util']:.1f} Wh útiles)")
    else:
        st.warning(f"🟡 **MUST (DoD 90%):** {rec['modelo']} ({rec['w']} W continuos | {rec['pico']} VA pico | {rec['wh_util']:.1f} Wh útiles)")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.caption(f"⚡ **Potencia:** {w_req:.0f} W / {rec['w']} W ({pct_w*100:.1f}%)")
        st.progress(pct_w)
    with col_b2:
        st.caption(f"🔋 **Energía:** {wh_req:.0f} Wh / {rec['wh_util']:.1f} Wh ({pct_wh*100:.1f}%)")
        st.progress(pct_wh)

    desplegar_fichas_tecnicas(rec['fichas'], key_prefix)
    st.write("---")

st.subheader("1. Selección de Cargas")

if 'cargas' not in st.session_state:
    st.session_state.cargas = []

with st.container(border=True):
    eq_sel = st.selectbox("Seleccione Equipo", list(EQUIPOS_BASE.keys()), key="eq_select")
    is_custom = (eq_sel == 'Otro / Personalizado')
    
    if is_custom:
        col_c1, col_c2 = st.columns(2)
        w_custom = col_c1.number_input("Potencia en Vatios (W)", min_value=1, value=100, step=10, key="w_custom_in")
        arr_custom = col_c2.number_input("Factor de arranque (1.0 normal, 3.0 neveras)", min_value=1.0, value=1.0, step=0.5, key="arr_custom_in")

    col_f1, col_f2 = st.columns(2)
    cant_in = col_f1.number_input("Cantidad", min_value=1, value=1, key="cant_in")
    horas_in = col_f2.number_input("Horas uso", min_value=0.5, value=4.0, step=0.5, key="horas_in")
    
    if st.button("➕ Agregar a la Lista", use_container_width=True, type="primary"):
        eq_data = EQUIPOS_BASE[eq_sel]
        real_w = w_custom if is_custom else eq_data['w']
        real_arr = arr_custom if is_custom else eq_data['arr']
        nombre_equipo = f"Carga Personalizada ({real_w}W)" if is_custom else eq_sel

        st.session_state.cargas.append({
            "equipo": nombre_equipo,
            "cant": cant_in,
            "w": real_w,
            "arr": real_arr,
            "v": eq_data['v'],
            "btu": eq_data['btu'],
            "horas": horas_in,
            "ciclo": 1.0
        })
        st.rerun()

if st.session_state.cargas:
    st.write("### Lista de Cargas Seleccionadas")
    idx_eliminar = None

    for idx, item in enumerate(st.session_state.cargas):
        with st.container(border=True):
            col_item1, col_item2, col_item3, col_item4 = st.columns([0.40, 0.22, 0.22, 0.16])
            
            w_tot_item = item['cant'] * item['w']
            wh_tot_item = w_tot_item * item['horas'] * item['ciclo']
            
            with col_item1:
                st.markdown(f"**{item['equipo']}**")
                st.caption(f"Subtotal: **{w_tot_item:.0f} W** | **{wh_tot_item:.0f} Wh**")
            
            with col_item2:
                item['cant'] = st.number_input("Cant.", min_value=1, value=int(item['cant']), key=f"edit_cant_{idx}")
            
            with col_item3:
                item['horas'] = st.number_input("Horas", min_value=0.5, value=float(item['horas']), step=0.5, key=f"edit_horas_{idx}")
            
            with col_item4:
                st.write("")
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

        bluetti_rec = next(
            (b for b in cat_bluetti_eval if b['w'] >= w_req and b['wh_util'] >= wh_req and b['pico'] >= pico_req), 
            None
        )

        MIN_UTIL_W = 0.25
        candidatos_must = [
            m for m in cat_must_eval 
            if m['w'] >= w_req and m['wh_util'] >= wh_req and m['pico'] >= pico_req
            and (w_req / m['w']) >= MIN_UTIL_W
        ]

        if not candidatos_must and not bluetti_rec:
            candidatos_must = [
                m for m in cat_must_eval 
                if m['w'] >= w_req and m['wh_util'] >= wh_req and m['pico'] >= pico_req
            ]

        must_rec = candidatos_must[0] if candidatos_must else None

        if w_req <= 1800 and bluetti_rec and must_rec:
            if (w_req / must_rec['w']) < 0.35:
                must_rec = None

        if not bluetti_rec and not must_rec:
            st.error("🔴 Se requiere un sistema industrial superior al catálogo comercial estándar.")
        else:
            if bluetti_rec:
                render_propuesta(bluetti_rec, w_req, wh_req, "BLUETTI", "bluetti")

            if must_rec:
                render_propuesta(must_rec, w_req, wh_req, "MUST", "must_optima")

            # --- SECCIÓN 4: EXPORTACIÓN Y COMPARTIR ---
            st.subheader("4. Exportar y Compartir Propuesta")
            
            col_exp1, col_exp2 = st.columns(2)

            # Botón 1: Descarga de PDF
            with col_exp1:
                pdf_bytes = generar_pdf_propuesta(st.session_state.cargas, w_req, wh_req, pico_req, bluetti_rec, must_rec)
                st.download_button(
                    label="📄 Descargar Propuesta en PDF",
                    data=pdf_bytes,
                    file_name="Propuesta_Respaldo_Prodimic.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )

            # Botón 2: Enlace a WhatsApp
            with col_exp2:
                msg_wa = f"⚡ *Cotización de Respaldo Eléctrico - Prodimic*\n\n"
                msg_wa += f"📊 *Requerimientos:* {w_req:.0f}W Potencia | {wh_req:.0f}Wh Energía | {pico_req:.0f}VA Pico\n\n"
                msg_wa += f"📋 *Cargas principales:*\n"
                for item in st.session_state.cargas:
                    msg_wa += f"• {item['cant']}x {item['equipo']} ({item['horas']}h uso)\n"
                
                msg_wa += "\n✅ *Equipos Recomendados:*\n"
                if bluetti_rec:
                    msg_wa += f"• BLUETTI: {bluetti_rec['modelo']}\n"
                if must_rec:
                    msg_wa += f"• MUST: {must_rec['modelo']}\n"
                
                wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg_wa)}"
                st.link_button("📱 Compartir por WhatsApp", wa_url, use_container_width=True)

else:
    st.info("💡 Selecciona y agrega equipos arriba para calcular la recomendación de respaldo.")