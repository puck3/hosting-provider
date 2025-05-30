from datetime import datetime
import streamlit as st

from src.components.public.rentals_table import manage_rentals_table, rentals_table
from src.db.connector import get_services_factory


def show_rentals():
    services_factory = get_services_factory()
    rental_service = services_factory.get_rental_service()

    user_id = st.session_state["user_id"]
    rentals = rental_service.get_rentals_by_user(user_id)
    time = datetime.now()
    current_rentals = [rental for rental in rentals if rental.end_at > time]
    archive_rentals = [rental for rental in rentals if rental.end_at <= time]

    st.header("Информация об арендованных серверах")

    current, archive = st.tabs(["Текущая аренда", "Архив"])

    with current:
        if current_rentals:
            st.subheader("Список арендованных серверов")
            manage_rentals_table(current_rentals)
        else:
            st.subheader("Ранее арендованные серверы")
            st.warning("Нет арендованных серверов")

    with archive:
        if archive_rentals:
            rentals_table(archive_rentals)
        else:
            st.warning("Нет арендованных серверов")
