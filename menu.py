import streamlit as st

# Configurar la página
st.set_page_config(page_title="Página Principal", layout="centered")


st.markdown("<h1 style='text-align: center;'>Página Principal</h1>", unsafe_allow_html=True)
st.image("../images/AlgoFit2.png", width=300)  # Cambia "tu_imagen.png" por tu imagen o URL
st.write("")
valor = st.slider("Selecciona un valor", 1, 10, 5)
st.write("")
if st.button("Recomendar"):
    st.success(f"Se recomienda el valor: {valor}")
st.write("")

if st.button("Datos Personales"):
    st.switch_page("pages/datos_personales.py")
    