import streamlit as st

st.set_page_config(page_title="Training Plan", layout="wide")

# ---------- Datos ----------
if "recomendaciones" not in st.session_state:
    st.error("❌ No data received. Please complete your profile first.")
    st.stop()

data = st.session_state["recomendaciones"]
user = data.get("user_data", {})
recs = data.get("recomendaciones", [])

st.title("🏋️‍♂️ Your Personalized Training Plan")
st.markdown(f"**User:** {user.get('genero','')} | Age: {user.get('edad','')} | Height: {user.get('altura','')} cm | Weight: {user.get('peso','')} kg")
st.markdown(f"**Level:** {data.get('nivel','')} | **Exercises Recommended:** {data.get('cantidad_recomendaciones',0)}")

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
        st.markdown(f"**Rating:** {exercise['rating_score']}/10")
    with cols[4]:
        st.progress(min(exercise['final_score'],1.0))  # barra para final_score

    st.write("---")

# ---------- Botón volver ----------
if st.button("⬅ Back to Main Page"):
    st.switch_page("app.py")
