import streamlit as st


import os
st.write("Working dir:", os.getcwd())
st.write("¿Existe la imagen?", os.path.exists("../images/AlgoFit.png"))
st.write("Listando carpeta images:", os.listdir("../images") if os.path.exists("images") else "No existe")


# Configurar la página
st.set_page_config(page_title="Página Principal", layout="centered")

# Ocultar sidebar
hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""

st.markdown("""
    <style>
        div.stButton > button {
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Ocultar barra superior */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Evitar padding superior extra */
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(hide_menu_style, unsafe_allow_html=True)

container = st.container(vertical_alignment = "center", border=True)

with container:
    # Crear columnas para centrar toda la caja
    col1, col2, col3 = st.columns([0.2, 1, 0.2],vertical_alignment="center")

    with col2:
        #st.markdown("<h1 style='text-align: center;'>Página Principal</h1>", unsafe_allow_html=True)
        
        im1, im2, im3 = st.columns([0.3,1,0.3])
        with im2:
            st.image("../images/AlgoFit.png", width=300)

        valor = st.slider("", 1, 10, 5)
        st.write("")

        container2 = st.container(vertical_alignment = "center", border=False)

        with container2:

            # Botón Recomendar centrado
            b1, b2, b3 = st.columns([2.3,3,2])
            with b2:
                if st.button("Recomendar"):
                    st.switch_page("pages/training_recommend.py")

            st.write("")

            # Botón Datos personales centrado
            b4, b5, b6 = st.columns([2.4,4,2])
            with b5:
                if st.button("Datos Personales"):
                    st.switch_page("pages/datos_personales.py")

        # Cierra la caja
        st.markdown('</div>', unsafe_allow_html=True)
