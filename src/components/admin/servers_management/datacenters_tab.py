import streamlit as st

from src.components.shared.datacenter_card import datacenter_card
from src.db.connector import get_services_factory
from src.models.server import Datacenter


def create_datacenter_form():
    datacenter_name = st.text_input("Название датацентра")
    col1, col2 = st.columns([1, 1])
    with col1:
        country = st.text_input("Страна")
    with col2:
        city = st.text_input("Город")
    if st.button("Добавить датацентр"):
        services = get_services_factory()
        server_service = services.get_server_service()
        try:
            server_service.add_datacenter(datacenter_name, country, city)
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def datacenters_table(datacenters: list[Datacenter]):
    st.markdown("---")
    for datacenter in datacenters:
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
            st.write(f"{datacenter.datacenter_id}")

        with col2:
            datacenter_card(datacenter)

        with col3:
            if st.button("Удалить", key=datacenter.datacenter_name):
                services = get_services_factory()
                server_service = services.get_server_service()
                try:
                    server_service.delete_datacenter(datacenter.datacenter_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")


def manage_datacenters_tab(datacenters: list[Datacenter]):
    st.subheader("Добавить датацентр")
    create_datacenter_form()

    st.subheader("Список датацентров")
    if datacenters:
        datacenters_table(datacenters)
    else:
        st.warning("Нет датацентров")
