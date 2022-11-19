import enum
from typing import Literal
from VarlaLib.Context import context
from VarlaLib import say


class Verbosity(enum.Enum):
    QUITE = 0
    NORMAL = 1
    VERBOSE = 2
    ALWAYS = 3

    def __str__(self) -> Literal['normal', 'quite', 'verbose'] | None:
        if self == Verbosity.NORMAL:
            return "normal"
        if self == Verbosity.QUITE:
            return "quite"
        if self == Verbosity.VERBOSE:
            return "verbose"


def say_conditional(message: str) -> None:
    print(message)


def set_verbosity(status: Verbosity) -> None:
    if status == Verbosity.QUITE:
        say(f"Shhh! setting verbosity to {status}")
    elif status == Verbosity.VERBOSE:
        say(f"Loud and clear! setting verbosity to {status}")
    elif status == Verbosity.NORMAL:
        say(f"Back to normal! setting verbosity to {status}")

    context.flags["verbosity"] = status


context.flags["verbosity"] = Verbosity.NORMAL
