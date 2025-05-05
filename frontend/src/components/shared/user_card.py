import streamlit as st

from src.models.user import User


def user_card(user: User):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(user.login)
        st.write(user.email)
        st.write(user.role.value)

    with col2:
        st.write(user.first_name if user.first_name else "Имя не указано")
        st.write(user.last_name if user.last_name else "Фамилия не указана")
        st.write(str(user.birthdate) if user.birthdate else "Дата рождения не указана")
