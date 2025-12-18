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


####test



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
st.markdown('<div class="section-login">', unsafe_allow_html=True)
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
        <p>Entrenamiento de alta intensidad que combina intervalos de carrera en cinta con trabajo muscular funcional. Una experiencia completa y exigente para todo el cuerpo.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 2
with cols[1]:
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/api/media/file/Bootcamp%20boutique-900x480.webp" alt="Cardio">
        <h3>Entrenamientos Fuerza</h3>
        <p>Entrenamiento funcional de alta intensidad que combina fuerza. Una experiencia desafiante para superar tus propios límites.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 3
with cols[2]:
    st.markdown("""
    <div class="text-card">
        <img src="https://www.dir.cat/api/media/file/Glow%20Pilates-900x480.jpg" alt="Nutrición">
        <h3>Ultimas tendencias en fitness</h3>
        <p>El fitness evoluciona constantemente, y en los clubs DiR encontrarás las actividades que marcan tendencia en Barcelona. </p>
        <p>HYROX, Reformer Pilates, Bootcamp, Boxeo y mucho más. Entrenamientos dinámicos, efectivos y guiados por instructores expertos para que descubras nuevas formas de superarte y mantener la motivación.</p>
    </div>
    """, unsafe_allow_html=True)

# Nueva tarjeta 4
with cols[3]:
   # Tarjeta del solárium con texto negro
    st.markdown("""
    <div class="text-card">
        <img src="https://pisojoven.es/wp-content/uploads/2024/01/vista-terraza.jpg" alt="Bienestar">
        <h3>Solarium & Relax</h3>
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

#=====================

# CSS para las tarjetas tipo directorio
st.markdown("""
<style>
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    margin-bottom: 40px;
}

.card {
    background-color: #0d1117;
    color: #ffffff;
    width: 250px;
    border-radius: 10px;
    overflow: hidden;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
}

.card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
}

.card h3 {
    font-family: 'Arial Black', sans-serif;
    margin: 10px 0;
}

.card p {
    font-size: 14px;
    margin: 5px 10px;
}

.card a {
    display: block;
    margin: 10px 0 15px 0;
    color: #00aaff;
    text-decoration: none;
}

.card a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Contenido HTML con las tarjetas
st.markdown("""
<style>
.card-container {
    display: flex;
    justify-content: center;
    margin: 30px 0;
}
.text-card {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 20px;
    max-width: 400px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.text-card img {
    margin-bottom: 15px;
}
.text-card h3 {
    text-align: center;
    margin: 10px 0;
    color: #d91f26;
}
.text-card p {
    font-size: 14px;
    color: #555;
    margin-bottom: 15px;
}
.text-card a {
    color: #d91f26;
    text-decoration: none;
    font-weight: bold;
}
.text-card a:hover {
    text-decoration: underline;
}
</style>

<div class="card-container">
    <div class="text-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/DiR_logo.png" alt="DIR Logo">
        <h3>Patrocinador Oficial</h3>
        <p>Estamos orgullosos de contar con <strong>DiR</strong> como nuestro patrocinador oficial. Gracias a su colaboración, podemos ofrecer experiencias únicas y mantener nuestros estándares de calidad en cada actividad.</p>
        <p>C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona</p>
        <a href="https://www.dir.cat/es">Detalles del club</a>
    </div>
</div>
""", unsafe_allow_html=True)
 

st.markdown("""
<div class="card-container">
    <div class="card">
        <img src="https://www.dir.cat/api/media/file/DiRAvmadridw-900x480.webp" alt="DIR Av. Madrid">
        <h3>DIR AV. MADRID</h3>
        <p>C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona</p>
    </div>
    <div class="card">
        <img src="https://www.dir.cat/api/media/file/dircampusw-900x480.webp" alt="DIR Campus">
        <h3>DIR CAMPUS</h3>
        <p>C/ Avinguda Dr. Marañón, 17, Les Corts, 08028, Barcelona</p>
    </div>
    <div class="card">
        <img src="https://www.dir.cat/api/media/file/dirclaretw-900x480.webp" alt="DIR Castillejos">
        <h3>DIR CASTILLEJOS</h3>
        <p>C/ Castillejos, 388, 08025, Barcelona</p>
    </div>
    <div class="card">
        <img src="https://www.dir.cat/api/media/file/dirclarisw-900x480.webp" alt="DIR Claret">
        <h3>DIR CLARET</h3>
        <p>C/ St. Antoni Maria Claret, 84-86, 08025, Barcelona</p>
    </div>
</div>
""", unsafe_allow_html=True) 





###3====EVENTOS 

st.markdown('<div class="title-shadow">Proximos Eventos</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card-container">
    <div class="card">
        <img src="https://public.dir.cat/api/media/file/banner-1080X19201w-1-1920x1080.webp" alt="DIR Av. Madrid">
        <h3>Dir AV. MADRID</h3>
        <p>C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona</p>
    </div>
</div>
""", unsafe_allow_html=True)


####FOOTER=========

footer = """
<style>
.footer {
    background-color: #f2f2f2;
    padding: 30px 20px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #333;
    line-height: 1.6;
}
.footer-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}
.footer .section {
    flex: 1 1 200px;
    margin: 10px;
}
.footer h4 {
    margin-bottom: 10px;
}
.footer ul {
    list-style-type: none;
    padding-left: 0;
}
.footer ul li {
    margin-bottom: 5px;
}
.footer ul li a {
    color: #333;
    text-decoration: none;
}
.footer ul li a:hover {
    text-decoration: underline;
}
.footer-bottom {
    border-top: 1px solid #ccc;
    padding-top: 10px;
    margin-top: 20px;
    font-size: 12px;
    color: #666;
    text-align: center;
}
</style>

<div class="footer">
    <div class="footer-container">
        <div class="section">
            <h4>Socios</h4>
            <ul>
                <li><a href="#">Conectarse</a></li>
                <li><a href="#">Club Prestige</a></li>
                <li><a href="#">Regala Algo Fit</a></li>
                <li><a href="#">Ventajas</a></li>
            </ul>
        </div>
        <div class="section">
            <h4>Empresa</h4>
            <ul>
                <li><a href="#">Franquicias</a></li>
                <li><a href="#">Inversiones</a></li>
                <li><a href="#">Algo Fit para empresas</a></li>
                <li><a href="#">Patrocinadores</a></li>
                <li><a href="#">Fundación Algo Fit</a></li>
            </ul>
        </div>
        <div class="section">
            <h4>Información</h4>
            <ul>
                <li><a href="#">Sobre Algo Fit</a></li>
                <li><a href="#">Contacto</a></li>
                <li><a href="#">FAQs</a></li>
                <li><a href="#">Trabaja en Algo Fit</a></li>
                <li><a href="#">Comunicación</a></li>
                <li><a href="#">Revista</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Singles & Friends</a></li>
                <li><a href="#">Sala de prensa</a></li>
                <li><a href="#">Comunidad</a></li>
            </ul>
        </div>
    </div>
    <div class="footer-bottom">
        Gestora Clubs AlgoFit, Barcelona 2025 © | <a href="#">Aviso Legal</a> y <a href="#">Política de privacidad</a>
    </div>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
