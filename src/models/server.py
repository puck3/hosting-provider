from src.core.constants import default_str, Status
from src.schemas.hardware_config import HardwareConfigResponse
from src.schemas.server import Datacenter


class Server:
    def __init__(
        self,
        operating_system: default_str,
        datacenter: Datacenter,
        config: HardwareConfigResponse,
        status: Status = Status.inactive,
    ) -> None:
        self.status = status
        self.operating_system = operating_system
        self.datacenter = datacenter
        self.config = config

    def set_status(self, status: Status) -> None:
        self.status = status

    def get_status(self) -> Status:
        return self.status
