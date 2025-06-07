import streamlit as st

from src.models.hardware import Hardware


def cpu_column(hardware: Hardware):
    st.write(f"{hardware.cpus_count}x {hardware.cpu.cpu_vendor} {hardware.cpu.cpu_name}")
    st.write(f"{hardware.cpu.frequency} ГГц, {hardware.cpu.cores * hardware.cpus_count} ядер")


def gpu_column(hardware: Hardware):
    assert hardware.gpu is not None
    st.write(f"{hardware.gpus_count}x {hardware.gpu.gpu_vendor} {hardware.gpu.gpu_name}")
    st.write(f"{hardware.gpu.vram_gb * hardware.gpus_count} ГБ {hardware.gpu.vram_type}")


def memory_column(hardware: Hardware):
    st.write(f"ОЗУ: {hardware.ram_gb} ГБ")
    st.write(f"ПЗУ: {hardware.storage_tb} TБ")


def hardware_card(hardware: Hardware):
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        cpu_column(hardware)
    with col2:
        if hardware.gpu:
            gpu_column(hardware)
        else:
            memory_column(hardware)
    with col3:
        if hardware.gpu:
            memory_column(hardware)
        st.write(f"Сеть: {hardware.bandwidth_gbps} Гбит/c")
