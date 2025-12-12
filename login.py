import streamlit as st
import re
import requests

st.set_page_config(page_title="Página Principal", layout="centered")

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

st.title("Login")
user = st.text_input("Usuario")
pwd = st.text_input("Contraseña", type="password")
if st.button("Login"):
    try:
        payload = {"dni": user}
        resp = requests.post("https://quadcodex-team-back.onrender.com/login", json=payload)
        if resp.status_code == 200:
            data = resp.json()
            st.session_state["user"] = data["usuario"]
            st.switch_page("pages/menu.py")
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")

    except Exception as e:
        st.error(f"Could not connect to API: {e}")