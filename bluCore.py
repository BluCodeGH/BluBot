import asyncio
import os
from os.path import join as pjoin
import json
import sys
import traceback
import datetime
import modules
from modules.internal.bot import Bot
from modules.internal import commands

with open(pjoin("data","botData.json"),"r") as infile:
  data = json.loads(infile.read())
selfBot = data[-2] == "s"

client = Bot(data[-1])
print("Loading modules.")
objects = modules.init(client, selfBot)
system = objects["system"]
print("Modules loaded.")

cooldown = {}

@client.event
async def on_ready():
  print('Logged in as ' + client.user.display_name + '.')
  objects["repl"].coreGlobals = globals()
  objects["repl"].coreLocals = locals()
  if selfBot:
    with open(pjoin("data", "perms.json"), "r") as inf:
      pdata = json.loads(inf.read())
    if pdata["owner"] == ["replaceMe"]:
      with open(pjoin("data", "perms.json"), "w+") as out:
        out.write(json.dumps({"owner":[client.user.id],"admin":pdata["admin"]}))
    print("Voice disabled due to running in selfbot mode.")
  if restartMsg is not None:
    await client.send_message(restartMsg.channel, "Restarted successfully.")

@client.event
async def on_message(m):
  if client.was_sent(m):
    return
  if m.content.startswith(client.prefix) and not m.author.bot and m.content.strip(client.prefix) != "":
    if selfBot and m.author.id != client.user.id:
      return
    if cooldown.get(m.author.id, None) is not None:
      if (datetime.datetime.now() - cooldown[m.author.id]).total_seconds() < 3:
        return
    cooldown[m.author.id] = datetime.datetime.now()
    if ' ' in m.content:
      comm, args = m.content[len(client.prefix):].split(" ", 1)
    else:
      comm = m.content[len(client.prefix):]
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
  elif selfBot:
    await objects["selfbot"].substitute(m, None)
  await objects["management"].filter(m, None)

restartMsg = None

def run(msg):
  global restartMsg
  restartMsg = msg
  loop = asyncio.get_event_loop()
  try:
    try:
      print("Logging in.")
      loop.run_until_complete(client.start(*data[:-2], bot=not selfBot))
    except RuntimeError:
      pass
  except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
    print("Logged out.")
  return client.isRestart
