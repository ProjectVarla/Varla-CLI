from .context import context,init_context
from VarlaLib.functions.Verbosity import Verbosity

init_context()

context.flags = {}
context.flags["verbosity"] = Verbosity.NORMAL