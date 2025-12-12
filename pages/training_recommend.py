import streamlit as st

st.set_page_config(page_title="Training Plan", layout="wide")

hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""

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

# ---------- Botón volver ----------
if st.button("⬅ Back to Main Menu"):
    st.switch_page("pages/menu.py")

# ---------- Datos ----------
if "recomendaciones" not in st.session_state:
    st.error("❌ No data received. Please complete your profile first.")
    st.stop()

data = st.session_state["recomendaciones"]
user = data.get("user_data", {})
recs = data.get("recomendaciones", [])

st.title("🏋️‍♂️ Your Personalized Training Plan")

usuario = st.session_state["usuario"]
st.markdown(f"**User:** {usuario.Nombre} {usuario.Apellido} | **Gender:** {usuario.Genero} | Age: {usuario.Edad} | Height: {usuario.Altura} cm | Weight: {usuario.Peso} kg")
st.markdown(f"**Level:** {usuario.Nivel} | **Exercises Recommended:** {len(st.session_state.get('recomendaciones', {}).get('recomendaciones', []))}")
    
st.write("---")

# ---------- Mostrar ejercicios en tarjetas ----------
for i, exercise in enumerate(recs):
    cols = st.columns([1,3,2,2,2])  # Ajusta ancho de columnas
    with cols[0]:
        st.markdown(f"**{i+1}**")
    with cols[1]:
        st.markdown(f"### {exercise['Exercise_Name']}")
        st.markdown(f"**Muscles:** {', '.join(exercise['muscles'])}")
    with cols[2]:
        st.markdown(f"**Level:** {exercise['Level']}")
        st.markdown(f"**Equipment:** {exercise['Equipment']}")
    with cols[3]:
        st.markdown(f"**Rating:** {min(exercise['rating_score'], 10.0):.1f}/10")
    with cols[4]:
        st.progress(min(exercise['final_score'],1.0))  # barra para final_score

    st.write("---")
