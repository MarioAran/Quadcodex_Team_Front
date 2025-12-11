import streamlit as st

# Configurar la página
st.set_page_config(page_title="Página Principal", layout="centered")

hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'>Página Principal</h1>", unsafe_allow_html=True)
st.image("../images/AlgoFit.png", width=300)  # Cambia "tu_imagen.png" por tu imagen o URL
st.write("")
valor = st.slider("Selecciona un valor", 1, 10, 5)
st.write("")
if st.button("Recomendar"):
    st.switch_page("pages/training_recommend.py")
st.write("")

if st.button("Datos Personales"):
    st.switch_page("pages/datos_personales.py")
    