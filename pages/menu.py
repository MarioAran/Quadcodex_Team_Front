import streamlit as st
from colores import Colores_class

st.set_page_config(page_title="AlgoFit-Lobby", layout="centered")
colores = Colores_class()

# Ocultar sidebar
hide_menu_style = f"""
    <style>
        [data-testid="stSidebar"] {{display: none !important;}}
        [data-testid="stSidebarNav"] {{display: none !important;}}
        section[data-testid="stSidebar"] {{display: none !important;}}
        div[data-testid="expandedSidebar"] {{display: none !important;}}
    </style>
"""

# Estilo general + botones
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("https://static.vecteezy.com/system/resources/previews/006/469/232/non_2x/abstract-white-background-with-halftone-texture-free-vector.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Contenedor principal */
        .block-container {{
            margin-top: 50px; 
            padding-top: 2rem;
            background-color: {colores.get_cajas_principales_trans()};
            border-radius: 15px;
            padding-bottom: 1rem;
        }}

        /* Botones */
        div.stButton > button {{
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            background-color: {colores.get_botones_1()};
            color: white;
            border: 2px solid {colores.get_botones_2()};
            transition: 0.2s ease-in-out;
        }}

        div.stButton > button:hover {{
            background-color: {colores.get_botones_2()};
            color: black;
            border: 2px solid {colores.get_botones_1()};
        }}

        /* Ocultar barra superior */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("""
    <style>
        .contact-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #A1D6E2;
            color: white;
            padding: 14px 22px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            z-index: 9999;
        }

        .contact-button:hover {
            background-color: #1995AD;
            transform: scale(1.05);
            color: white;
        }
    </style>

    <a href="https://docs.google.com/document/d/1PVFGo_wejt-lQle5M6s0c27xSXvV65I2l97M_cnZuEU/edit?usp=sharing"
       target="_blank"
       class="contact-button">
        Contacts
    </a>
""", unsafe_allow_html=True)

container = st.container(vertical_alignment = "center", border=False)

with container:
    # Crear columnas para centrar toda la caja
    col1, col2, col3 = st.columns([0.2, 1, 0.2],vertical_alignment="center")

    with col2:
        im1, im2, im3 = st.columns([0.3,1,0.3])
        with im2:
            st.image("images/AlgoFit2.png", width=600)
        st.write("")
        container2 = st.container(vertical_alignment = "center", border=False)
        with container2:
            # Boton Recomendar
            b1, b2, b3 = st.columns([2.3,3,2])
            with b2:
                if st.button("Recomendar"):
                    st.switch_page("pages/training_recommend.py")
            st.write("")
            b4, b5, b6 = st.columns([2.4,4,2])
            with b5:
                if st.button("Datos Personales"):
                    st.switch_page("pages/datos_personales.py")
        st.markdown('</div>', unsafe_allow_html=True)