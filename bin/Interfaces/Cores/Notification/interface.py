from pprint import pprint
import typer

from VarlaLib.Context import context
from VarlaLib import Notify
from Models.Cores import NotificationMessage
from VarlaLib.Shell import VarlaCLI as Varla
from .main import Notifications

notification = typer.Typer(add_completion=True)


@notification.command("push")
def push(channel_name: str, message: str):
    Notifications.push(NotificationMessage(channel_name=channel_name, message=message))


@notification.command("bind")
def bind(channel_name: str, host: str = typer.Option(None, "--host", "-h")):
    Notifications.bind(channel_name, host)


@notification.command("context")
def context():
    # Noti
    context.test = "test?"
    # fications.bind(channel_name, host)
    print((context.__dict__))


@notification.command("subscribe")
def subscribe():
    # Noti
    context.test = "test?"
    # fications.bind(channel_name, host)
    print((context.__dict__))


# @notification.command("switch")
# def switch():
#     run_socket("ws://localhost:8500/connect")
#     pass
