import streamlit as st

from src.components.shared.rental_card import rental_card


def admin_rentals_table(rentals):
    st.markdown("---")
    for rental in rentals:
        col1, col2 = st.columns([1, 8])
        with col1:
            st.write(str(rental.rental_id))
        with col2:
            st.write(f"**Арендатор:** {rental.user.login}")
            st.write(f"**Email**: {rental.user.email}")

            st.write("**Информация об аренде:**")
            rental_card(rental)

        st.markdown("---")


def show_user_rentals(user_rentals):
    for rental in user_rentals:
        col1, col2 = st.columns([1, 9])
        with col1:
            st.write(str(rental.rental_id))
        with col2:
            rental_card(rental)
        st.write("")
        st.write("")
