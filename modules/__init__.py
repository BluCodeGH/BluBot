import importlib
from .internal import commands

__all__ = ["system", "admin", "info", "quotes", "games", "management", "repl"]
modules = {}

for m in __all__:
  modules[m] = importlib.import_module("modules." + m)

def init(client, selfBot):
  if selfBot:
    __all__.append("selfbot")
    modules["selfbot"] = importlib.import_module("modules.selfbot")
  objects = {}
  for m in __all__:
    modules[m] = importlib.reload(modules[m])
    obj = modules[m].main(client)
    objects[m] = obj
    commands.objects[m] = obj
  return objects
