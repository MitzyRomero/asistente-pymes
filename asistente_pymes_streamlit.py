
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from fpdf import FPDF
import os
from datetime import datetime

# Entrenamiento del modelo
X_train = pd.DataFrame({
    "antiguedad": [0, 1, 2, 3, 2, 1, 0, 3],
    "empleados": [1, 2, 3, 4, 2, 1, 1, 3],
    "ingresos": [0, 1, 2, 3, 1, 1, 0, 2],
    "deuda": [0, 1, 2, 3, 1, 1, 0, 2],
    "clientes": [0, 1, 2, 3, 1, 0, 0, 2],
    "software": [0, 1, 1, 1, 0, 0, 0, 1],
    "digitalizacion": [0, 1, 2, 3, 1, 0, 0, 2],
    "estrategia": [0, 1, 2, 2, 1, 0, 0, 2],
    "competencia_sector": [80, 120, 95, 50, 60, 120, 95, 60],
    "desempleo": [4.8, 5.2, 6.1, 4.3, 5.5, 5.2, 6.1, 5.5],
    "innovacion": [2, 3, 3, 2, 1, 3, 3, 1]
})
y_train = [2, 1, 0, 0, 1, 2, 2, 0]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

niveles = {0: "Bajo", 1: "Medio", 2: "Alto"}

def obtener_recomendacion_detallada(nivel):
    if nivel == "Bajo":
       return (
    "1. Consolida lo que ya funciona: protege tus fortalezas actuales.\n"
    "2. Diversifica tu oferta: explora nuevas líneas complementarias.\n"
    "3. Invierte en innovación gradual: usa herramientas digitales accesibles.\n"
    "4. Mide tu salud financiera mensualmente.\n"
    "5. Revisa indicadores clave del mercado local una vez al mes."
)
    elif nivel == "Medio":
        return (
            "1. Revisa tu flujo de caja y controla gastos.
"
            "2. Fortalece la captación de clientes con promociones o fidelización.
"
            "3. Mejora tu presencia digital (Google, redes sociales).
"
            "4. Automatiza procesos administrativos básicos.
"
            "5. Busca apoyo en programas locales para PyMEs."
        )
    else:
        return (
            "1. Diagnostica tus costos y elimina lo no esencial.
"
            "2. Enfócate en productos o servicios más rentables.
"
            "3. Busca apoyo externo: incubadoras, universidades, gobierno.
"
            "4. Aumenta visibilidad con promociones digitales.
"
            "5. Considera alianzas estratégicas con negocios compatibles."
        )

def generar_pdf(nombre_empresa, municipio, nivel, recomendacion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informe de Diagnóstico - PyME", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Empresa: {nombre_empresa}", ln=True)
    pdf.cell(200, 10, txt=f"Municipio: {municipio}", ln=True)
    pdf.cell(200, 10, txt=f"Nivel de riesgo detectado: {nivel}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Recomendación detallada:
" + recomendacion)
    ruta = os.path.join("/tmp", f"Informe_{nombre_empresa.replace(' ', '_')}.pdf")
    pdf.output(ruta)
    return ruta

def guardar_diagnostico(data):
    ruta = "registros_pymes.csv"
    if os.path.exists(ruta):
        df = pd.read_csv(ruta)
        df = pd.concat([df, data], ignore_index=True)
    else:
        df = data
    df.to_csv(ruta, index=False)

# Interfaz
st.title("Asistente de Diagnóstico para PyMEs")

acepta = st.checkbox("He leído y acepto el aviso de privacidad")
if acepta:
    nombre_empresa = st.text_input("Nombre de la empresa")
    municipio = st.selectbox("Municipio:", ["León", "Irapuato", "Celaya", "Salamanca", "Silao"])
    antiguedad = st.selectbox("Antigüedad:", ["<1 año", "1–3 años", "4–7 años", ">7 años"])
    empleados = st.selectbox("Empleados:", ["1–5", "6–10", "11–20", ">20"])
    ingresos = st.selectbox("Ingresos:", ["<25k", "25–50k", "50–100k", ">100k"])
    deuda = st.selectbox("Porcentaje de deuda:", ["0%", "1–25%", "26–50%", ">50%"])
    clientes = st.selectbox("Clientes fijos:", ["<10", "10–25", "26–50", ">50"])
    software = st.radio("¿Usa software?", ["Sí", "No"])
    digital = st.selectbox("Digitalización:", ["Nulo", "Bajo", "Medio", "Alto"])
    estrategia = st.selectbox("Estrategia de crecimiento:", ["No", "En proceso", "Sí"])
    competencia = st.slider("Competencia local:", 10, 150, 80)
    desempleo = st.slider("Desempleo (%):", 3.0, 10.0, 5.0)
    innovacion = st.slider("Innovación (0–5):", 0, 5, 2)

    map_vals = {
        "antiguedad": {"<1 año": 0, "1–3 años": 1, "4–7 años": 2, ">7 años": 3},
        "empleados": {"1–5": 1, "6–10": 2, "11–20": 3, ">20": 4},
        "ingresos": {"<25k": 0, "25–50k": 1, "50–100k": 2, ">100k": 3},
        "deuda": {"0%": 0, "1–25%": 1, "26–50%": 2, ">50%": 3},
        "clientes": {"<10": 0, "10–25": 1, "26–50": 2, ">50": 3},
        "software": {"No": 0, "Sí": 1},
        "digital": {"Nulo": 0, "Bajo": 1, "Medio": 2, "Alto": 3},
        "estrategia": {"No": 0, "En proceso": 1, "Sí": 2}
    }

    entrada = pd.DataFrame([[
        map_vals["antiguedad"][antiguedad],
        map_vals["empleados"][empleados],
        map_vals["ingresos"][ingresos],
        map_vals["deuda"][deuda],
        map_vals["clientes"][clientes],
        map_vals["software"][software],
        map_vals["digital"][digital],
        map_vals["estrategia"][estrategia],
        competencia,
        desempleo,
        innovacion
    ]], columns=X_train.columns)

    if st.button("Obtener Diagnóstico"):
        pred = model.predict(entrada)[0]
        nivel = niveles[pred]
        recomendacion = obtener_recomendacion_detallada(nivel)
        st.success(f"Nivel de riesgo detectado: **{nivel}**")
        st.text("Recomendación detallada:")
        st.code(recomendacion)

        df_guardar = pd.DataFrame([{
            "Empresa": nombre_empresa,
            "Municipio": municipio,
            "Nivel de Riesgo": nivel,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        guardar_diagnostico(df_guardar)

        pdf_path = generar_pdf(nombre_empresa, municipio, nivel, recomendacion)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Descargar informe PDF", f, file_name=os.path.basename(pdf_path))
else:
    st.info("Debes aceptar el aviso de privacidad para continuar.")
