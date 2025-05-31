from src.models.server import Datacenter, Server, Status
from src.utils.client import Client


class ServerService:
    def __init__(self, client: Client) -> None:
        self.client = client

    def get_servers(self) -> list[Server]:
        response = self.client.request("GET", "/servers")
        return [Server.model_validate(server) for server in response]

    def create_server(
        self,
        datacenter_id: int,
        hardware_id: int,
        status: Status,
        operating_system: str,
    ) -> Server:
        body = {
            "datacenter_id": datacenter_id,
            "hardware_id": hardware_id,
            "status": status,
            "operating_system": operating_system,
        }
        response = self.client.protected_request("POST", "/servers", json=body)
        return Server.model_validate(response)

    def delete_server(self, server_id: int) -> None:
        self.client.protected_request("DELETE", f"/servers/{server_id}")

    def release_servers(self) -> None:
        self.client.protected_request("PATCH", "/servers/release")

    def fix_servers_status(self) -> None:
        self.client.protected_request("PATCH", "/servers/fix_status")

    def change_server_status(self, server_id: int, status: Status) -> None:
        self.client.protected_request("PATCH", f"/servers/{server_id}", json={"status": status})

    def get_datacenters(self) -> list[Datacenter]:
        response = self.client.request("GET", "/datacenters")
        return [Datacenter.model_validate(datacenter) for datacenter in response]

    def get_countries(self) -> list[str]:
        response = self.client.request("GET", "/datacenters/countries")
        return [country["country_name"] for country in response]

    def add_datacenter(self, datacenter_name: str, country: str, city: str) -> Datacenter:
        body = {
            "datacenter_name": datacenter_name,
            "country": country,
            "city": city,
        }
        response = self.client.protected_request("POST", "/datacenters", json=body)
        return Datacenter.model_validate(response)

    def delete_datacenter(self, datacenter_id: int) -> None:
        self.client.protected_request("DELETE", f"/datacenters/{datacenter_id}")
