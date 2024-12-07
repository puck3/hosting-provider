import streamlit as st
from src.components.public.plans_table import plans_table
from src.db.connector import get_services_factory


def show_plans_page():
    services_factory = get_services_factory()
    plan_service = services_factory.get_plan_service()

    st.title("Актуальные тарифы")

    # Выбор страны
    country = st.selectbox("Выберите страну", ["Россия", "США", "Германия", "Япония"])

    if country:
        plans = plan_service.get_available_plans_by_country(country)

        if plans:
            plans_table(plans, country)
        else:
            st.warning("Нет доступных тарифов для выбранной страны.")
