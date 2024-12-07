from src.models.hardware import Hardware


def get_hardware_info(hardware: Hardware) -> str:
    cpu = f"{hardware.cpus_count}x {hardware.cpu.cpu_name},"
    gpu = f"{hardware.gpus_count}x {hardware.gpu.gpu_name}," if hardware.gpu else ""
    other = f"OЗУ {hardware.ram_gb} ГБ, ПЗУ {hardware.storage_tb} ТБ, Сеть {hardware.bandwidth_gbps} Гбит/c"
    return f"{cpu} {gpu} {other}"
