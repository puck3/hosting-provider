import streamlit as st

from src.components.admin.servers_management.cpus_tab import manage_cpus_tab
from src.components.admin.servers_management.datacenters_tab import (
    manage_datacenters_tab,
)
from src.components.admin.servers_management.gpus_tab import manage_gpus_tab
from src.components.admin.servers_management.hardwares_tab import manage_hardwares_tab
from src.components.admin.servers_management.servers_tab import manage_servers_tab
from src.db.connector import get_services_factory


def manage_servers():
    services_factory = get_services_factory()

    hardware_service = services_factory.get_hardware_service()
    cpus = hardware_service.get_cpus()
    gpus = hardware_service.get_gpus()
    hardwares = hardware_service.get_hardwares()

    server_service = services_factory.get_server_service()
    datacenters = server_service.get_datacenters()
    servers = server_service.get_servers()

    st.header("Управление серверами")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Серверы", "Датацентры", "Конфигурации серверов", "Процессоры", "Видеокарты"]
    )

    with tab1:
        manage_servers_tab(datacenters, hardwares, servers)
    with tab2:
        manage_datacenters_tab(datacenters)
    with tab3:
        manage_hardwares_tab(cpus, gpus, hardwares)
    with tab4:
        manage_cpus_tab(cpus)
    with tab5:
        manage_gpus_tab(gpus)
