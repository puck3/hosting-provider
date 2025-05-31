import streamlit as st

from src.models.hardware import CPU
from src.pages.plans import ServicesFactory


def create_cpu_form():
    col1, col2 = st.columns([1, 1])
    with col1:
        cpu_vendor = st.text_input("Производитель процессора")
        frequency = st.number_input("Тактовая частота (ГГц)", min_value=1.0)

    with col2:
        cpu_name = st.text_input("Название процессора")
        cores = st.number_input("Количество ядер", min_value=1)

    if st.button("Добавить процессор"):
        services = ServicesFactory()
        hardware_service = services.get_hardware_service()
        try:
            hardware_service.add_cpu(cpu_name, cpu_vendor, cores, frequency)
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def cpus_table(cpus: list[CPU]):
    st.markdown("---")
    for cpu in cpus:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col1:
            st.write(f"{cpu.cpu_id}")

        with col2:
            st.write(f"{cpu.cpu_vendor} {cpu.cpu_name}")

        with col3:
            st.write(f"{cpu.frequency} ГГц, {cpu.cores} ядер")

        with col4:
            if st.button("Удалить", key=cpu.cpu_name):
                services = ServicesFactory()
                hardware_service = services.get_hardware_service()
                try:
                    hardware_service.delete_cpu(cpu.cpu_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")


def manage_cpus_tab(cpus: list[CPU]):
    st.subheader("Добавить процессор")
    create_cpu_form()

    st.subheader("Список процессоров")
    if cpus:
        cpus_table(cpus)
    else:
        st.warning("Нет процессоров")
