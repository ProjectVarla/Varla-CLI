import requests
from Models.Cores import NotificationMessage
from conf import settings
from VarlaLib.Shell import VarlaCLI as Varla
from websocket import create_connection


class Notifications:
    @staticmethod
    def push(message: NotificationMessage):
        try:
            response = requests.get(
                f"{settings.GATEWAY_URL}/push/{message.channel_name}/{message.message}",
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)

    @staticmethod
    def bind(channel_name: str, host: str = ""):

        host = host if host else settings.NOTIFICATION_CORE_URL
        Varla.clear(top_text=host.upper(), bottom_text=channel_name)

        try:
            ws = create_connection(f"ws://{host}/bind/{channel_name}")
            while True:
                Varla.say(ws.recv(), name=channel_name)

        except KeyboardInterrupt:
            ws.close()
            Varla.clear()

        except Exception as e:
            Varla.clear()
            Varla.error(e)
