from dataclasses import dataclass
import os
from pprint import pprint
from typing import Any

from v2.Registry import Action, Registry, Command


@dataclass
class NotificationIntegration:
    @classmethod
    def registry(cls) -> Registry:

        # pprint(cls.__dict__)
        reg: Registry = Registry()
        for i in cls.__dict__:
            pprint(i)

        reg.add_command(
            Command(
                command="hello",
                action=Action(excutable=cls.hello),
            )
        )

        print(reg.commands)
        return reg

    @classmethod
    def hello(cls):
        print("hello")


if __name__ == "__main__":
    registry: Registry = Registry()

    registry.add_command(
        Command(
            command="help",
            action=Action(
                excutable=lambda: os.system("pipenv run python3 bin/Varla --help")
            ),
        )
    )

    registry.include(NotificationIntegration.registry())

    print(registry)

    for i in registry.commands:
        registry.DFS(i, 0)
