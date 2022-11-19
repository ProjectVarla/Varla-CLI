
import contextvars
import types

request_global = contextvars.ContextVar(
    "request_global", default=types.SimpleNamespace())
context = request_global.get()


def init_context() -> None:
    request_global.set(types.SimpleNamespace())
