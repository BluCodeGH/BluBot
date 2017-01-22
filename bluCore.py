import asyncio
from os.path import join as pjoin
import json
import datetime
import discord
import modules
from modules.internal import commands

client = discord.Client()
print("Loading modules.")
system = modules.init(client)
print("Modules loaded.")

cooldown = {}

with open(pjoin("data","botData.json"),"r") as infile:
  data = json.loads(infile.read())

@client.event
async def on_ready():
  print('Logged in as ' + client.user.display_name + '.')

@client.event
async def on_message(m):
  if m.content.startswith(system.startChars) and not m.author.bot and m.content.strip(system.startChars) != "":
    if data[-2] == "u" and m.author.id != client.user.id:
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
    if comm in commands.commands.keys():
      try:
        await commands.commands[comm](m, args)
      except Exception as e:
        res = "An internal error occurred. Contact <@!207648732336881664> for help.\n"
        res += "```" + str(type(e).__name__) + ": " + str(e) + ".```"
        await client.send_message(m.channel, res)
        if args is None:
          args = ""
  elif m.content == "The current latency is" and m.author == client.user:
    await commands.commands["latency"](m, "placeholder")

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
