from __future__ import annotations
import os
from pprint import pprint

from typing import Any, Callable, Optional, OrderedDict

from pydantic import BaseModel, validator


class Action(BaseModel):
    excutable: Callable
    options: Optional[list[str]] = []
    params: OrderedDict[str, dict[str, Any]] = {}

    @validator("options", always=True)
    def validate_options(cls, v, values):
        return values["excutable"].__annotations__

    @validator("params", always=True)
    def validate_params(cls, v, values) -> OrderedDict[str, dict[str, Any]]:

        e: Callable = values["excutable"]

        params: dict[str, dict[str, Any]] = OrderedDict()
        for key in e.__code__.co_varnames:
            params[key] = {"required": True, "type": Any, "default": None}

        for key in e.__annotations__:
            params[key]["type"] = e.__annotations__[key]

        if e.__defaults__:
            for idx, key in enumerate(e.__code__.co_varnames[-len(e.__defaults__) :]):
                params[key] = {
                    **params[key],
                    "default": e.__defaults__[idx],
                    "required": False,
                }

        return params


class Command(BaseModel):
    command: str
    short_hand: Optional[str]
    sub_commands: Optional[list[Command]] = []
    action: Optional[Action]

    @property
    def identifiers(self) -> list[str]:
        return [self.command, self.short_hand] if self.short_hand else [self.command]

    def trigger(self, prompt: list[str]):
        print(prompt)

        if not self.action:
            return

        pprint(self.action.params)
        try:
            if prompt != []:
                return self.action.excutable(*prompt)
            else:
                return self.action.excutable()

        except Exception as e:
            print(e)


class Registry(BaseModel):
    commands: Optional[list[Command]] = []

    def DFS(self, node: Command, depth: int):
        print(node.command)

        for i in node.sub_commands:
            self.DFS(i, depth=depth + 1)

    def find(self, prompt: list[str], commands: list[Command] = None, depth=0):
        if commands == None:
            commands: list[Command] = self.commands

        if depth >= len(prompt):
            return None, 0

        for command in commands:
            if prompt[depth] in command.identifiers:
                print(command.command)
                # Match
                sub_command, sub_depth = self.find(
                    prompt[depth::], commands=command.sub_commands, depth=depth + 1
                )

                if sub_command == None:  # This command is a leaf
                    return command, depth + 1

                else:
                    return sub_command, sub_depth

        else:  # No Match
            return None, 0

    def include(self, registry: Registry) -> None:
        [self.commands.append(command) for command in registry.commands]

    def add_command(self, command: Command) -> None:
        self.commands.append(command)


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

    for i in registry.commands:
        registry.DFS(i, 0)
