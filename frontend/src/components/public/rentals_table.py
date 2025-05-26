import streamlit as st

from src.components.shared.rental_card import rental_card
from src.db.connector import get_services_factory
from src.models.rental import Rental


def rentals_table(rentals: list[Rental]):
    st.markdown("---")
    for rental in rentals:
        rental_card(rental)
        st.markdown("---")


def manage_rentals_table(rentals: list[Rental]):
    st.markdown("---")
    for rental in rentals:
        rental_card(rental)
        if st.button("Продлить аренду", key=f"extend_{rental.rental_id}"):
            services_factory = get_services_factory()
            rental_service = services_factory.get_rental_service()
            try:
                rental_service.extend_rental(rental.rental_id)
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        st.markdown("---")
