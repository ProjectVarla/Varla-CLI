import requests
from conf import settings


class Notifications:
    @staticmethod
    def push(channel_name: str, message: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/push/{channel_name}/{message}", timeout=3
        )
        return response.json()
