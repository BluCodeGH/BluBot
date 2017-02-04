import importlib
from .internal import commands

__all__ = ["system", "admin", "info", "quotes", "games", "management", "repl", "fun", "logger"]
modules = {}

for m in __all__:
  modules[m] = importlib.import_module("modules." + m)

def init(client, selfBot):
  if selfBot:
    __all__.append("selfbot")
    modules["selfbot"] = importlib.import_module("modules.selfbot")
  else:
    __all__.append("voice")
    modules["voice"] = importlib.import_module("modules.voice")
  objects = {}
  on_messages = []
  for m in __all__:
    modules[m] = importlib.reload(modules[m])
    obj = modules[m].main(client)
    objects[m] = obj
    commands.objects[m] = obj
    try:
      on_messages.append(obj.on_message)
    except AttributeError:
      pass
  return objects, on_messages
