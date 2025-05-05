import streamlit as st
from src.pages.admin_panel.manage_plans import manage_plans
from src.pages.admin_panel.manage_users import manage_users
from src.pages.admin_panel.manage_servers import manage_servers


def show_admin_panel():
    st.title("Панель администратора")
    admin_options = {
        "Управление серверами": manage_servers,
        "Управление тарифами": manage_plans,
        "Упрваление пользователями": manage_users,
    }

    option = st.sidebar.selectbox("Выберите раздел", list(admin_options.keys()))
    admin_options[option]()
