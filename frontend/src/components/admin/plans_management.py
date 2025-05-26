import streamlit as st

from src.components.shared.plan_card import plan_card
from src.db.connector import get_services_factory
from src.models.hardware import Hardware
from src.models.plan import BillingPeriod, Plan
from src.utils.key_id_map import HardwareKeyIdMap


def create_plan_form(hardwares: list[Hardware]):
    hardware_mapper = HardwareKeyIdMap(hardwares)

    plan_name = st.text_input("Введите название тарифа")

    hardware_info = st.selectbox(
        "Выберите конфигурацию серверов", hardware_mapper.list_keys()
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        price = st.number_input("Введите цену", min_value=1.0)

    with col2:
        billing_period = st.selectbox(
            "Выберите срок аренды", [e.value for e in BillingPeriod]
        )

    if st.button("Добавить тариф"):
        services = get_services_factory()
        plan_service = services.get_plan_service()
        try:
            plan_service.add_plan(
                hardware_id=hardware_mapper.get(hardware_info),
                price=price,
                billing_period=billing_period,
                plan_name=plan_name,
            )
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def admin_plans_table(plans: list[Plan]):
    st.markdown("---")
    for plan in plans:
        col1, col2, col3 = st.columns([1, 8, 2])
        with col1:
            st.write(str(plan.plan_id))

        with col2:
            plan_card(plan)

        with col3:
            if st.button("Удалить", key=f"delete_{plan.plan_name}"):
                services = get_services_factory()
                plan_service = services.get_plan_service()
                try:
                    plan_service.delete_plan(plan.plan_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")
