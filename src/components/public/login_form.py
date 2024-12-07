import streamlit as st

from src.db.connector import get_services_factory


def login_form():
    login = st.text_input("Логин", key="login_input")
    password = st.text_input("Пароль", type="password", key="password_input")
    if st.button("Войти"):
        services_factory = get_services_factory()
        user_service = services_factory.get_user_service()
        try:
            user = user_service.login_user(login, password)
            st.success("Авторизация успешна!")
            st.session_state["user_id"] = user.user_id
            st.session_state["role"] = user.role
            st.rerun()
        except ValueError as e:
            st.error(str(e))
