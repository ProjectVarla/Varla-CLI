import requests
from conf import settings
from VarlaLib.Shell import VarlaCLI as Varla
from Models import ServicesFilter


class OrchestratorInfrastructureClient:
    @staticmethod
    def up(service_filter: ServicesFilter):
        try:
            response = requests.post(
                f"{settings.ORCHESTRATOR_URL}/up",
                json=service_filter.dict(),
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)
            return []

    @staticmethod
    def down(service_filter: ServicesFilter):
        try:
            response = requests.post(
                f"{settings.ORCHESTRATOR_URL}/down",
                json=service_filter.dict(),
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)
            return []

    @staticmethod
    def restart(service_filter: ServicesFilter):
        try:
            response = requests.post(
                f"{settings.ORCHESTRATOR_URL}/restart",
                json=service_filter.dict(),
                timeout=6,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)
            return []

    @staticmethod
    def status(service_filter: ServicesFilter):
        try:
            response = requests.post(
                f"{settings.ORCHESTRATOR_URL}/status",
                json=service_filter.dict(),
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)
            return []

    @staticmethod
    def list():
        try:
            response = requests.post(
                f"{settings.ORCHESTRATOR_URL}/list",
                timeout=3,
            )
            Varla.debug(response.json(), name="Orchestrator List Response")
            return response.json()

        except Exception as e:
            Varla.error(e)
            return []
