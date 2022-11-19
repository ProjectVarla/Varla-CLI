from math import ceil, floor, floor
import os
from os import system
import readline

from Models.Registry.main import Registry
from VarlaLib.Shell.Colors import Colorize, Foreground, Modifier


class VarlaCLI:

    @staticmethod
    def standby(commands: list[Registry]):
        standby(commands)

    @staticmethod
    def say(message: str):
        say(message)

    @staticmethod
    def ask(message: str = ""):
        ask(message)

    @staticmethod
    def error(message: str):
        error(message)

    @staticmethod
    def heartbeat():
        heartbeat()

    @staticmethod
    def history():
        history()

    @staticmethod
    def clear() -> None:
        clear()


def standby(commands: list[Registry]):
    VarlaCLI.say("Yes boss!")
    VarlaCLI.say("How can I help you?")

    while True:
        command = ask()
        command = command.lower().split(" ")
        for item in commands:
            if command[0] == item.command.command or command[0] == item.command.short_hand:
                item.trigger()

                break
        else:
            VarlaCLI.say("ha?!")


def say(message: str):
    print(f"\033[36m\033[01mVarla >> \033[0m{message}")


def ask(message: str = ""):
    if message:
        message = f"\033[36mVarla >> \033[0m{message}\n"
    try:
        return input(message + "\033[33m\033m  #   >>\033[0m ")
    except KeyboardInterrupt:
        print()
        VarlaCLI.say("Goodbye Boss!")
        exit()


def error(message: str):
    print(f"\033[31m\033[01mVarla >> \033[0m Oops!, Something went wrong!")
    print(
        f"\033[31m\033[01mVarla >> \033[0m This is what I managed to capture: {message}")


def heartbeat():
    VarlaCLI.say("Connecting to main-frame...")
    VarlaCLI.say("Connected!")


def history():
    for i in range(readline.get_current_history_length()):
        print(i, readline.get_history_item(i))


def clear():
    rows, columns = os.popen('stty size', 'r').read().split()
    print(rows, columns)

    columns = max(int(columns), 44)
# \033[33m\033[01mPROJECT\033[0m
    varla_logo = [
        Colorize('██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ ',
                 foreground=Foreground.LIGHT_CYAN),
        Colorize('██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗',
                 foreground=Foreground.LIGHT_CYAN),
        Colorize('██║   ██║███████║██████╔╝██║     ███████║',
                 foreground=Foreground.LIGHT_CYAN),
        Colorize('╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║',
                 foreground=Foreground.LIGHT_CYAN),
        Colorize(' ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║',
                 foreground=Foreground.LIGHT_CYAN),
        Colorize('  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝',
                 foreground=Foreground.LIGHT_CYAN),
        # "\033[36m██╗   ██╗ █████╗ ██████╗ ██╗      █████╗ \033[0m",
        # "\033[36m██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗\033[0m",
        # "\033[36m██║   ██║███████║██████╔╝██║     ███████║\033[0m",
        # "\033[36m╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║\033[0m",
        # "\033[36m ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║\033[0m",
        # "\033[36m  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\033[0m"
    ]

    system("cls||clear")

    print(f"╔═ { Colorize('PROJECT',foreground=Foreground.YELLOW,style=Modifier.BOLD)} {'═'*floor(columns-12)}╗")
    print(f"║{' '*floor(columns-2)}║")
    for i in varla_logo:
        print(
            f"║{' '*int(((columns-len(i))/2)+4)}{i}{' '*int(((columns-len(i))/2)+5)}║")

    print(f"║{' '*floor(columns-2)}║")
    print(
        f"╚{'═'*floor(columns-14)} { Colorize('VARLA-CLI',foreground=Foreground.YELLOW,style=Modifier.BOLD)} ═╝")
    #         """║                                             ║
    # ║ \033[36m ██╗   ██╗ █████╗ ██████╗ ██╗      █████╗\033[0m   ║
    # ║ \033[36m ██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗\033[0m  ║
    # ║ \033[36m ██║   ██║███████║██████╔╝██║     ███████║\033[0m  ║
    # ║ \033[36m ╚██╗ ██╔╝██╔══██║██╔══██╗██║     ██╔══██║\033[0m  ║
    # ║ \033[36m  ╚████╔╝ ██║  ██║██║  ██║███████╗██║  ██║\033[0m  ║
    # ║ \033[36m   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\033[0m  ║
    # ║                                             ║
    # """,

    # f"╚{'═'*int(columns-2)}╝\n", end = "")

# \033[33m\033[01mVARLA-CLI\033[0m
