import requests
from conf import settings


class OrchestratorInfrastructureClient:
    @staticmethod
    def up(service_name: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/up/{service_name}",
            timeout=3,
        )
        return response.json()

    @staticmethod
    def down(service_name: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/down/{service_name}",
            timeout=3,
        )
        return response.json()

    @staticmethod
    def restart(service_name: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/restart/{service_name}",
            timeout=6,
        )
        return response.json()

    @staticmethod
    def status(service_name: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/status/{service_name}",
            timeout=3,
        )
        return response.json()
