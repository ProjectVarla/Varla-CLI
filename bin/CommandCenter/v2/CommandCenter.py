from __future__ import annotations
import functools
import os
from pprint import pprint
from typing import List

from VarlaLib.Context import context
from .NotificationCoreShellIntegration import NotificationIntegration


from .TyperTree import TyperTree

from VarlaLib.Shell import VarlaCLI as Varla
from VarlaLib import Verbosity
from .Registry import Registry, Command, Action
from pydantic import BaseModel


class CommandCenter:
    @staticmethod
    def commands() -> list[Command]:
        return CommandCenter.get_registry().commands

    def registry():
        return CommandCenter.get_registry()

    @staticmethod
    def get_registry() -> Registry:

        reg = Registry(
            commands=[
                Command(
                    command="parse",  # "unsubscribe",
                    sub_commands=[
                        Command(
                            command="switch",
                            action=Action(
                                excutable=lambda: NotificationIntegration.connect()
                            ),
                        ),
                        Command(
                            command="stop",
                            action=Action(
                                excutable=lambda: NotificationIntegration.stop()
                            ),
                        ),
                        Command(
                            command="id",
                            action=Action(excutable=NotificationIntegration.get_id),
                            sub_commands=[
                                Command(
                                    command="show",
                                    action=Action(
                                        excutable=NotificationIntegration.get_id
                                    ),
                                    sub_commands=[],
                                ),
                                Command(
                                    command="delete",
                                    action=Action(
                                        excutable=NotificationIntegration.get_id
                                    ),
                                    sub_commands=[],
                                ),
                            ],
                        ),
                        Command(
                            command="sub",  # "subscribe",
                            action=Action(excutable=NotificationIntegration.subscribe),
                        ),
                        Command(
                            command="unsub",  # "unsubscribe",
                            action=Action(
                                excutable=NotificationIntegration.unsubscribe
                            ),
                        ),
                    ],
                ),
            ]
        )

        re2 = Registry(
            commands=[
                # command=["help", "options"],
                # action=Action(excutable = lambda: os.system("pipenv run python3 Varla --help"))
                Command(
                    command="help",
                    action=Action(
                        excutable=lambda: os.system(
                            "pipenv run python3 bin/Varla --help"
                        )
                    ),
                ),
                Command(
                    command="list",
                    short_hand="ls",
                    action=Action(excutable=CommandCenter.list_registry_options),
                ),
                Command(
                    command="tree",
                    short_hand="tr",
                    action=Action(
                        excutable=lambda: (
                            TyperTree().tree.show(
                                filter=lambda node: node.data != "param"
                            )
                        )
                    ),
                ),
                Command(
                    command="param_tree",
                    short_hand="ptr",
                    action=Action(excutable=lambda: (TyperTree().tree.show())),
                ),
                Command(
                    command="debug_tree",
                    short_hand="dtr",
                    action=Action(
                        excutable=lambda: pprint(TyperTree().tree.all_nodes())
                    ),
                ),
                Command(
                    command="heartbeat",
                    short_hand="hb",
                    action=Action(excutable=lambda: Varla.heartbeat()),
                ),
                Command(
                    command="history",
                    action=Action(excutable=lambda: Varla.history()),
                ),
                Command(
                    command="bye",
                    action=Action(
                        excutable=lambda: Varla.say("Goodbye boss!") & exit()
                    ),
                ),
                Command(
                    command="hello",
                    action=Action(excutable=lambda: Varla.say("Hello boss!")),
                ),
                Command(
                    command="clear",
                    short_hand="clr",
                    action=Action(excutable=lambda: Varla.clear()),
                ),
                Command(
                    command="flags",
                    action=Action(excutable=lambda: Varla.say(context.flags)),
                ),
            ]
        )

        reg.include(re2)

        return reg

    @staticmethod
    def list_registry_options():
        for command in CommandCenter.commands():
            print((command.command))

    @classmethod
    def get_command(cls, command: List[str]):
        return cls.registry().find(command)
