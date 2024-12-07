import streamlit as st

from src.components.shared.datacenter_card import datacenter_card
from src.components.shared.hardware_card import hardware_card
from src.models.server import Server


def server_card(server: Server):
    datacenter_card(server.datacenter)
    hardware_card(server.hardware)
    st.write(f"ОС: {server.operating_system}")
