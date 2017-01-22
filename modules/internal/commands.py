import asyncio
import os
import inspect
from . import perms

commands = {}
commandHelp = {}
commandHelpClass = {}
objects = {}

def command(alts=None, optional=False):
  if alts is not None:
    if isinstance(alts, str):
      alts = [alts]
  else:
    alts = []
  def real_command(func):
    obj = inspect.getfile(func).split(os.sep)[-1].split(".")[0]
    if objects.get(obj, -1) == -1:
      objects[obj] = None
    if commandHelpClass.get(obj, None) is None:
      commandHelpClass[obj] = {}
    async def wrapper(m, args, args2="UNUSED"):
      if args2 != "UNUSED":
        m = args
        args = args2
      if inspect.getsourcelines(func)[0][1][-4] != "_" and args is None and not optional:
        res = 'Err: Missing required argument. Usage:\n```' + func.__doc__.split("\n", 2)[-1] +  + "```"
        await objects[obj].client.send_message(m.channel, res)
      else:
        await func(objects[obj], m, args)
    commands[func.__name__] = wrapper
    commandHelp[func.__name__] = func.__doc__.split("\n", 1)
    commandHelpClass[obj][func.__name__] = func.__doc__.split("\n", 1)
    for alt in alts:
      commands[alt] = wrapper
      hlp = func.__doc__.split("\n", 3)
      if len(hlp) == 3:
        hlp.append("")
      hlp = [hlp[0], hlp[1] + "\n" + hlp[2].replace(func.__name__, alt) + "\n" + hlp[3]]
      commandHelp[alt] = hlp
      commandHelpClass[obj][alt] = hlp + [None]
    return func
  return real_command

def adminCommand(alts=None, optional=False):
  if alts is not None:
    if isinstance(alts, str):
      alts = [alts]
  else:
    alts = []
  def real_adminCommand(func):
    obj = inspect.getfile(func).split(os.sep)[-1].split(".")[0]
    if objects.get(obj, -1) == -1:
      objects[obj] = None
    async def wrapper(m, args, args2="UNUSED"):
      selfCalled = False
      if args2 != "UNUSED":
        selfCalled = True
        m = args
        args = args2
      if await perms.check(m.author.id, ["owner", "admin"]) or selfCalled:
        if inspect.getsourcelines(func)[0][1][-4] != "_" and args is None and not optional:
          res = 'Err: Missing required argument. Usage:\n```' + func.__doc__.split("\n", 2)[-1] +  + "```"
          await objects[obj].client.send_message(m.channel, res)
        else:
          await func(objects[obj], m, args)
      else:
        await objects[obj].client.send_message(m.channel, 'Err: Admin only command.')
    commands[func.__name__] = wrapper
    commandHelp[func.__name__] = func.__doc__.split("\n", 1)
    commandHelpClass[obj][func.__name__] = func.__doc__.split("\n", 1)
    for alt in alts:
      commands[alt] = wrapper
      hlp = func.__doc__.split("\n", 3)
      if len(hlp) == 3:
        hlp.append("")
      hlp = [hlp[0], hlp[1] + "\n" + hlp[2].replace(func.__name__, alt) + "\n" + hlp[3]]
      commandHelp[alt] = hlp
      commandHelpClass[obj][alt] = hlp + [None]
    return func
  return real_adminCommand

def ownerCommand(alts=None, optional=False):
  if alts is not None:
    if isinstance(alts, str):
      alts = [alts]
  else:
    alts = []
  def real_ownerCommand(func):
    obj = inspect.getfile(func).split(os.sep)[-1].split(".")[0]
    if objects.get(obj, -1) == -1:
      objects[obj] = None
    async def wrapper(m, args, args2="UNUSED"):
      selfCalled = False
      if args2 != "UNUSED":
        selfCalled = True
        m = args
        args = args2
      if await perms.check(m.author.id, ["owner"]) or selfCalled:
        if inspect.getsourcelines(func)[0][1][-4] != "_" and args is None and not optional:
          res = 'Err: Missing required argument. Usage:\n```' + func.__doc__.split("\n", 2)[-1] +  + "```"
          await objects[obj].client.send_message(m.channel, res)
        else:
          await func(objects[obj], m, args)
      else:
        await objects[obj].client.send_message(m.channel, 'Err: Owner only command.')
    commands[func.__name__] = wrapper
    commandHelp[func.__name__] = func.__doc__.split("\n", 1)
    commandHelpClass[obj][func.__name__] = func.__doc__.split("\n", 1)
    for alt in alts:
      commands[alt] = wrapper
      hlp = func.__doc__.split("\n", 3)
      if len(hlp) == 3:
        hlp.append("")
      hlp = [hlp[0], hlp[1] + "\n" + hlp[2].replace(func.__name__, alt) + "\n" + hlp[3]]
      commandHelp[alt] = hlp
      commandHelpClass[obj][alt] = hlp + [None]
    return func
  return real_ownerCommand
