import streamlit as st

from src.models.server import Datacenter


def datacenter_card(datacenter: Datacenter):
    st.write(
        f"Датацентр {datacenter.datacenter_name}, {datacenter.country}, {datacenter.city}"
    )
