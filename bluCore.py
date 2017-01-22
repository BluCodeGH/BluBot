import asyncio
from os.path import join as pjoin
import json
import discord

client = discord.Client()
with open(pjoin("data","botData.json"),"r") as infile:
  data = json.loads(infile.read())

@client.event
async def on_ready():
  print('Logged in as ' + client.user.display_name + '.')

@client.event
async def on_message(m):
  print(m.content)
  if m.content == ".q":
    await client.logout()

def run(count):
  loop = asyncio.get_event_loop()
  try:
    try:
      print("Logging in.")
      loop.run_until_complete(client.start(*data[:-1]))
      print("done")
    except RuntimeError:
      pass
  except KeyboardInterrupt:
    print("logging out")
    loop.run_until_complete(client.logout())
    # cancel all tasks lingering
    print("logged out")
  return count == 0
