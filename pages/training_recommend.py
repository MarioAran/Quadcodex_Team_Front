import streamlit as st
import requests

from colores import Colores_class

MUSCLE_MAP = {
    "abs": "abs", "abdominals": "abs", "core": "abs",
    "quadriceps": "legs", "quads": "legs", "hamstrings": "legs",
    "calves": "legs", "legs": "legs",
    "chest": "chest", "pecs": "chest", "pectorals": "chest",
    "back": "back", "lats": "back", "latissimus": "back",
    "shoulders": "shoulders", "deltoids": "shoulders",
    "biceps": "biceps", "triceps": "triceps",
    "glutes": "glutes"
}

# Mapa final → imagen
MUSCLE_IMAGES = {
    "abs": "images/AlgoFit_Abs.png",
    "legs": "images/AlgoFit_Legs.png",
    "chest": "images/AlgoFit_Chest.png",
    "back": "images/AlgoFit_Back.png",
    "shoulders": "images/AlgoFit_Shoulders.png",
    "biceps": "images/AlgoFit_Biceps.png",
    "triceps": "images/AlgoFit_Triceps.png",
    "glutes": "images/AlgoFit_Glutes.png",
}

DEFAULT_IMAGE = "https://via.placeholder.com/80x80.png?text=IMG"

def get_muscle_image(muscles: list[str]) -> str:
    """
    Recibe la lista de músculos de un ejercicio y devuelve
    la imagen correspondiente al músculo principal.
    """

    # 1. Recorrer músculos declarados en el ejercicio
    for m in muscles:
        m_clean = m.lower().strip()

        # 2. Buscar en MUSCLE_MAP
        if m_clean in MUSCLE_MAP:
            muscle_key = MUSCLE_MAP[m_clean]

            # 3. Buscar imagen en MUSCLE_IMAGES
            return MUSCLE_IMAGES.get(muscle_key, DEFAULT_IMAGE)

    # 4. Si no encuentra nada, imagen por defecto
    return DEFAULT_IMAGE

st.set_page_config(page_title="AlgoFit-Training Plan", layout="wide")
colores = Colores_class()

hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""

st.markdown(f"""
    <style>
        /* Fondo general */
        .stApp {{
            background-color: {colores.get_fondo_general()};
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

         /* Slider */
        .stSlider > div[data-baseweb="slider"] > div > div > div {{
            background-color: {colores.get_cajas_terciarias()} !important;
        }}
        .stSlider > div[data-baseweb="slider"] > div > div > div > div {{
            background-color: {colores.get_botones_1()} !important;
            border: 2px solid {colores.get_botones_1()} !important;
        }}
        .stSlider > div[data-baseweb="slider"] > div > div > div > div > div {{
            color: black !important;
        }}
        
        /* Ocultar barra superior */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <style>
    /* Texto dentro de los containers de recomendaciones */
    div[class*="st-key-rec_container_"] * {{
        color: black !important;
    }}

    /* Texto dentro de los sliders */
    .stSlider * {{
        color: black !important;
    }}
    </style>
""", unsafe_allow_html=True)

css = f"""
<style>
/* Container principal */
div[class*="st-key-my_blue_container"] {{
    background-color: {colores.get_cajas_principales()};
    border-radius: 14px;
    padding: 20px;
}}

/* Containers de recomendaciones */
div[class*="st-key-rec_container_"] {{
    background-color: {colores.get_botones_2()};
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.markdown(hide_menu_style, unsafe_allow_html=True)

container = st.container(key="my_blue_container",vertical_alignment = "center", border=True )


with container:
    # ---------- Botón volver ----------
    if st.button("⬅ Back to Main Page"):
        st.switch_page("pages/menu.py")


    # ---------- Crear columnas: imagen izquierda, contenido derecha ----------
    cols_layout = st.columns([0.5, 3])  # 1 parte para imagen, 3 partes para contenido

    with cols_layout[0]:
        # Imagen del usuario
        st.image("images/AlgoFitTrain.png", width=200)

    with cols_layout[1]:
        # Título y datos
        st.title("Your Personalized Training Plan")

        # ---------- Datos ----------
        if "recomendaciones" not in st.session_state:
            st.error("❌ No data received. Please complete your profile first.")
            st.stop()
        usuario = st.session_state["usuario"]

        data = st.session_state["recomendaciones"]
        user = data.get("user_data", {})
        recs = data.get("recomendaciones", [])

        # ---------- INVERTIR EL ORDEN ----------
        recs = sorted(recs, key=lambda x: x.get("rating_score", 0), reverse=True)


        st.markdown(f"**User:** {usuario.Nombre} {usuario.Apellido} | **Gender:** {usuario.Genero} | Age: {usuario.Edad} | Height: {usuario.Altura} cm | Weight: {usuario.Peso} kg")
        st.markdown(f"**Level:** {usuario.Nivel} | **Exercises Recommended:** {len(st.session_state.get('recomendaciones', {}).get('recomendaciones', []))}")

#st.write("---")

# ---------- Mostrar ejercicios en tarjetas ----------
# ---------- Mostrar ejercicios en tarjetas ----------
API_URL = "https://quadcodex-team-back.onrender.com/update"  # ajusta si usas otro host

for i, exercise in enumerate(recs):

    container_rec = st.container(
        key=f"rec_container_{i}",
        vertical_alignment="center",
        border=True
    )

    with container_rec:
        cols = st.columns([1, 3, 1, 1, 2], vertical_alignment="center")

        with cols[0]:
            img_url = get_muscle_image(exercise["muscles"])
            st.image(img_url, width=80)

        with cols[1]:
            st.markdown(f"### {exercise['Exercise_Name']}")
            st.markdown(f"**Muscles:** {', '.join(exercise['muscles'])}")

        with cols[2]:
            st.markdown(f"**Level:** {exercise['Level']}")
            st.markdown(f"**Equipment:** {exercise['Equipment']}")

        with cols[3]:
            st.markdown(f"**Rating:** {min(exercise['rating_score'], 10.0):.1f}/10")

        with cols[4]:
            col_slider, col_button = st.columns([2, 1], vertical_alignment="center")

            with col_slider:
                rating_value = st.slider(
                    "Your rating",
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    value=0.0,
                    key=f"slider_{i}"
                )
                if st.button("Send ⭐", key=f"send_{i}"):

                    payload = {
                        "id_usuario": st.session_state["id_usuario"],
                        "genero": user["genero"],
                        "edad": user["edad"],
                        "peso": user["peso"],
                        "altura": user["altura"],
                        "id_ejercicio": exercise["id_ejercicio"],
                        "valoracion": rating_value
                    }




                    try:
                        response = requests.post(API_URL, json=payload, timeout=5)

                        if response.status_code == 200:
                            st.success("✅ Rating sent successfully")
                        else:
                            st.error(f"❌ Error: {response.json().get('mensaje','Unknown error')}")

                    except Exception as e:
                        st.error(f"❌ API connection error: {str(e)}")
