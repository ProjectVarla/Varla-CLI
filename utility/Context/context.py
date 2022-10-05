
import contextvars,types

request_global = contextvars.ContextVar("request_global",default=types.SimpleNamespace())
context = request_global.get()

def init_context():
    request_global.set(types.SimpleNamespace())
