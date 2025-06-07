import streamlit as st
from src.services.services_factory import ServicesFactory
from src.utils.client import Client


def login_form():
    login = st.text_input("Логин", key="login_input")
    password = st.text_input("Пароль", type="password", key="password_input")
    if st.button("Войти"):
        client = Client()
        user_service = ServicesFactory.get_user_service()
        try:
            client.login(login, password)
            user = user_service.get_self()
            st.success("Авторизация успешна!")
            st.session_state["user_id"] = user.user_id
            st.session_state["role"] = user.role
            st.rerun()
        except ValueError as e:
            st.error(str(e))
