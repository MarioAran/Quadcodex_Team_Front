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
        time.sleep(58)

st.set_page_config(page_title="AlgoFit V0.1-Login", layout="centered")
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
.stApp {{
    background-image: url("https://public.dir.cat/api/media/file/web-1080x1920-dec-1920x1080.gif");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.block-container {{
    margin-top: 0;
    padding: 0;
    background-color: transparent;
    border-radius: 18px;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}
label {{
    font-weight: 600 !important;
    color: {colores.get_fondo_general()} !important;
    font-size: 18px !important;
}}
.stTextInput {{
    background: #7a7a7a;
    background: linear-gradient(54deg,rgba(122, 122, 122, 1) 0%, rgba(163, 163, 164, 1) 100%);
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
.custom-button {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 8px;
    color: white;
    border: none;
    margin-bottom: 15px;
    background: #020224;
    background: linear-gradient(4deg, rgba(2, 2, 36, 0.57) 72%, rgba(0, 212, 255, 1) 100%);
    cursor: pointer;
    transition: 0.2s ease-in-out;
}
.custom-button:hover {
    background-color: #333333; /* Cambia color al pasar el mouse */
}
</style>
""", unsafe_allow_html=True)

b1, b2, b3 = st.columns([1.7,6.5,1.7])
with b2:
    t1, t2, t3 = st.columns([0.85,9,0.5])
    with t2:
        st.title("Welcome to AlgoFit")
    user = st.text_input("User")
    pwd = st.text_input("Password", type="password")
    
    b4, b5, b6 = st.columns([4.5,6.5,1.7])
    with b5:
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
    with st.expander("Contact"):
        col1, col2 = st.columns(2)
        with col1 :
                st.markdown("""
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <button class="custom-button">
                        <a href="https://www.linkedin.com/in/gabriel-alejandro-michielon-perez/" target="_blank">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" height="24">
                                Gabriel Alejandro Michielon Perez 
                        </a>
                    </button>
                    <button class="custom-button">
                        <a href="https://www.linkedin.com/in/pablo-mesa-valladares/" target="_blank">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" height="24">
                            Pablo Mesa Valladares
                        </a>
                    </button>
                    <button class="custom-button">
                        <a href="https://www.linkedin.com/in/alexis-barros-vera-386a0b398/" target="_blank">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" height="24">
                            Alexis Barros Vera
                        </a>
                    </button>
                    <button class="custom-button">
                        <a href="https://www.linkedin.com/in/mario-german-arancibia-perez/" target="_blank">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" height="24">
                            Mario German Arancibia Perez
                        </a>
                    </button>
                </div>
                """, unsafe_allow_html=True)
        with col2:
                st.markdown("""
                        <button class="custom-button">
                            <a href="https://github.com/MarioAran/Quadcodex_Team_Front" target="_blank">
                                <img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" width="24" height="24">
                                    Github Frontend
                            </a>
                            </button>
                        <button class="custom-button">
                            <a href="https://github.com/MarioAran/Quadcodex_Team_Back" target="_blank">
                                <img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" width="24" height="24">
                                    Github Backend
                            </a>
                        </button>
                """, unsafe_allow_html=True)
