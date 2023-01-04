import requests
from conf import settings
from Models import ServicesFilter


class OrchestratorInfrastructureClient:
    @staticmethod
    def up(service_filter: ServicesFilter):
        response = requests.post(
            f"{settings.GATEWAY_URL}/up",
            json=service_filter.dict(),
            timeout=3,
        )
        return response.json()

    @staticmethod
    def down(service_filter: ServicesFilter):
        response = requests.post(
            f"{settings.GATEWAY_URL}/down",
            json=service_filter.dict(),
            timeout=3,
        )
        return response.json()

    @staticmethod
    def restart(service_filter: ServicesFilter):
        response = requests.post(
            f"{settings.GATEWAY_URL}/restart",
            json=service_filter.dict(),
            timeout=6,
        )
        return response.json()

    @staticmethod
    def status(service_filter: ServicesFilter):
        response = requests.post(
            f"{settings.GATEWAY_URL}/status",
            json=service_filter.dict(),
            timeout=3,
        )
        return response.json()

    @staticmethod
    def list():
        response = requests.post(
            f"{settings.GATEWAY_URL}/list",
            timeout=3,
        )
        return response.json()
