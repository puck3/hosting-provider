import streamlit as st

from src.components.public.login_form import login_form
from src.components.public.registration_form import registration_form


def show_auth_page():
    tabs = st.tabs(["Вход", "Регистрация"])

    with tabs[0]:
        st.subheader("Вход")
        login_form()
    with tabs[1]:
        st.subheader("Регистрация")
        registration_form()
