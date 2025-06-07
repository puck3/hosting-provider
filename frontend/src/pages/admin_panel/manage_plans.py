import streamlit as st

from src.components.admin.plans_management import admin_plans_table, create_plan_form
from src.services.services_factory import ServicesFactory


def manage_plans():
    services_factory = ServicesFactory()

    hardware_service = services_factory.get_hardware_service()
    hardwares = hardware_service.get_hardwares()

    plan_service = services_factory.get_plan_service()
    plans = plan_service.get_plans()

    st.subheader("Добавить тариф")
    create_plan_form(hardwares)
    st.subheader("Список тарифов")
    if plans:
        admin_plans_table(plans)
    else:
        st.warning("Нет тарифов")
