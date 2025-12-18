import streamlit as st
import time
import threading
import requests
from colores import Colores_class

# Funcion para mantener el Render activo
def keep_server_alive():
    while True:
        try:
            requests.get("https://quadcodex-team-back.onrender.com/health", timeout=10)
        except Exception as e:
            print("Error keeping server alive:", e)
        time.sleep(58)

# Config
st.set_page_config(page_title="AlgoFit V0.1-Login", layout="wide")
colores = Colores_class()

# Ocultar barra de arriba
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

# Estilo General
st.markdown(f"""
<style>
.section-login {{
    min-height: 100vh;
    background-image: url("https://public.dir.cat/api/media/file/web-1080x1920-dec-1920x1080.gif");
    background-size: cover;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
}}
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
.title-shadow {{
    font-size: 2.8rem;
    font-weight: 650;
    color: white;
    text-align: center;
    text-shadow: 4px 4px 8px rgba(0,0,0,0.95);
    margin-bottom: 25px;
}}
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

/* ===== TARJETAS ===== */
.card-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    margin-bottom: 40px;
}}
.text-card, .card {{
    background-color: #f9f9f9;
    color: #111;
    width: 300px;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    text-align: center; /* centra todo el contenido */
    transition: transform 0.2s ease-in-out;
}}
.text-card:hover, .card:hover {{
    transform: translateY(-6px);
}}
.text-card img, .card img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    margin-bottom: 15px;
}}
.text-card h3, .card h3 {{
    margin: 10px 0;
    color: #d91f26;
}}
.text-card p, .card p {{
    font-size: 14px;
    color: #555;
    margin-bottom: 15px;
}}
.text-card a, .card a {{
    color: #d91f26;
    text-decoration: none;
    font-weight: bold;
}}
.text-card a:hover, .card a:hover {{
    text-decoration: underline;
}}
.text-card ul, .card ul {{
    list-style: none;
    padding-left: 0;
    margin: 0 auto;
    text-align: center; /* centra listas */
}}
.text-card li, .card li {{
    font-size: 16px;
    color: #000;
    margin-bottom: 5px;
}}

.footer {{
    background-color: #f2f2f2;
    padding: 30px 20px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #333;
    line-height: 1.6;
}}
.footer-container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}}
.footer .section {{
    flex: 1 1 200px;
    margin: 10px;
}}
.footer h4 {{
    margin-bottom: 10px;
}}
.footer ul {{
    list-style-type: none;
    padding-left: 0;
}}
.footer ul li {{
    margin-bottom: 5px;
}}
.footer ul li a {{
    color: #333;
    text-decoration: none;
}}
.footer ul li a:hover {{
    text-decoration: underline;
}}
.footer-bottom {{
    border-top: 1px solid #ccc;
    padding-top: 10px;
    margin-top: 20px;
    font-size: 12px;
    color: #666;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# Login
st.markdown('<div class="login-box">', unsafe_allow_html=True)
st.markdown('<div class="title-shadow">Welcome to AlgoFit</div>', unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.7,6.5,1.7])
with b2:
    t1, t2, t3 = st.columns([3,3,3])
    with t2:
        user = st.text_input("User")
        pwd = st.text_input("Password", type="password")
        b4, b5, b6 = st.columns([5.6,6.5,1.7])
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
                        st.markdown('<div class="custom-error">❌ Incorrect user, please try again</div>', unsafe_allow_html=True)
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
st.markdown('<div class="title-shadow"><h1>    </h1></div>', unsafe_allow_html=True)

# Tarjetas
cols = st.columns([0.2,3,3,3,3,0.2])
cards_data = [
    {
        "img": "https://www.dir.cat/api/media/file/Hyrox-boutique-1-900x480.webp",
        "title": "Cardio Routines",
        "text": "High-intensity training that combines treadmill intervals with functional muscle work, ideal for improving your cardiovascular endurance and toning your entire body. Each session is designed to keep you motivated, burn calories effectively, and give you an energy boost that you'll feel outside the gym."
    },
    {
        "img": "https://www.dir.cat/api/media/file/Bootcamp%20boutique-900x480.webp",
        "title": "Strength Training",
        "text": "High-intensity functional training that combines strength, endurance, and coordination. Designed to help you push your limits and boost your physical performance, with exercises guided by expert instructors. Discover a complete experience that strengthens your body, improves your posture, and increases your energy in every session."
    },
    {
        "img": "https://www.dir.cat/api/media/file/Glow%20Pilates-900x480.jpg",
        "title": "Latest trends in fitness",
        "text": "Fitness is constantly evolving, and at DiR clubs you'll find the activities that are setting trends in Barcelona, including HYROX, Reformer Pilates, Bootcamp, Boxing, and much more. Dynamic, effective workouts led by expert instructors."
    },
    {
        "img": "https://pisojoven.es/wp-content/uploads/2024/01/vista-terraza.jpg",
        "title": "Solarium & Relax",
        "text": "Enjoy our solarium to relax and recharge your batteries after your workouts.",
        "list": ["☀️ Comfortable and safe spaces", "🧘 Relaxation and reading area", "💧 Hydration available"]
    }
]

for i, card in enumerate(cards_data):
    with cols[i+1]:
        st.markdown(f"""
        <div class="text-card">
            <img src="{card['img']}" alt="{card['title']}">
            <h3>{card['title']}</h3>
            <p>{card['text']}</p>
            {"<ul>" + "".join([f"<li>{li}</li>" for li in card.get("list", [])]) + "</ul>" if card.get("list") else ""}
        </div>
        """, unsafe_allow_html=True)
st.markdown('<div class="title-shadow"><h1>    </h1></div>', unsafe_allow_html=True)

# Seccion de "Patrocinador"
st.markdown("""
<style>
.text-card-partner {
    background-color: #f9f9f9;
    border-radius: 16px;
    padding: 30px;
    width: auto;  /* se adapta al contenido */
    max-width: 600px; /* opcional para no exceder cierto ancho */
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    margin: 0 auto; /* centra la tarjeta */
}
.text-card-partner:hover {
    transform: translateY(-6px);
    transition: transform 0.2s ease-in-out;
}

.text-card-partner img {
    width: 100%;
    max-width: 500px; /* limita el ancho máximo de la imagen */
    height: auto; /* mantiene la proporción */
    margin-bottom: 20px;
}

.text-card-partner h3 {
    margin: 10px 0;
    color: #d91f26;
}

.text-card-partner p {
    font-size: 16px;
    color: #444;
    margin-bottom: 15px;
}

.text-card-partner a {
    color: #d91f26;
    text-decoration: none;
    font-weight: bold;
}

.text-card-partner a:hover {
    text-decoration: underline;
}
</style>

<div class="card-container">
    <div class="text-card-partner">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/DiR_logo.png" alt="DIR Logo">
        <h3>Official Sponsor</h3>
        <p>We are proud to have <strong>DiR</strong> as our official sponsor. Thanks to their collaboration, we can offer unique experiences and maintain our quality standards in every activity..</p>
        <p>C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona</p>
        <a href="https://www.dir.cat/es">Club details</a>
    </div>
</div>
""", unsafe_allow_html=True)



# Tarjetas del DIR
dir_cards = [
    {"img": "https://www.dir.cat/api/media/file/DiRAvmadridw-900x480.webp", "title": "DIR AV. MADRID", "text": "C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona"},
    {"img": "https://www.dir.cat/api/media/file/dircampusw-900x480.webp", "title": "DIR CAMPUS", "text": "C/ Avinguda Dr. Marañón, 17, Les Corts, 08028, Barcelona"},
    {"img": "https://www.dir.cat/api/media/file/dirclaretw-900x480.webp", "title": "DIR CASTILLEJOS", "text": "C/ Castillejos, 388, 08025, Barcelona"},
    {"img": "https://www.dir.cat/api/media/file/dirclarisw-900x480.webp", "title": "DIR CLARET", "text": "C/ St. Antoni Maria Claret, 84-86, 08025, Barcelona"},
]

st.markdown('<div class="card-container">', unsafe_allow_html=True)

cols = st.columns([0.2,3,3,3,3,0.2])

# Iterar sobre las tarjetas y asignarlas a cada columna
for i, c in enumerate(dir_cards):
    with cols[i+1]:
        st.markdown(f"""
        <div class="card">
            <img src="{c['img']}" alt="{c['title']}">
            <h3>{c['title']}</h3>
            <p>{c['text']}</p>
        </div>
        """, unsafe_allow_html=True)

# Eventos
st.markdown('<div class="title-shadow">Upcoming Events</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card-container">
    <div class="card">
        <img src="https://public.dir.cat/api/media/file/banner-1080X19201w-1-1920x1080.webp" alt="DIR Av. Madrid">
        <h3>Dir AV. MADRID</h3>
        <p>C/ Av. de Madrid, 170, Sants-Montjuïc, 08028, Barcelona</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
footer = """
<div class="footer">
    <div class="footer-container">
        <div class="section">
            <h4>Partners</h4>
            <ul>
                <li><a href="#">Log in</a></li>
                <li><a href="#">Prestige Club</a></li>
                <li><a href="#">Give AlgoFit as a gift</a></li>
                <li><a href="#">Advantages</a></li>
            </ul>
        </div>
        <div class="section">
            <h4>Company</h4>
            <ul>
                <li><a href="#">Franchises</a></li>
                <li><a href="#">Investments</a></li>
                <li><a href="#">AlgoFit for businesses</a></li>
                <li><a href="#">Sponsors</a></li>
                <li><a href="#">AlgoFit Foundation</a></li>
            </ul>
        </div>
        <div class="section">
            <h4>Information</h4>
            <ul>
                <li><a href="#">About AlgoFit</a></li>
                <li><a href="#">Contact</a></li>
                <li><a href="#">FAQs</a></li>
                <li><a href="#">Work at AlgoFit</a></li>
                <li><a href="#">Communication</a></li>
                <li><a href="#">Magazine</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Singles & Friends</a></li>
                <li><a href="#">Press room</a></li>
                <li><a href="#">Community</a></li>
            </ul>
        </div>
    </div>
    <div class="footer-bottom">
        Gestora Clubs AlgoFit, Barcelona 2025 © | <a href="#">Legal Notice</a> y <a href="#">Privacy Policy</a>
    </div>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
