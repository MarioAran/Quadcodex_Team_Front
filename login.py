import streamlit as st
import time
import threading
import requests
from colores import Colores_class

def keep_server_alive():
    while True:
        try:
            requests.get("https://quadcodex-team-back.onrender.com/health", timeout=10)
        except Exception as e:
            print("Error keeping server alive:", e)
        time.sleep(30)
st.set_page_config(page_title="AlgoFit-Login", layout="centered")
colores = Colores_class()
hide_menu_style = """
<style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"],
    div[data-testid="expandedSidebar"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown(f"""
<style>
/* Imagen de fondo */
.stApp {{
    background-image: url("https://public.dir.cat/api/media/file/web-1080x1920-dec-1920x1080.gif");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Contenedor principal */
.block-container {{
    margin-top: 0;
    padding: 0;
    background-color: transparent;
    border-radius: 18px;
    height: 100vh; /* toda la pantalla */
    display: flex;
    justify-content: center; /* horizontal */
    align-items: center;    /* vertical */
}}

/* Labels */
label {{
    font-weight: 600 !important;
    color: {colores.get_fondo_general()} !important;
    font-size: 18px !important;
}}

/* Inputs */
.stTextInput {{
    background-color: {colores.get_cajas_terciarias()};
    padding: 10px 12px 6px 10px;
    border-radius: 10px;
    border: 2px solid {colores.get_botones_2()};
    margin-bottom: 15px;
}}
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

/* Logos de login social */
.social-icons {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 15px;
}}
.social-icons img {{
    width: 40px;
    height: 40px;
    cursor: pointer;
    transition: transform 0.2s;
}}
.social-icons img:hover {{
    transform: scale(1.2);
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Botón flotante "Contacts" fijo abajo a la derecha */
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
    cursor: pointer;
    z-index: 9999;
    transition: all 0.2s ease-in-out;
}
.contact-button:hover {
    background-color: #1995AD;
    transform: scale(1.05);
}

/* Panel de contactos */
.contact-panel {
    position: fixed;
    bottom: 70px; /* arriba del botón */
    right: 20px;
    width: 320px;
    background-color: #A1D6E2;
    border-radius: 15px;
    padding: 20px;
    display: none;
    flex-direction: column;
    gap: 15px;
    z-index: 9999;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

/* Cada recuadro/link dentro del panel */
.contact-box {
    background-color: white;
    color: black;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    transition: background-color 0.2s, color 0.2s, transform 0.2s;
    cursor: pointer;
}
.contact-box:hover {
    background-color: #1995AD;
    color: white;
    transform: scale(1.05);
}
</style>

<!-- Botón flotante -->
<div class="contact-button" onclick="togglePanel()">Contacts</div>

<!-- Panel de contactos -->
<div class="contact-panel" id="contactPanel">
    <a href="https://docs.google.com/document/d/1PVFGo_wejt-lQle5M6s0c27xSXvV65I2l97M_cnZuEU/edit?usp=sharing"
       target="_blank" class="contact-box">Documentación</a>
    <a href="https://www.google.com" target="_blank" class="contact-box">Google</a>
    <a href="https://www.facebook.com" target="_blank" class="contact-box">Facebook</a>
    <a href="https://www.twitter.com" target="_blank" class="contact-box">X/Twitter</a>
</div>

<script>
function togglePanel() {
    var panel = document.getElementById("contactPanel");
    if (panel.style.display === "flex") {
        panel.style.display = "none";
    } else {
        panel.style.display = "flex";
    }
}
</script>
""", unsafe_allow_html=True)

b1, b2, b3 = st.columns([3,5,3])
with b2:
    st.title("Welcome Back")
    user = st.text_input("User")
    pwd = st.text_input("Password", type="password")
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
                st.session_state["user"] = data["usuario"]
                st.session_state["id_usuario"] = data["usuario"]["id_user"]

                if "server_pinger_started" not in st.session_state:
                    thread = threading.Thread(target=keep_server_alive, daemon=True)
                    thread.start()
                    st.session_state["server_pinger_started"] = True

                st.switch_page("pages/menu.py")
            else:
                st.markdown("""
                <div class="custom-error">
                    ❌ Usuario incorrecto, vuelva a intentarlo
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not connect to API: {e}")

st.markdown("""
<div class="social-icons">
    <img src="https://upload.wikimedia.org/wikipedia/commons/archive/c/c1/20210618182605%21Google_%22G%22_logo.svg" alt="Google" title="Login with Google">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" title="Login with Facebook">
    <img src="https://abs.twimg.com/responsive-web/client-web/icon-default.522d363a.png" alt="X" title="Login with X">
</div>
""", unsafe_allow_html=True)
