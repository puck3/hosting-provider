import streamlit as st

from src.components.shared.hardware_card import hardware_card
from src.models.hardware import CPU, GPU, Hardware
from src.services.services_factory import ServicesFactory
from src.utils.key_id_map import CPUKeyIdMap, GPUKeyIdMap


def create_hardware_form(cpus: list[CPU], gpus: list[GPU]):
    cpu_mapper = CPUKeyIdMap(cpus)
    gpu_mapper = GPUKeyIdMap(gpus)
    col1, col2 = st.columns([2, 1])
    with col1:
        cpu_name = st.selectbox("Процессор", cpu_mapper.list_keys())
        gpu_name = st.selectbox("Видеокарта", [None] + gpu_mapper.list_keys())

    with col2:
        cpus_count = st.number_input("Количество процессоров", min_value=1)
        gpus_count = st.number_input(
            "Количество видеокарт",
            min_value=1 if gpu_name else 0,
            max_value=(None if gpu_name else 0),
        )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        storage_tb = st.number_input("ПЗУ (ТБ)", min_value=1)

    with col2:
        ram_gb = st.number_input("ОЗУ(ГБ)", min_value=32)

    with col3:
        bandwidth_gbps = st.number_input("Сеть (Гбит/c)", min_value=1)

    if st.button("Добавить конфигурацию"):
        services = ServicesFactory()
        hardware_service = services.get_hardware_service()
        try:
            hardware_service.create_hardware(
                cpu_id=cpu_mapper.get(cpu_name),
                cpus_count=cpus_count,
                gpu_id=gpu_mapper.get(gpu_name) if gpu_name else None,
                gpus_count=gpus_count,
                storage_tb=storage_tb,
                ram_gb=ram_gb,
                bandwidth_gbps=bandwidth_gbps,
            )
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def hardwares_table(hardwares: list[Hardware]):
    st.markdown("---")
    for hardware in hardwares:
        col1, col2, col3 = st.columns([1, 9, 2])
        with col1:
            st.write(f"{hardware.hardware_id}")

        with col2:
            hardware_card(hardware)

        with col3:
            if st.button("Удалить", key=f"{hardware.hardware_id}{hardware.cpu.cpu_name}"):
                services = ServicesFactory()
                hardware_service = services.get_hardware_service()
                try:
                    hardware_service.delete_hardware(hardware.hardware_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")


def manage_hardwares_tab(
    cpus: list[CPU],
    gpus: list[GPU],
    hardwares: list[Hardware],
):
    st.subheader("Добавить конфигурацию сервера")
    create_hardware_form(cpus, gpus)

    st.subheader("Список конфигураций")
    if hardwares:
        hardwares_table(hardwares)
    else:
        st.warning("Нет конфигураций серверов")
