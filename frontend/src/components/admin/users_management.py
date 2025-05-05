import streamlit as st

from src.components.admin.rentals_management import show_user_rentals
from src.components.shared.user_card import user_card
from src.db.connector import get_services_factory
from src.models.user import Role, User


def change_user_role_form():
    email = st.text_input("Введите email пользователя")
    role = st.selectbox("Выберите роль", [e.value for e in Role])
    if st.button("Изменить роль"):
        services = get_services_factory()
        user_service = services.get_user_service()
        try:
            user_service.change_user_role_by_email(email, role)
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def users_table(users: list[User]):
    st.markdown("---")

    for user in users:
        col1, col2 = st.columns([1, 9])

        with col1:
            st.write(str(user.user_id))

        with col2:
            user_card(user)

        key = f"rentals_{user.login}"

        if st.button(
            "Показать историю аренды" if key not in st.session_state else "Скрыть",
            key=user.login,
        ):
            if key not in st.session_state:
                st.session_state[key] = True
                st.rerun()
            else:
                del st.session_state[key]
                st.rerun()

        if key in st.session_state:
            services = get_services_factory()
            rental_service = services.get_rental_service()
            user_rentals = rental_service.get_rentals_by_user(user.user_id)
            if user_rentals:
                show_user_rentals(user_rentals)
            else:
                st.warning("У пользователя нет арендованных серверов")

        st.markdown("---")


def manage_users_tab(users: list[User]):
    st.subheader("Изменить роль пользователя")
    change_user_role_form()

    st.subheader("Список пользователей")
    if users:
        users_table(users)
    else:
        st.warning("Нет зарегистрированнх пользователей")
