from typing import List, Optional

from pydantic import BaseModel, validator
from treelib import Tree
from typer.core import TyperGroup
from VarlaLib.Context import context
from VarlaLib.Shell import Colorize, Foreground, Modifier


class TyperTree(BaseModel):

    command: Optional[TyperGroup]
    tree: Tree = Tree()
    dictionary: dict = {}

    class Config:
        arbitrary_types_allowed = True

    @validator("command", always=True)
    def command_validator(cls, v, values):
        return context.ctx_command

    @validator("tree", always=True)
    def tree_validator(cls, v, values):
        ROOT: str = "varla"
        v.create_node(
            Colorize(
                text=ROOT,
                style=Modifier.BOLD,
                foreground=Foreground.PURPLE,
            ),
            ROOT,
        )
        cls.get_ctx_tree(tree=v, commands=values["command"].commands, name=ROOT)

        v.update_node(
            f"{ROOT}_shell",
            tag=Colorize(
                text=f"shell { Colorize( text='[ Interactive Shell ]', style=Modifier.NOTHING,foreground=Foreground.DARK_GRAY )}",
                style=Modifier.BOLD,
                foreground=Foreground.PURPLE,
            ),
        )

        for i in context.command_center_registry:
            v.create_node(
                Colorize(
                    text=i.command.command,
                    style=Modifier.BOLD,
                    foreground=Foreground.YELLOW,
                ),
                i.command.command,
                parent=f"{ROOT}_shell",
                data="leaf",
            )
        return v

    @validator("dictionary", always=True)
    def dict_validator(cls, v, values):
        return cls.get_children(commands=values["command"].commands, name="varla")

    @classmethod
    def get_children(cls, commands, name: str):
        return {
            name: [
                cls.get_children(commands[i].commands, i)
                if "commands" in commands[i].__dict__
                else i
                for i in commands
            ]
        }

    @classmethod
    def get_ctx_tree(cls, tree: Tree, commands, name: str):
        for i in commands:
            if "commands" in commands[i].__dict__:
                tree.create_node(
                    Colorize(
                        text=i,
                        style=Modifier.BOLD,
                        foreground=Foreground.PURPLE
                        if commands[i].invoke_without_command
                        else Foreground.GREEN,
                    ),
                    name + "_" + i,
                    parent=name,
                    data="leaf" if commands[i].invoke_without_command else None,
                )
                cls.get_ctx_tree(tree, commands[i].commands, name + "_" + i)
            else:
                tree.create_node(
                    Colorize(text=i, style=Modifier.BOLD, foreground=Foreground.YELLOW),
                    name + "_" + i,
                    parent=name,
                    data="leaf",
                )
                for param in commands[i].params:
                    tree.create_node(
                        Colorize(
                            text=f"{' '.join(param.opts) if param.param_type_name == 'option' else param.name} [ {param.type} ] {'[ required ]' if param.required else ''}",
                            foreground=Foreground.BLUE,
                            style=Modifier.ITALIC,
                        ),
                        f"{name}_{i}_param_{param.name}",
                        parent=f"{name}_{i}",
                        data="param",
                    )

    def contains(self, cmd: List[str]):
        return self.tree.contains("varla_" + "_".join(cmd))

    def is_leaf(self, cmd: List[str]):
        return self.tree.get_node("varla_" + "_".join(cmd)).data == "leaf"
