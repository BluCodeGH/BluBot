import asyncio
import datetime
import json
from os.path import join as pjoin
from .internal import commands

class main:
  """General bot maintenance."""
  def __init__(self, client):
    self.client = client
    self.logs = []
    self.lognum = 20
    with open(pjoin("data", "keywords.json"),"r") as infile:
      self.kws = json.loads(infile.read())

  async def on_message(self, m):
    self.logs.append(m)
    if len(self.logs) > self.lognum:
      self.logs.pop(0)
    for k in self.kws:
      if k in m.content:
        await self._log()

  async def _log(self):
    out = ""
    for msg in self.logs:
      out += msg.timestamp.strftime("%Y/%m/%d %I:%M:%S %p") + ":" + msg.author.name + ": " + msg.content + "\n"
    self.logs = []
    with open(pjoin("logs", str(datetime.date.today()) + ".log"), "a+b") as outfile:
      outfile.write(out.encode("utf-8"))

  @commands.command("save")
  async def log(self, m, _):
    """Save the last messages to a file.
USAGE:
  log"""
    await self._log()
    await self.client.send_message(m.channel, "Successfully logged the last " + str(len(self.logs)) + " messages.")

  @commands.ownerCommand("kwadd")
  async def addkw(self, m, args):
    """Add a keyword to log
USAGE:
  addkw keyword ...

ARGUMENTS:
  keyword:  The keyword to add."""
    args = args.split()
    self.kws += args
    with open(pjoin("data", "keywords.json"),"w") as outfile:
      outfile.write(json.dumps(self.kws))
    await self.client.send_message(m.channel, "Added keyword successfully.")

  @commands.ownerCommand("kwdel")
  async def delkw(self, m, args):
    """Remove a keyword to log
USAGE:
  delkw keyword

ARGUMENTS:
  keyword:  The keyword to remove."""
    self.kws.pop(self.kws.index(args))
    with open(pjoin("data", "keywords.json"),"w") as outfile:
      outfile.write(json.dumps(self.kws))
    await self.client.send_message(m.channel, "Removed keyword successfully.")
