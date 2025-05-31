import streamlit as st

from src.components.shared.server_card import server_card
from src.models.hardware import Hardware
from src.models.server import Datacenter, Server, Status
from src.pages.plans import ServicesFactory
from src.utils.key_id_map import DatacenterKeyIdMap, HardwareKeyIdMap


def create_server_form(
    datacenters: list[Datacenter],
    hardwares: list[Hardware],
):
    hardware_mapper = HardwareKeyIdMap(hardwares)
    datacenter_mapper = DatacenterKeyIdMap(datacenters)

    datacenter_name = st.selectbox("Выберите датацентр", datacenter_mapper.list_keys())
    hardware_info = st.selectbox("Выберите конфигурацию сервера", hardware_mapper.list_keys())
    col1, col2 = st.columns([3, 1])
    with col1:
        operating_system = st.text_input("Выберите операционную систему")

    with col2:
        status = st.selectbox("Выберите статус сервера", [e.value for e in Status])

    if st.button("Добавить сервер"):
        services = ServicesFactory()
        server_service = services.get_server_service()
        try:
            server_service.create_server(
                datacenter_id=datacenter_mapper.get(datacenter_name),
                hardware_id=hardware_mapper.get(hardware_info),
                status=Status(status),
                operating_system=operating_system,
            )
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def servers_table(servers: list[Server]):
    st.markdown("---")
    for server in servers:
        col1, col2, col3 = st.columns([1, 7, 2])
        with col1:
            st.write(f"{server.server_id}")

        with col2:
            server_card(server)

        with col3:
            new_status = st.selectbox(
                "Изменить статус",
                [e.value for e in Status],
                index=list(Status).index(server.status),
                key=f"{server.server_id}:{server.status}",
                label_visibility="collapsed",
            )
            if new_status != server.status:
                services = ServicesFactory()
                server_service = services.get_server_service()
                try:
                    server_service.change_server_status(server.server_id, Status(new_status))
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

            if st.button("Удалить", key=server.server_id):
                services = ServicesFactory()
                server_service = services.get_server_service()
                try:
                    server_service.delete_server(server.server_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")


def change_status_buttons():
    services = ServicesFactory()
    server_service = services.get_server_service()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Обновить статус неиспользуемых серверов"):
            try:
                server_service.release_servers()
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    with col2:
        if st.button("Обновить статус арендованных серверов"):
            try:
                server_service.fix_servers_status()
                st.rerun()
            except ValueError as e:
                st.error(str(e))


def manage_servers_tab(
    datacenters: list[Datacenter],
    hardwares: list[Hardware],
    servers: list[Server],
):
    st.subheader("Добавить сервер")
    create_server_form(datacenters, hardwares)

    st.subheader("Изменение статусов серверов")
    change_status_buttons()

    st.subheader("Список серверов")
    if servers:
        servers_table(servers)
    else:
        st.warning("Нет серверов")
