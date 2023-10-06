from __future__ import annotations
from dataclasses import dataclass
from optparse import Option
from pprint import pprint
from typing import Callable, Optional
from pydantic import BaseModel, validator


class Action(BaseModel):
    excutable: Callable
    options: Optional[list[str]] = []


class Command(BaseModel):
    command: str
    sub_nodes: Optional[list[Command]] = []
    action: Action


class Registry(BaseModel):
    commands: Optional[list[Command]]


def DFS(node: Command, depth: int):

    # print("\t" * depth, "|" + "----", node.command)
    node.action.excutable()
    for i in node.sub_nodes:
        DFS(i, depth=depth + 1)


if __name__ == "__main__":
    x = Command(
        command="notification",
        action=Action(excutable=lambda: print("notification")),
        sub_nodes=[
            Command(
                command="push",
                action=Action(excutable=lambda: print("push")),
                sub_nodes=[
                    Command(
                        command="push",
                        action=Action(excutable=lambda: print("push")),
                        sub_nodes=[
                            Command(
                                command="push",
                                action=Action(excutable=lambda: print("push")),
                            ),
                            Command(
                                command="bind",
                                action=Action(excutable=lambda: print("bind")),
                            ),
                        ],
                    ),
                    Command(
                        command="bind",
                        action=Action(excutable=lambda: print("bind")),
                    ),
                ],
            ),
            Command(
                command="bind",
                action=Action(excutable=lambda: print("bind")),
            ),
        ],
    )

    DFS(x, 0)
