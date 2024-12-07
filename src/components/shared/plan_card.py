import streamlit as st

from src.components.shared.hardware_card import hardware_card
from src.models.plan import Plan


def plan_card(plan: Plan):
    st.subheader(plan.plan_name)
    hardware_card(plan.hardware)
    st.write(f"**Стоимость тарифа:** ${plan.price} / {plan.billing_period.value}")
