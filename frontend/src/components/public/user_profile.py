import streamlit as st

from src.db.connector import get_services_factory
from src.models.user import User


def show_profile(user: User):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("**Email:**")
        st.write("**Логин:**")
        st.write("**Имя:**")
        st.write("**Фамилия:**")
        st.write("**Дата рождения:**")
    with col2:
        st.write(f"{user.email}")
        st.write(f"{user.login}")
        st.write(f"{user.first_name if user.first_name else ''}")
        st.write(f"{user.last_name if user.last_name else ''}")
        st.write(f"{user.birthdate if user.birthdate else ''}")


def edit_profile_form():
    new_email = st.text_input("Новый email", value=None)
    new_login = st.text_input("Новый логин", value=None)
    new_password = st.text_input("Новый пароль", type="password", value=None)
    new_first_name = st.text_input("Новое имя", value=None)
    new_last_name = st.text_input("Новая фамилия", value=None)
    new_birthdate = st.date_input("Новая дата рождения", value=None)

    if new_email or new_login or new_password:
        password = st.text_input("Введите пароль*", type="password")

    if st.button("Сохранить изменения"):
        services = get_services_factory()
        user_service = services.get_user_service()
        user_id = st.session_state["user_id"]
        try:
            if new_email:
                user_service.change_user_email(user_id, password, new_email)
            if new_login:
                user_service.change_user_login(user_id, password, new_login)
            if new_password:
                user_service.change_user_password(user_id, password, new_password)
            if new_first_name or new_last_name or new_birthdate:
                user_service.change_user_personal(
                    user_id, new_first_name, new_last_name, new_birthdate
                )
            st.rerun()
        except ValueError as e:
            st.error(str(e))
