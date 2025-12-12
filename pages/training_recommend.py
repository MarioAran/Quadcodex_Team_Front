import streamlit as st
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
    "abs": "https://via.placeholder.com/80x80.png?text=ABS",
    "legs": "https://via.placeholder.com/80x80.png?text=LEGS",
    "chest": "https://via.placeholder.com/80x80.png?text=CHEST",
    "back": "https://via.placeholder.com/80x80.png?text=BACK",
    "shoulders": "https://via.placeholder.com/80x80.png?text=SHOULDERS",
    "biceps": "https://via.placeholder.com/80x80.png?text=BICEPS",
    "triceps": "https://via.placeholder.com/80x80.png?text=TRICEPS",
    "glutes": "https://via.placeholder.com/80x80.png?text=GLUTES",
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

st.set_page_config(page_title="Training Plan", layout="wide")

hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""

st.markdown(hide_menu_style, unsafe_allow_html=True)

# ---------- Botón volver ----------
if st.button("⬅ Back to Main Page"):
    st.switch_page("pages/menu.py")

# ---------- Datos ----------
if "recomendaciones" not in st.session_state:
    st.error("❌ No data received. Please complete your profile first.")
    st.stop()

data = st.session_state["recomendaciones"]
user = data.get("user_data", {})
recs = data.get("recomendaciones", [])

# ---------- INVERTIR EL ORDEN ----------
recs = recs[::-1]

st.title("🏋️‍♂️ Your Personalized Training Plan")

usuario = st.session_state["usuario"]
st.markdown(f"**User:** {usuario.Nombre} {usuario.Apellido} | **Gender:** {usuario.Genero} | Age: {usuario.Edad} | Height: {usuario.Altura} cm | Weight: {usuario.Peso} kg")
st.markdown(f"**Level:** {usuario.Nivel} | **Exercises Recommended:** {len(st.session_state.get('recomendaciones', {}).get('recomendaciones', []))}")
    
st.write("---")

# ---------- Mostrar ejercicios en tarjetas ----------
for i, exercise in enumerate(recs):

    cols = st.columns([1.5, 3, 2, 2, 2])  # Ajusta ancho de columnas

    # --- Columna imagen ---
    with cols[0]:
        img_url = get_muscle_image(exercise["muscles"])
        st.image(img_url, width=80)

    # --- Nombre del ejercicio y músculos ---
    with cols[1]:
        st.markdown(f"### {exercise['Exercise_Name']}")
        st.markdown(f"**Muscles:** {', '.join(exercise['muscles'])}")

    # --- Level y Equipment ---
    with cols[2]:
        st.markdown(f"**Level:** {exercise['Level']}")
        st.markdown(f"**Equipment:** {exercise['Equipment']}")

    # --- Rating ---
    with cols[3]:
        st.markdown(f"**Rating:** {min(exercise['rating_score'], 10.0):.1f}/10")

    # --- Slider para final_score ---
    with cols[4]:
        #slider_value = int(min(exercise['final_score'], 1.0) * 10)
        st.slider("How much did you like the exercise?", min_value=0.0, max_value=10.0, step=0.1, value=0.0, key=f"slider_{i}")

    st.write("---")
