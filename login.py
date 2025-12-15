import streamlit as st
import time
import threading
import requests
from colores import Colores_class

# Funcion para mantener el render abierto
def keep_server_alive():
    while True:
        try:
            requests.get("https://quadcodex-team-back.onrender.com/health", timeout=10)
        except Exception as e:
            print("Error keeping server alive:", e)
        time.sleep(30)

st.set_page_config(page_title="AlgoFit-Login", layout="centered")
colores = Colores_class()

#Diseño
# Ocultar sidebar
hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""

# Ocultar barra superior
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

# Estilo general
st.markdown(f"""
<style>

/* Fondo general */
.stApp {{
    background-color: {colores.get_fondo_general()};
}}

/* Contenedor principal centrado */
.block-container {{
    margin-top: 50px;
    padding: 2rem;
    background-color: {colores.get_cajas_principales()};
    border-radius: 18px;
}}

/* Labels */
label {{
    font-weight: 600 !important;
    color: {colores.get_fondo_general()} !important;
    font-size: 18px !important;
}}

/* Contenedor de inputs */
.stTextInput {{
    background-color: {colores.get_cajas_terciarias()};
    padding: 10px 12px 6px 10px;
    border-radius: 10px;
    border: 2px solid {colores.get_botones_2()};
    margin-bottom: 15px;
}}

/* Inputs de textos y numeros */
div[data-baseweb="input"] > div {{
    background-color: {colores.get_botones_2()} !important;
    border: 2px solid {colores.get_botones_1()} !important;
    border-radius: 8px !important;
}}

div[data-baseweb="input"] input {{
    background-color: {colores.get_botones_2()} !important;
    color: black !important;
    font-size: 16px !important;
    padding: 12px !important;
}}

/* Focus de los inputs */
div[data-baseweb="input"]:focus-within {{
    border: 3px solid white !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}}

div[data-baseweb="input"] input:focus {{
    outline: none !important;
    box-shadow: none !important;
}}

/* Botones */
div.stButton > button {{
    width: 100%;
    padding: 15px 40px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
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

h1 {{
    text-align: center;
}}

/* Boton del ojo */
div[data-baseweb="input"] button {{
    background-color: transparent !important;
    border-radius: 6px;
}}

/* SVG del ojo */
div[data-baseweb="input"] button svg {{
    fill: {colores.get_botones_1()} !important;
    opacity: 0.9;
}}

/* Hover */
div[data-baseweb="input"] button:hover svg {{
    fill: white !important;
    opacity: 1;
}}

/* Focus */
div[data-baseweb="input"] button:focus {{
    outline: none !important;
    box-shadow: none !important;
}}

""", unsafe_allow_html=True)

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

st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Welcome Back")
user = st.text_input("User")
pwd = st.text_input("Password", type="password")

b1, b2, b3 = st.columns([3.2,3,2])
with b2:
    if st.button("Login"):
        try:
            payload = {"dni": user}
            resp = requests.post(
                "https://quadcodex-team-back.onrender.com/login",
                json=payload,
                timeout=10
            )

            if resp.status_code == 200:
                data = resp.json()

                #Guardar usuario completo
                st.session_state["user"] = data["usuario"]

                #Guarda el ID correctamente
                st.session_state["id_usuario"] = data["usuario"]["id_user"]

                #Mantener backend despierto solo una vez
                if "server_pinger_started" not in st.session_state:
                    thread = threading.Thread(
                        target=keep_server_alive,
                        daemon=True
                    )
                    thread.start()
                    st.session_state["server_pinger_started"] = True

                st.switch_page("pages/menu.py")

            else:
                st.error(f"API error {resp.status_code}: {resp.text}")

        except Exception as e:
            st.error(f"Could not connect to API: {e}")
