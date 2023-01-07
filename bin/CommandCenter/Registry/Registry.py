import os
from pprint import pprint
from typing import List

from VarlaLib.Context import context

from ..TyperTree import TyperTree

from VarlaLib.Shell import VarlaCLI as Varla
from VarlaLib import Verbosity
from Models import Registry, Command


class CommandCenter:
    @staticmethod
    def commands():
        return CommandCenter.get_registry()

    @staticmethod
    def get_registry():
        return [
            Registry(
                # command=["help", "options"],
                # action=lambda: os.system("pipenv run python3 Varla --help")
                command=Command(
                    command="help",
                    options=[],
                    action=lambda: os.system("pipenv run python3 bin/Varla --help"),
                )
            ),
            Registry(
                command=Command(
                    command="list",
                    short_hand="ls",
                    options=[],
                    action=lambda: CommandCenter.list_registry_options(),
                )
            ),
            Registry(
                command=Command(
                    command="tree",
                    short_hand="tr",
                    options=[],
                    action=lambda: (
                        TyperTree().tree.show(filter=lambda node: node.data != "param")
                    ),
                )
            ),
            Registry(
                command=Command(
                    command="param_tree",
                    short_hand="ptr",
                    options=[],
                    action=lambda: (TyperTree().tree.show()),
                )
            ),
            Registry(
                command=Command(
                    command="debug_tree",
                    short_hand="dtr",
                    options=[],
                    action=lambda: pprint(TyperTree().tree.all_nodes()),
                )
            ),
            # Registry(
            #     command=Command(
            #         command="tasks",
            #         options=["-a"],
            #         action=lambda: os.system("pipenv run python3 bin/Varla tasks"),
            #     ),
            #     subcommands=[],
            # ),
            # Registry(
            #     command=["quite"],
            #     action=lambda: set_verbosity(Verbosity.QUITE)
            # ),
            # Registry(
            #     command=["verbose"],
            #     action=lambda: set_verbosity(Verbosity.VERBOSE)
            # ),
            # Registry(
            #     command=["normal"],
            #     action=lambda: set_verbosity(Verbosity.NORMAL)
            # ),
            Registry(
                command=Command(
                    command="heartbeat",
                    short_hand="hb",
                    action=lambda: Varla.heartbeat(),
                )
            ),
            Registry(
                command=Command(command="history", action=lambda: Varla.history())
            ),
            Registry(
                command=Command(
                    command="bye",
                    action=lambda: Varla.say("Goodbye boss!") & exit(),
                )
            ),
            Registry(
                command=Command(
                    command="hello",
                    # "hi",
                    # "hey",
                    # "hello varla",
                    # "hi varla",
                    # "hey varla",
                    action=lambda: Varla.say("Hello boss!"),
                )
            ),
            Registry(
                command=Command(
                    command="clear", short_hand="clr", action=lambda: Varla.clear()
                )
            ),
            Registry(
                command=Command(
                    command="flags", action=lambda: Varla.say(context.flags)
                )
            ),
        ]

    @staticmethod
    def list_registry_options():
        for command in CommandCenter.commands():
            print((command.command.command))

    @staticmethod
    def get_command(command: List[str]):
        for item in CommandCenter.get_registry():
            if (
                command[0] == item.command.command
                or command[0] == item.command.short_hand
            ):
                return item
        return None
