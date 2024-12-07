import streamlit as st

from src.db.connector import initialize_services_factory
from src.models.user import Role
from src.pages.auth import show_auth_page
from src.pages.profile import show_profile_page
from src.pages.plans import show_plans_page
from src.pages.rentals import show_rentals
from src.pages.admin_panel.admin_panel import show_admin_panel


def main():
    if "factory_init" not in st.session_state:
        initialize_services_factory()
        st.session_state["factory_init"] = True

    st.set_page_config(page_title="Сервис аренды серверов", layout="centered")
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
        st.session_state["role"] = None

    if st.session_state["user_id"] is None:
        show_auth_page()
    else:
        st.sidebar.title("Навигация")

        options = ["Тарифы", "Аренда", "Профиль"]
        if st.session_state["role"] == Role.admin:
            options += ["Администрирование"]

        page = st.sidebar.radio(
            "Выберите страницу",
            options=options,
        )
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
