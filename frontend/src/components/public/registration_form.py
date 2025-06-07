import streamlit as st


from src.services.services_factory import ServicesFactory
from src.utils.client import Client


def registration_form():
    email = st.text_input("Электронная почта*")
    login = st.text_input("Логин*")
    password = st.text_input("Пароль*", type="password")
    first_name = st.text_input("Имя", value=None)
    last_name = st.text_input("Фамилия", value=None)
    birthdate = st.date_input("Дата рождения", value=None)

    if st.button("Зарегистрироваться"):
        services_factory = ServicesFactory()
        user_service = services_factory.get_user_service()
        client = Client()
        try:
            user = user_service.create_user(email, login, password, first_name, last_name, birthdate)
            client.login(login, password)
            st.success("Регистрация успешна!")
            st.session_state["user_id"] = user.user_id
            st.session_state["role"] = user.role
            st.rerun()

        except ValueError as e:
            st.error(str(e))
