import streamlit as st
import re
import requests
from datetime import date
from colores import Colores_class

st.set_page_config(page_title="AlgoFit", layout="centered")
colores = Colores_class()

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

st.markdown(f"""
    <style>
        /* Fondo general */
        .stApp {{
            background-color: {colores.get_fondo_general()};
        }}

        .block-container {{
            margin-top: 50px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: {colores.get_cajas_principales()}; /* azul claro semi-transparente */
            border-radius: 15px;
        }}

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

            /* =============================
        LABELS (títulos de inputs)
        ============================== */
        label {{
            font-weight: 600 !important;
            color: {colores.get_fondo_general()} !important;
            font-size: 18px !important;
        }}

        /* =============================
        CONTENEDORES DE INPUTS
        ============================== */
        .stTextInput, .stNumberInput, .stSelectbox {{
            background-color: {colores.get_cajas_terciarias()};
            padding: 10px 12px 5px 12px;
            border-radius: 10px;
            border: 2px solid {colores.get_botones_2()};
        }}

        /* =============================
        INPUTS DE TEXTO Y NÚMEROS
        ============================== */
        input {{
            background-color: {colores.get_botones_2()};
            padding: 8px 10px !important;
        }}

        input:focus {{
            border-color: {colores.get_botones_1()} !important;
            background-color: {colores.get_botones_2};
        }}


        /* ==========================================
       SELECTBOX (Caja principal cerrada)
        ========================================== */
        div[data-baseweb="select"] > div {{
            background-color: {colores.get_botones_2()} !important;
            border: 2px solid {colores.get_botones_1()} !important;
            border-radius: 6px !important;
            color: black !important;
            transition: 0.2s ease-in-out;
        }}

        /* Focus borde */
        div[data-baseweb="select"]:focus-within {{
            border: 3px solid white !important;
            border-radius: 6px !important;
            box-shadow: none !important;
        }}

        /* Hover */
        div[data-baseweb="select"]:hover {{
            border-color: white !important;
        }}

        /* =============================
        DROPDOWN DEL SELECTBOX
        ============================== */
        ul[role="listbox"] {{
            background-color: {colores.get_botones_2()};
            border-radius: 6px;
            border: 1px solid {colores.get_botones_1()};
        }}


        li[role="option"]:hover {{
            background-color: white !important;
            color: black !important;
        }}

        /* =============================
        SELECTBOX (real background)
        ============================= */
        div[data-baseweb="select"] > div {{
            background-color: {colores.get_botones_2()} !important;
            border: 2px solid {colores.get_botones_1()} !important;
            border-radius: 6px !important;
        }}

        /* Dropdown */
        div[role="listbox"] ul {{
            background-color: {colores.get_botones_2()} !important;
            border-radius: 6px;
        }}

        /* =============================
        NUMBER INPUT (real background)
        ============================= */
        div[data-baseweb="input"] > div {{
            background-color: {colores.get_botones_2()} !important;
            border: 3px solid {colores.get_botones_1()} !important;
            border-radius: 6px !important;
        }}
'
        /* Input real */
        div[data-testid="stNumberInput"] input {{
            background-color: {colores.get_botones_2()} !important;
            color: black !important;
        }}

        /* Botones + y - */
        div[data-testid="stNumberInput"] button {{
            background-color: {colores.get_botones_1()} !important;
            color: white !important;
            border-left: 1px solid {colores.get_botones_1()} !important;
        }}

        /* Hover botones */
        div[data-testid="stNumberInput"] button:hover {{
            background-color: {colores.get_botones_2()} !important;
            color: black !important;
        }}

        /* =============================
        INPUT DE TEXTO (nombre) – estilo como selectbox
        ============================= */
        div[data-baseweb="input"] > div input[type="text"]:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT DE TEXTO (nombre) – estilo como selectbox
        ============================= */
        div[data-baseweb="input"] > div input[type="text"]:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT NUMÉRICO – borde al foco
        ============================= */
        div[data-testid="stNumberInput"] input:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT DE TEXTO – borde al foco
        ============================= */
        div[data-baseweb="input"] > div input[type="text"]:focus {{
            border: 3px solid white !important;
            box-shadow: none !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT NUMÉRICO – borde al foco
        ============================= */
        div[data-testid="stNumberInput"] input:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        SELECTBOX – borde al foco
        ============================= */
        div[data-baseweb="select"]:focus-within {{
            border: 3px solid white !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT DE TEXTO – borde al foco
        ============================= */
        div[data-baseweb="input"] > div input[type="text"]:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        INPUT NUMÉRICO – borde al foco
        ============================= */
        div[data-testid="stNumberInput"] input:focus {{
            border: 3px solid white !important;
            outline: none !important;
            border-radius: 6px !important;
        }}

        /* =============================
        SELECTBOX – borde al foco
        ============================= */
        div[data-baseweb="select"]:focus-within {{
            border: 3px solid white !important;
            border-radius: 6px !important;
        }}
        </style>
""", unsafe_allow_html=True)

css = f"""
<style>
    [data-testid="stForm"] {{
        background-color: {colores.get_cajas_secundarias()};
    }}
</style>
"""

st.write(css, unsafe_allow_html=True)
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ==============================
#  DATOS DEL LOGIN
# ==============================
usuario_api = st.session_state.get("user", {})

nombre_api = usuario_api.get("nombre", "")
apellido_api = usuario_api.get("apellido", "")
dni_api = usuario_api.get("dni", "")
id_user_api = usuario_api.get("id_user", None)
genero_api = usuario_api.get("genero", "")
edad_api = usuario_api.get("edad", "")
altura_api = usuario_api.get("altura", "")
peso_api = usuario_api.get("peso", "")


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
        return max(18, min(edad, 80))

    def verif_genero(self, genero):
        return genero if genero in ["male", "female"] else "Other"

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


# ==========================
#   INTERFAZ STREAMLIT
# ==========================

if st.button("⬅ Back to Main Menu"):
    st.switch_page("pages/menu.py")

st.title("Sign up and join our community!")
st.markdown("Fill your personal information below.")

gestor = Gestor_Usuario()

with st.form("perfil_gym_form"):
    st.header("Personal Data")
    col1, col2 = st.columns(2)

    with col1:
        # Prellenado de nombre
        nombre_completo = st.text_input(
            "Full name",
            value=f"{nombre_api} {apellido_api}".strip()
        )

        genero = st.selectbox(
            "Gender",
            ["male", "female"],
            index=(
                1 if genero_api == "male" else
                2 if genero_api == "female" else
                0
            )
        )

        num_default = 6
        cantidad = st.selectbox(
            "Number of exercises",
            list(range(1, 11)),  # genera la lista [1, 2, ..., 10]
            index=(num_default - 1)  # index empieza en 0, por eso restamos 1
        )

    with col2:
        edad = st.number_input(
            "Age",
            min_value=12,
            max_value=80,
            step=1,
            value=int(edad_api) if str(edad_api).isdigit() else 18
        )

        altura_cm = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=270,
            step=1,
            value=int(altura_api) if str(altura_api).isdigit() else 170
        )

        peso_kg = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=300.0,
            step=0.1,
            value=float(peso_api) if str(peso_api).replace('.', '').isdigit() else 70.0
        )

    st.header("Physical info and goals")

    objetivo = st.selectbox("Objective", [
        "Select an objective",
        "Gain muscle/weight",
        "Lose weight"
    ])

    experiencia = st.selectbox("Gym experience", [
        "Beginner (0-6 months)",
        "Intermediate (6-12 months)",
        "Expert (>12 months)"
    ])
    
    enviar = st.form_submit_button("Send to recommend")

# ==========================
#  VALIDACIÓN Y ENVÍO
# ==========================

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
            "id_user": id_user_api,
            "nombre": usuario.Nombre,
            "genero": usuario.Genero.lower(),
            "edad": usuario.Edad,
            "peso": usuario.Peso,
            "altura": usuario.Altura,
            "nivel": usuario.Nivel.lower(),
            "cantidad": cantidad
        }

        try:
            resp = requests.post("https://quadcodex-team-back.onrender.com/recomendar", json=payload)

            if resp.status_code == 200:
                st.session_state["recomendaciones"] = resp.json()
                st.switch_page("pages/training_recommend.py")
            else:
                st.error(f"API error {resp.status_code}")

        except Exception as e:
            st.error(f"Could not connect to API: {e}")
