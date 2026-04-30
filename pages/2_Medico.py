import streamlit as st
import numpy as np
import urllib.parse

st.set_page_config(page_title="AMPA Médico", layout="centered")
st.title("Interpretación AMPA - Modo médico")

# Leer datos del QR via session_state o query_params
datos_raw = ""

if "datos_qr" in st.session_state:
    datos_raw = st.session_state["datos_qr"]
elif "data" in st.query_params:
    datos_raw = st.query_params["data"]

if datos_raw:
    texto_pre = urllib.parse.unquote(datos_raw)
    st.success("Datos cargados automáticamente desde el QR")
else:
    texto_pre = ""

st.write("Pega aquí los datos generados por la app del paciente.")
texto = st.text_area("Datos AMPA del paciente", value=texto_pre, height=160)

excluir_primer_dia = st.checkbox("Excluir primer día", value=True)

def parsear_datos(texto):
    dias = texto.strip().split(";")
    lecturas = []
    for d in dias:
        if d.strip() == "":
            continue
        nombre_dia, valores = d.split(":")
        dia_num = int(nombre_dia.replace("D", ""))
        pares = valores.split(",")
        for p in pares:
            sis, dia = p.split("/")
            lecturas.append((dia_num, int(sis), int(dia)))
    return lecturas

if st.button("Analizar AMPA"):
    try:
        lecturas = parsear_datos(texto)
        if excluir_primer_dia:
            lecturas_validas = [x for x in lecturas if x[0] != 1]
        else:
            lecturas_validas = lecturas

        sistolicas = [x[1] for x in lecturas_validas]
        diastolicas = [x[2] for x in lecturas_validas]
        media_sis = round(np.mean(sistolicas), 1)
        media_dia = round(np.mean(diastolicas), 1)

        st.subheader("Resultado")
        st.write(f"Lecturas válidas: {len(lecturas_validas)}")
        st.write(f"Media AMPA: {media_sis}/{media_dia} mmHg")

        if len(lecturas_validas) < 12:
            st.warning("Número bajo de lecturas válidas. Interpretar con cautela.")

        if media_sis < 135 and media_dia < 85:
            interpretacion = "control adecuado de la presión arterial domiciliaria"
            st.success("AMPA controlada")
        else:
            interpretacion = "mal control de la presión arterial domiciliaria"
            st.error("AMPA no controlada")

        texto_clinico = (
            f"Monitorización domiciliaria de presión arterial (AMPA) "
            f"con {len(lecturas_validas)} lecturas válidas. "
        )
        if excluir_primer_dia:
            texto_clinico += "Se excluye el primer día del análisis. "
        texto_clinico += (
            f"Media domiciliaria de {media_sis}/{media_dia} mmHg. "
            f"Resultado compatible con {interpretacion}."
        )

        st.subheader("Texto clínico")
        st.text_area("Copiar a historia clínica", texto_clinico, height=130)

    except Exception as e:
        st.error("No se pudieron interpretar los datos. Revisa que el formato sea correcto.")
        st.write(e)
