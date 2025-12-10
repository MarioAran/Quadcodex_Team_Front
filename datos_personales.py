import streamlit as st
import requests
import time
import threading
from datetime import date

st.set_page_config(page_title="AlgoFit", layout="centered")

hide_menu_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="expandedSidebar"] {display: none !important;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

class Usuario_datos:
    def __init__(self, nombre, apellido, edad, genero, altura, peso, objetivo, nivel):
        self.Nombre = nombre
        self.Apellido = apellido
        self.Edad = edad
        self.Genero = genero
        self.Altura = altura
        self.Peso = peso
        self.Objetivo = objetivo
        self.Nivel = nivel

class Gestor_Usuario:
    def get_usuario(self, nombre_completo, edad, genero, altura, peso, objetivo, nivel):
        nombre, apellido = self.verif_nombre(nombre_completo)
        return Usuario_datos(
            nombre=nombre,
            apellido=apellido,
            edad=self.verif_edad(edad),
            genero=self.verif_genero(genero),
            altura=self.verif_altura(altura),
            peso=self.verif_peso(peso),
            objetivo=self.verif_objetivo(objetivo),
            nivel=self.verif_nivel(nivel)
        )

    def verif_nombre(self, nombre_completo):
        partes = nombre_completo.strip().split()
        nombre = partes[0] if partes else ""
        apellido = " ".join(partes[1:]) if len(partes) > 1 else ""
        return nombre, apellido

    def verif_edad(self, edad):
        return max(12, min(edad, 80))

    def verif_genero(self, genero):
        return genero if genero in ["Male", "Female"] else "Other"

    def verif_altura(self, altura):
        return max(100, min(altura, 270))

    def verif_peso(self, peso):
        return max(30, min(peso, 300))

    def verif_objetivo(self, objetivo):
        objetivo = objetivo.lower()
        if "gain" in objetivo:
            return "Gain muscle"
        if "lose" in objetivo:
            return "Lose weight"
        return "Unknown"

    def verif_nivel(self, nivel):
        return nivel.split("(")[0].strip()

def keep_server_alive(payload):
    while True:
        try:
            requests.get("https://quadcodex-team-back.onrender.com/health", json=payload)
        except Exception as e:
            print("Error keeping server alive:", e)
        time.sleep(30)

# ---------- Botón volver ----------
if st.button("⬅ Back to Main Menu"):
    st.switch_page("pages/training_recommend.py")

st.title("Sign up and join our community!")
st.markdown("Fill your personal information below.")

gestor = Gestor_Usuario()
u = st.session_state.get("usuario", None)  # Usuario previo si existe

# ---------------------------
# Formulario con autorelleno
# ---------------------------
with st.form("perfil_gym_form"):

    st.header("Personal Data")
    col1, col2 = st.columns(2)

    with col1:
        nombre_completo = st.text_input(
            "Full name",
            value=f"{u.Nombre} {u.Apellido}" if u else ""
        )

        genero_opciones = ["Select your gender", "Male", "Female"]
        genero_value = u.Genero if u and u.Genero in genero_opciones else "Select your gender"
        genero = st.selectbox("Gender", genero_opciones, index=genero_opciones.index(genero_value))

        actual_date = date.today()

    with col2:
        edad = st.number_input(
            "Age", min_value=0, max_value=80, step=1,
            value=u.Edad if u else 0
        )

        altura_cm = st.number_input(
            "Height (cm)", min_value=0, max_value=270, step=1,
            value=u.Altura if u else 0
        )

        peso_kg = st.number_input(
            "Weight (kg)", min_value=0.0, max_value=300.0, format="%.1f",
            value=float(u.Peso) if u else 0.0
        )

    st.header("Physical info and goals")

    objetivo_opciones = ["Select an objective", "Gain muscle/weight", "Lose weight"]
    if u:
        if "gain" in u.Objetivo.lower():
            objetivo_value = "Gain muscle/weight"
        elif "lose" in u.Objetivo.lower():
            objetivo_value = "Lose weight"
        else:
            objetivo_value = "Select an objective"
    else:
        objetivo_value = "Select an objective"
    objetivo = st.selectbox("Objective", objetivo_opciones, index=objetivo_opciones.index(objetivo_value))

    experiencia_opciones = ["Select your gym experience", "Beginner (0-6 months)", "Intermediate (6-12 months)", "Expert (>12 months)"]
    if u:
        n = u.Nivel.lower()
        if "beginner" in n:
            experiencia_value = "Beginner (0-6 months)"
        elif "intermediate" in n:
            experiencia_value = "Intermediate (6-12 months)"
        elif "expert" in n:
            experiencia_value = "Expert (>12 months)"
        else:
            experiencia_value = "Select your gym experience"
    else:
        experiencia_value = "Select your gym experience"

    experiencia = st.selectbox("Gym experience", experiencia_opciones, index=experiencia_opciones.index(experiencia_value))

    enviar = st.form_submit_button("Send")


# ---------------------------
# Validación y envío
# ---------------------------
if enviar:
    errores = []

    if nombre_completo.strip() == "":
        errores.append("Name is mandatory.")
    if genero == "Select your gender":
        errores.append("You must select a gender.")
    if objetivo == "Select an objective":
        errores.append("You must select an objective.")
    if experiencia == "Select your gym experience":
        errores.append("You must select a gym experience.")

    if not (14 <= edad <= 80):
        errores.append("Age must be between 14 and 80.")
    if not (100 <= altura_cm <= 270):
        errores.append("Height must be between 100 and 270 cm.")
    if not (50 <= peso_kg <= 300):
        errores.append("Weight must be between 30 and 300 kg.")

    if errores:
        st.error("Fix these errors:")
        for e in errores:
            st.write("❌ " + e)
    else:
        usuario = gestor.get_usuario(
            nombre_completo, edad, genero, altura_cm, peso_kg, objetivo, experiencia
        )
        st.session_state["usuario"] = usuario

        payload = {
            "nombre": usuario.Nombre,
            "genero": usuario.Genero.lower(),
            "edad": usuario.Edad,
            "peso": usuario.Peso,
            "altura": usuario.Altura,
            "nivel": usuario.Nivel,
            "cantidad": 10
        }

        if "server_pinger_started" not in st.session_state:
            thread = threading.Thread(target=keep_server_alive, args=(payload,), daemon=True)
            thread.start()
            st.session_state["server_pinger_started"] = True

        try:
            resp = requests.post("https://quadcodex-team-back.onrender.com/recomendar", json=payload)
            if resp.status_code == 200:
                st.session_state["recomendaciones"] = resp.json()
                st.switch_page("pages/training_recommend.py")
            else:
                st.error(f"API error {resp.status_code}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
