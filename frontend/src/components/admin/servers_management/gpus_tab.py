import streamlit as st

from src.db.connector import get_services_factory
from src.models.hardware import GPU


def create_gpu_form():
    col1, col2 = st.columns([1, 1])
    with col1:
        gpu_vendor = st.text_input("Производитель видеокарты")
        vram_gb = st.number_input("Объем видеопамяти (ГБ)", min_value=1)

    with col2:
        gpu_name = st.text_input("Название видеокарты")
        vram_type = st.text_input("Тип видеопамяти")

    if st.button("Добавить видеокарту"):
        services = get_services_factory()
        hardware_service = services.get_hardware_service()
        try:
            hardware_service.add_gpu(gpu_name, gpu_vendor, vram_type, vram_gb)
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def gpus_table(gpus: list[GPU]):
    st.markdown("---")
    for gpu in gpus:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col1:
            st.write(f"{gpu.gpu_id}")

        with col2:
            st.write(f"{gpu.gpu_vendor} {gpu.gpu_name}")

        with col3:
            st.write(f"{gpu.vram_gb} ГБ {gpu.vram_type}")

        with col4:
            if st.button("Удалить", key=gpu.gpu_name):
                services = get_services_factory()
                hardware_service = services.get_hardware_service()
                try:
                    hardware_service.delete_gpu(gpu.gpu_id)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")


def manage_gpus_tab(gpus: list[GPU]):
    st.subheader("Добавить видеокарту")
    create_gpu_form()

    st.subheader("Список видеокарт")
    if gpus:
        gpus_table(gpus)
    else:
        st.warning("Нет видеокарт")
