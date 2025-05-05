import streamlit as st

from src.components.admin.rentals_management import admin_rentals_table
from src.components.admin.users_management import manage_users_tab
from src.db.connector import get_services_factory


def manage_users():
    services_factory = get_services_factory()
    user_service = services_factory.get_user_service()
    rental_service = services_factory.get_rental_service()

    st.subheader("Управление пользователями и арендой")
    users_tab, rentals_tab = st.tabs(
        ["Управление пользователями", "Управление арендой"]
    )

    with users_tab:
        users = user_service.get_users()
        manage_users_tab(users)

    with rentals_tab:
        rentals = rental_service.get_rentals()
        st.subheader("История аренды серверов")
        admin_rentals_table(rentals)
