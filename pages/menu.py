import streamlit as st

# Configurar página
st.set_page_config(page_title="Página Principal", layout="centered")

# Paleta de colores
AZUL_OSCURO = "#1995AD"
AZUL_MEDIO = "#A1D6E2"
AZUL_CLARO = "#BCBABE"
AZUL_BLANCO = "#F1F1F2"

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
        /* Fondo general */
        .stApp {{
            background-color: {AZUL_BLANCO};
        }}

        /* Contenedor principal */
        .block-container {{
            margin-top: 50px;  /* <-- separa del borde superior */
            padding-top: 2rem;
            background-color: {AZUL_CLARO};
            border-radius: 15px;
            padding-bottom: 1rem;
        }}

        /* Botones */
        div.stButton > button {{
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            background-color: {AZUL_OSCURO};
            color: white;
            border: 2px solid {AZUL_MEDIO};
            transition: 0.2s ease-in-out;
        }}

        div.stButton > button:hover {{
            background-color: {AZUL_MEDIO};
            color: black;
            border: 2px solid {AZUL_OSCURO};
        }}

        /* Ocultar barra superior */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(hide_menu_style, unsafe_allow_html=True)

container = st.container(vertical_alignment = "center", border=False)

with container:
    # Crear columnas para centrar toda la caja
    col1, col2, col3 = st.columns([0.2, 1, 0.2],vertical_alignment="center")

    with col2:
        #st.markdown("<h1 style='text-align: center;'>Página Principal</h1>", unsafe_allow_html=True)
        im1, im2, im3 = st.columns([0.3,1,0.3])
        with im2:
            st.image("images/AlgoFit2.png", width=600)
        st.write("")
        container2 = st.container(vertical_alignment = "center", border=False)
        with container2:
            # Botón Recomendar centrado
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