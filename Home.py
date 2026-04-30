import streamlit as st

st.set_page_config(page_title="Sistema AMPA", layout="centered")

st.markdown("""
<div style="text-align: center;">
    <h1 style="color:#1F618D;">Sistema AMPA con QR</h1>
    <h4 style="color:gray;">
        Digitalización del control domiciliario de la presión arterial
    </h4>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Paciente")
    st.write("Registra tus mediciones y genera un QR para consulta.")
    if st.button("Ir a Paciente", use_container_width=True):
        st.switch_page("pages/1_Paciente.py")

with col2:
    st.markdown("### 👩‍⚕️ Médico")
    st.write("Escanea el QR y analiza automáticamente los resultados.")
    if st.button("Ir a Médico", use_container_width=True):
        st.switch_page("pages/2_Medico.py")

st.divider()
st.caption("Proyecto de Salud Digital en Atención Primaria | AMPA QR System")
