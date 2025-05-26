import streamlit as st

from src.components.shared.server_card import server_card
from src.models.rental import Rental


def rental_card(rental: Rental):
    server_card(rental.server)
    st.write(f"**Стоимость аренды:** ${rental.price} / {rental.billing_period.value}")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("**Дата начала:**")
        st.write("**Дата продления:**")
        st.write("**Дата окончания:**")
    with col2:
        st.write(f"{rental.start_at:%Y-%m-%d %H:%M}")
        st.write(f"{rental.update_at:%Y-%m-%d %H:%M}")
        st.write(f"{rental.end_at:%Y-%m-%d %H:%M}")
