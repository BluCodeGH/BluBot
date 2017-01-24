import asyncio
import os
from os.path import join as pjoin
import json
import sys
import traceback
import datetime
import discord
import modules
from modules.internal import commands

with open(pjoin("data","botData.json"),"r") as infile:
  data = json.loads(infile.read())
selfBot = data[-2] == "s"

client = discord.Client()
print("Loading modules.")
objects = modules.init(client, selfBot)
system = objects["system"]
print("Modules loaded.")

cooldown = {}

@client.event
async def on_ready():
  print('Logged in as ' + client.user.display_name + '.')

@client.event
async def on_message(m):
  if m.content.startswith(system.startChars) and not m.author.bot and m.content.strip(system.startChars) != "":
    if selfBot and m.author.id != client.user.id:
      return
    if cooldown.get(m.author.id, None) is not None:
      if (datetime.datetime.now() - cooldown[m.author.id]).total_seconds() < 3:
        return
    cooldown[m.author.id] = datetime.datetime.now()
    if ' ' in m.content:
      comm, args = m.content[len(system.startChars):].split(" ", 1)
    else:
      comm = m.content[len(system.startChars):]
      args = None
    if comm.lower() in commands.commands.keys():
      try:
        await commands.commands[comm.lower()](m, args)
      except Exception as e:
        res = "An internal error occurred. Contact <@!207648732336881664> for help.\n```python\n"
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for i, line in enumerate(traceback.format_exception(exc_type, exc_value, exc_traceback)):
          if i > 0 and i < len(traceback.format_exception(exc_type, exc_value, exc_traceback)) - 1 and not line.split(os.sep)[-1].startswith("  File"):
            res += '  File "'
          res += line.split(os.sep)[-1]
        res += "```"
        await client.send_message(m.channel, res)
        if args is None:
          args = ""
  elif m.content == "The current latency is" and m.author == client.user:
    await commands.commands["latency"](m, "placeholder")
  if selfBot:
    await objects["selfbot"].substitute(m, None)
  await objects["management"].filter(m, None)

def run():
  loop = asyncio.get_event_loop()
  try:
    try:
      print("Logging in.")
      loop.run_until_complete(client.start(*data[:-2]))
    except RuntimeError:
      pass
  except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
    print("Logged out.")
  return system.isRestart
