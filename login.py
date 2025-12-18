import streamlit as st
import time
import threading
import requests
from colores import Colores_class

# ================= FUNCIONES =================
def keep_server_alive():
    while True:
        try:
            requests.get("https://quadcodex-team-back.onrender.com/health", timeout=10)
        except Exception as e:
            print("Error keeping server alive:", e)
        time.sleep(58)

# ================= CONFIG =================
st.set_page_config(page_title="AlgoFit V0.1-Login", layout="wide")
colores = Colores_class()

# ================= OCULTAR UI STREAMLIT =================
st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
header[data-testid="stHeader"] {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ================= CSS =================
st.markdown(f"""
<style>

/* ===== SECCIÓN LOGIN (GIF SOLO AQUÍ) ===== */
.section-login {{
    min-height: 100vh;
    background-image: url("https://public.dir.cat/api/media/file/web-1080x1920-dec-1920x1080.gif");
    background-size: cover;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.login-box {{
    width: 420px;
    padding: 35px;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(6px);
    border-radius: 18px;
}}

/* Inputs */
label {{
    color: white !important;
    font-size: 16px !important;
}}

div[data-baseweb="input"] > div {{
    background-color: {colores.get_botones_2()} !important;
    border-radius: 8px !important;
}}

div[data-baseweb="input"] input {{
    color: black !important;
    padding: 12px !important;
}}

/* Botón */
div.stButton > button {{
    width: 100%;
    padding: 14px;
    font-size: 18px;
    border-radius: 12px;
    background-color: {colores.get_botones_1()};
    color: white;
    border: none;
    transition: 0.2s;
}}
div.stButton > button:hover {{
    background-color: {colores.get_botones_2()};
    color: black;
}}

/* Título */
.title-shadow {{
    font-size: 2.8rem;
    font-weight: 650;
    color: white;
    text-align: center;
    text-shadow: 4px 4px 8px rgba(0,0,0,0.95);
    margin-bottom: 25px;
}}

/* Social icons */
.social-icons {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 15px;
}}
.social-icons img {{
    width: 36px;
    cursor: pointer;
}}

/* ===== SECCIÓN CARDS (FONDO BLANCO) ===== */
.section-cards {{
    background-color: white;
    padding: 80px 10%;
}}

.text-card {{
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: transform 0.2s ease-in-out;
}}

.text-card:hover {{
    transform: translateY(-6px);
}}

.text-card h3 {{
    margin-top: 0;
    color: #111;
}}

.text-card p {{
    color: #444;
}}

</style>
""", unsafe_allow_html=True)

# ================= CONTENEDOR 1: LOGIN =================

st.markdown('<div class="section-login">', unsafe_allow_html=True)
st.markdown('<div class="login-box">', unsafe_allow_html=True)
st.markdown('<div class="title-shadow">Welcome to AlgoFit</div>', unsafe_allow_html=True)

b1, b2, b3 = st.columns([1.7,6.5,1.7])
with b2:
    t1, t2, t3 = st.columns([3,3,3])
    with t2:
        user = st.text_input("User")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            try:
                # Llamada para el login
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
                        thread = threading.Thread(target=keep_server_alive, daemon=True) # Mantener vivo el Render
                        thread.start()
                        st.session_state["server_pinger_started"] = True
                        st.switch_page("pages/menu.py")

                else:
                    st.markdown("""
                    <div class="custom-error">
                        ❌ Incorrect user, please try again
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

st.markdown('</div></div>', unsafe_allow_html=True)

# ================= CONTENEDOR 2: CARDS =================

# CSS para tarjetas (puedes añadir más estilos como colores, íconos, etc.)
st.markdown("""
<style>
.text-card {
    background-color: #ffffff;  /* Fondo blanco */
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 20px;
    color: #000000;  /* Texto negro */
}

.text-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0,0,0,0.2);
}

.text-card h3 {
    color: #2E86C1;  /* Puedes mantener azul para títulos */
}

.text-card p, .text-card li {
    color: #000000;  /* Texto negro para párrafos y listas */
    font-size: 16px;
}

.text-card img {
    height: auto;
}
</style>
""", unsafe_allow_html=True)


# Crear columnas
cols = st.columns(4)

# Nueva tarjeta 1
with cols[0]:
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/api/media/file/Hyrox-boutique-1-900x480.webp" alt="Fuerza">
        <h3>Rutinas de Cardio</h3>
        <p>Entrenamiento funcional de alta intensidad que combina fuerza, resistencia y carrera. Una experiencia desafiante para superar tus propios límites.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 2
with cols[1]:
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/api/media/file/Bootcamp%20boutique-900x480.webp" alt="Cardio">
        <h3>🏃 Entrenamientos FUerza</h3>
        <p>Entrenamiento de alta intensidad que combina intervalos de carrera en cinta con trabajo muscular funcional. Una experiencia completa y exigente para todo el cuerpo.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 3
with cols[2]:
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/api/media/file/Glow%20Pilates-900x480.jpg" alt="Nutrición">
        <h3>Últimes tendències en fitness</h3>
        <p>El fitness evoluciona constantemente, y en los clubs DiR encontrarás las actividades que marcan tendencia en Barcelona. HYROX, Reformer Pilates, Bootcamp, Boxeo y mucho más. Entrenamientos dinámicos, efectivos y guiados por instructores expertos para que descubras nuevas formas de superarte y mantener la motivación.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 4
with cols[3]:
   # Tarjeta del solárium con texto negro
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/sites/default/files/2017-03/solarium-dir.jpg" alt="Bienestar">
        <h3>☀️ Solárium & Relax</h3>
        <p>Disfruta de nuestro solárium para relajarte y recuperar energía después de tus entrenamientos. 
        Un espacio diseñado para el descanso, mejorar tu bienestar y disfrutar de la luz natural de manera segura.</p>
        <ul style="text-align:left; margin-left:20px;">
            <li>☀️ Espacios cómodos y seguros</li>
            <li>🧘 Zona de relax y lectura</li>
            <li>💧 Hidratación disponible</li>
            <li>🕒 Acceso flexible según tu rutina</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

