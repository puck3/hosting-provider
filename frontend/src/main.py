import streamlit as st

from src.models.user import Role
from src.pages.auth import show_auth_page
from src.pages.profile import AppSession, show_profile_page
from src.pages.plans import show_plans_page
from src.pages.rentals import show_rentals
from src.pages.admin_panel.admin_panel import show_admin_panel


def main():
    st.set_page_config(page_title="Сервис аренды серверов", layout="centered")

    if not AppSession.is_initialized():
        AppSession.clear()

    if not AppSession.is_authenticated():
        show_auth_page()
        return

    st.sidebar.title("Навигация")
    options = ["Тарифы", "Аренда", "Профиль"]
    if st.session_state["role"] == Role.admin:
        options.append("Администрирование")

    page = st.sidebar.radio("Выберите страницу", options=options)

    match page:
        case "Тарифы":
            show_plans_page()
        case "Аренда":
            show_rentals()
        case "Профиль":
            show_profile_page()
        case "Администрирование":
            if st.session_state["role"] == Role.admin:
                show_admin_panel()
            else:
                st.error("Доступ запрещен")
