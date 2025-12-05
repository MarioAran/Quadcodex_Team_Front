import streamlit as st
import re
from datetime import date

st.set_page_config(page_title="Datos Personales", layout="centered")

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
        edad = self.verif_edad(edad)
        genero = self.verif_genero(genero)
        altura = self.verif_altura(altura)
        peso = self.verif_peso(peso)
        objetivo = self.verif_objetivo(objetivo)
        nivel = self.verif_nivel(nivel)

        return Usuario_datos(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            genero=genero,
            altura=altura,
            peso=peso,
            objetivo=objetivo,
            nivel=nivel
        )

# Verificación para todos los datos.
    def verif_nombre(self, nombre_completo):
        partes = nombre_completo.strip().split()
        if len(partes) == 0:
            return ("", "")
        nombre = partes[0]
        apellido = " ".join(partes[1:]) if len(partes) > 1 else ""
        return (nombre, apellido)

    def verif_edad(self, edad):
        return max(12, min(edad, 80))

    def verif_genero(self, genero):
        if genero in ["Male", "Female"]:
            return genero
        return "Other"

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

st.markdown("""
<style>
    .card {
        background: linear-gradient(180deg, #a1d6e2, #a1d6e2);
        border-radius: 12px;
        padding: 18px;
        color: #e6f6ff;
        box-shadow: 0 6px 18px rgba(0,0,0,0.5);
    }
    .label {
        color: #afd7ff;
        font-weight: 600;
    }
    .metric {
        font-size: 20px;
        font-weight: 700;
        color: #d8f3ff;
    }
    .small {
        color: #bcdff7;
        font-size: 13px;
    }
    .two-col { display:flex; gap:12px; }
    .two-col > div { flex: 1; }
</style>
""", unsafe_allow_html=True)

st.title("Sign up and join our community!")
st.markdown("Fill in your personal details to join our community.")

gestor = Gestor_Usuario()

with st.form("perfil_gym_form", clear_on_submit=False):

    st.header("New Registration")
    col1, col2 = st.columns(2)

    with col1:
        nombre_completo = st.text_input("Full name", max_chars=80)
        genero = st.selectbox("Gender", ["Select your gender","Male", "Female"])

        actual_date = date.today()
        long_date = date(actual_date.year - 80, actual_date.month, actual_date.day)
        fecha_nac = st.date_input(
            "Birth date (required)",
            min_value=long_date,
            max_value=actual_date,
            value=actual_date
        )

    with col2:
        edad = st.number_input("Age", min_value=0, max_value=80, step=1)
        altura_cm = st.number_input("height (cm)", min_value=0, max_value=270, step=5)
        peso_kg = st.number_input("weight (kg)", min_value=0.0, max_value=300.0, format="%.1f", step=5.0)

    st.header("Physical information and objectives")
    objetivo = st.selectbox("Objetive", [
        "Select an objective",
        "Gain muscle/weight",
        "lose weight"
    ])
    experiencia = st.selectbox("Gym experience", [
        "Select your gym experience",
        "Beginner (0-6 months)",
        "Intermediate (6-12 months)",
        "Expert (>12 months)"
    ])

    enviar = st.form_submit_button("Send")

if enviar:
    errores = [] 

    if nombre_completo.strip() == "":
        errores.append("The name is mandatory.")
    elif not re.match(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$", nombre_completo):
        errores.append("The name can only contain letters and spaces (including accents).")

    if genero.strip() == "Select your gender":
        errores.append("You must select a gender.")

    if fecha_nac is None:
        errores.append("You must select a birth date.")
    else:
        hoy = date.today()
        edad_calc = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

    if objetivo.strip() == "Select an objective":
        errores.append("You must select an objective.")
    if experiencia.strip() == "Select your gym experience":
        errores.append("You must select your gym experience.")

    if not (14 <= edad <= 80):
        errores.append("Age must be between 12 and 80.")
    if not (100 <= altura_cm <= 270):
        errores.append("Height must be between 100 and 270 cm.")
    if not (30.0 <= peso_kg <= 300.0):
        errores.append("Weight must be between 30 and 300 kg.")

    if fecha_nac is not None:
        if not (edad == edad_calc or edad == edad_calc + 1):
            errores.append(
                f"Entered age does not match with your birth date. Based on birth you have {edad_calc}-{edad_calc + 1} years old, "
                f"but your entered age is {edad} ."
                "Please correct either the birth date or the age."
            )

    if errores:
        st.error("Please correct the following errors before continuing:")
        for e in errores:
            st.write("❌ " + e)
    else:
        usuario = gestor.get_usuario(
            nombre_completo,
            edad,
            genero,
            altura_cm,
            peso_kg,
            objetivo,
            experiencia
        )

        st.success("Data sent successfully!")

        st.json({
            "Nombre": usuario.Nombre,
            "Apellido": usuario.Apellido,
            "Edad": usuario.Edad,
            "Genero": usuario.Genero,
            "Altura": usuario.Altura,
            "Peso": usuario.Peso,
            "Objetivo": usuario.Objetivo,
            "Nivel": usuario.Nivel
        })

st.info("Fill out the form to join our community!!!")








