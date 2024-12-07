import streamlit as st

from src.db.connector import get_services_factory


def registration_form():
    email = st.text_input("Электронная почта*")
    login = st.text_input("Логин*")
    password = st.text_input("Пароль*", type="password")
    first_name = st.text_input("Имя", value=None)
    last_name = st.text_input("Фамилия", value=None)
    birthdate = st.date_input("Дата рождения", value=None)

    if st.button("Зарегистрироваться"):
        services_factory = get_services_factory()
        user_service = services_factory.get_user_service()
        try:
            user = user_service.register_user(
                email, login, password, first_name, last_name, birthdate
            )
            st.success("Регистрация успешна!")
            st.session_state["user_id"] = user.user_id
            st.session_state["role"] = user.role
            st.rerun()

        except ValueError as e:
            st.error(str(e))
