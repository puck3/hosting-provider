import streamlit as st
from src.components.public.plans_table import plans_table
from src.services.services_factory import ServicesFactory


def show_plans_page():
    services_factory = ServicesFactory()
    plan_service = services_factory.get_plan_service()
    server_service = services_factory.get_server_service()

    st.title("Актуальные тарифы")

    countries = server_service.get_countries()
    country = st.selectbox("Выберите страну", countries)

    if country:
        plans = plan_service.get_available_plans_by_country(country)

        if plans:
            plans_table(plans, country)
        else:
            st.warning("Нет доступных тарифов для выбранной страны.")
