import streamlit as st

from src.components.public.user_profile import edit_profile_form, show_profile
from src.utils.app_session import AppSession
from src.services.services_factory import ServicesFactory


def show_profile_page():
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Вы не авторизованы")
        return

    st.title("Профиль пользователя")
    tabs = st.tabs(["Информация о пользователе", "Редактировать профиль"])

    with tabs[0]:
        services = ServicesFactory()
        user_service = services.get_user_service()
        user = user_service.get_user_by_id(user_id)
        if not user:
            st.error("Пользователь не найден")
            return

        st.subheader("Информация о пользователе")
        show_profile(user)

        st.subheader("Удалить аккаунт")
        password = st.text_input("Введите пароль", type="password")
        if st.button("Удалить аккаунт"):
            try:
                user_service.delete_user(user_id, password)
                AppSession.clear()
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    with tabs[1]:
        st.subheader("Редактировать данные")
        edit_profile_form()
