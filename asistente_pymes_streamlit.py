
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os
from fpdf import FPDF
from datetime import datetime

# Simular datos de entrenamiento
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

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Streamlit App
st.title("Asistente de Diagnóstico para PyMEs")

st.markdown("Este asistente predice el nivel de riesgo de tu PyME y ofrece recomendaciones según tu situación.")

acepta = st.checkbox("He leído y acepto el aviso de privacidad")

if acepta:
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
        niveles = {0: "Bajo", 1: "Medio", 2: "Alto"}
        st.success(f"Nivel de riesgo detectado: **{niveles[pred]}**")
else:
    st.info("Debes aceptar el aviso de privacidad para continuar.")
