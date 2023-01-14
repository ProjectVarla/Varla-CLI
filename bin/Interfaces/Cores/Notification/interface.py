import typer

from VarlaLib import Notify
from Models.Cores import NotificationMessage

from .main import Notifications

notification = typer.Typer(add_completion=True)


@notification.command("push")
def push(channel_name: str, message: str):
    Notifications.push(NotificationMessage(channel_name=channel_name, message=message))


@notification.command("bind")
def bind(channel_name: str, host: str = typer.Option(None, "--host", "-h")):
    Notifications.bind(channel_name, host)
