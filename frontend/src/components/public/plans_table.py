import streamlit as st

from src.components.shared.plan_card import plan_card
from src.models.plan import Plan
from src.services.services_factory import ServicesFactory


def plans_table(plans: list[Plan], country):
    st.markdown("---")
    for plan in plans:
        plan_card(plan)

        if st.button("Оформить аренду", key=f"rent_{plan.plan_name}"):
            try:
                services = ServicesFactory()
                rental_service = services.get_rental_service()
                rental_service.create_rental(
                    plan_id=plan.plan_id,
                    country=country,
                )
                st.success("Сервер успешно арендован!")
            except ValueError as e:
                st.error(str(e))

        st.markdown("---")
