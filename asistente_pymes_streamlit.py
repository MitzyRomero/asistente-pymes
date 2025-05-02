
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from fpdf import FPDF
import os
from datetime import datetime

# --------------------------
# ENTRENAMIENTO DEL MODELO
# --------------------------
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

# --------------------------
# FUNCIONES DE UTILIDAD
# --------------------------
niveles = {0: "Bajo", 1: "Medio", 2: "Alto"}

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
    pdf.multi_cell(0, 10, txt=f"Recomendación:\n{recomendacion}")
    nombre_archivo = f"Informe_{nombre_empresa.replace(' ', '_')}.pdf"
    ruta = os.path.join("/tmp", nombre_archivo)
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

def obtener_recomendacion(nivel):
    if nivel == "Bajo":
        return " Riesgo bajo. Continúe con su estrategia actual y explore nuevas oportunidades de mercado."
    elif nivel == "Medio":
        return "Riesgo medio. Fortalezca su base de clientes y considere implementar herramientas digitales."
    else:
        return "Riesgo alto. Revise su estructura financiera, reduzca deuda y busque asesoría externa."

# --------------------------
# INTERFAZ STREAMLIT
# --------------------------
st.title("Asistente de Diagnóstico para PyMEs")

modo_admin = st.sidebar.checkbox("🔐 Modo administrador")

if modo_admin:
    pwd = st.sidebar.text_input("Contraseña de administrador", type="password")
    if pwd == "admin123":
        st.subheader("Panel de Resumen")
        if os.path.exists("registros_pymes.csv"):
            df_admin = pd.read_csv("registros_pymes.csv")
            st.dataframe(df_admin)
            resumen = df_admin.groupby(["Municipio", "Nivel de Riesgo"]).size().unstack(fill_value=0)
            st.subheader("Resumen por Municipio y Nivel de Riesgo")
            st.dataframe(resumen)
        else:
            st.info("Aún no hay registros.")
    else:
        st.warning("Contraseña incorrecta.")
else:
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
            recomendacion = obtener_recomendacion(nivel)
            st.success(f"Nivel de riesgo detectado: **{nivel}**")
            st.markdown(recomendacion)

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
