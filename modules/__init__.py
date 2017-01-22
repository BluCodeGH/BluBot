import importlib
from .internal import commands

__all__ = ["system", "admin", "info"]
modules = {}

for m in __all__:
  modules[m] = importlib.import_module("modules." + m)

def init(client):
  sysObj = None
  for m in __all__:
    modules[m] = importlib.reload(modules[m])
    obj = modules[m].main(client)
    commands.objects[m] = obj
    if m == "system":
      sysObj = obj
  return sysObj
