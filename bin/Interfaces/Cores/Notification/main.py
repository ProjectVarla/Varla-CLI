import requests
from conf import settings
from VarlaLib.Shell import VarlaCLI as Varla
from websocket import create_connection


class Notifications:
    @staticmethod
    def push(channel_name: str, message: str):
        response = requests.get(
            f"{settings.GATEWAY_URL}/push/{channel_name}/{message}", timeout=3
        )
        return response.json()

    @staticmethod
    def bind(channel_name: str):
        Varla.clear(top_text="CHANNEL", bottom_text=channel_name)
        try:
            ws = create_connection(
                f"ws://{settings.NOTIFICATION_CORE_URL}/bind/{channel_name}"
            )
            while True:
                Varla.say(ws.recv(), name=channel_name)

        except:
            ws.close()
            Varla.clear()
