import asyncio
from os.path import join as pjoin
import json
from datetime import datetime
from dateutil import tz as dtz
from .internal import commands
from .internal import util

class main:
  """General bot maintenance."""
  def __init__(self, client):
    self.client = client
    with open(pjoin("data", "meetingData.json"),"r") as infile:
      self.data = json.loads(infile.read())

  @commands.adminCommand()
  async def plan(self, m, args):
    """Plan a meeting.
USAGE:
  plan title time, date member,[member...] channel

ARGUMENTS:
  title: The title of the meeting.

  time: The time for the meeting to be scheduled (In *your* time zone). Formatting examples: 04:25PM or 11:06AM.

  date: The date of the meeting in this format: dd/mm/yy eg. 27/04/17 (27 April, 2017)

  member(s): The members to be included in the meeting, separated by commas but *not spaces*.

  channel: The channel in the current server for the meeting to be announced in."""
    title, rest = args.split(" ", 1)
    date, members, channel = rest.rsplit(" ", 2)
    try:
      tz = self.data[m.author.id][0]
      date = datetime.strptime(date, "%I:%M%p, %d/%m/%y").replace(tzinfo=dtz.tzrange("BluCode", tz * 3600, "BluCode")).astimezone(dtz.tzutc())
      for c in m.server.channels:
        if c.name.lower() == channel.lower():
          channel = c
          break
      if isinstance(channel, str):
        raise LookupError
    except Exception as e:
      await self.client.send_message(m.channel, "Err: Invalid input. Contact BluCode for help.")
      raise e
    res = title + " scheduled for " + members.replace(",", ", ") + ".\n"
    for member in members.split(","):
      mem = await util.getUser(member, self.client)
      if mem is None:
        res += "Err: Unable to find " + member + ".\n"
        continue
      try:
        if self.data.get(mem.id, None)[1]:
          mtz = dtz.tzrange("BluCode", self.data.get(mem.id, None)[0] * 3600, "BluCode")
        else:
          mtz = dtz.tzrange("BluCode", self.data.get(mem.id, None)[0] * 3600)
      except:
        res += "Err: Unable to get timezone for " + member + ".\n"
        continue
      d = date.astimezone(mtz).strftime("%I:%M%p, %d %B, %Y")
      res += mem.mention + ": " + d + "\n"
    await self.client.send_message(channel, res)

  @commands.command("reg")
  async def register(self, m, args):
    """Register your time zone.
USAGE:
  register UTC+/-num [DST]

ARGUMENTS:
  UTC+/-num: Your time zone. Format example: UTC-5 or UTC+2.

  DST: Put `False` here if your time zone does not observe daylight savings time (DST), eg `register UTC+0 False`."""
    args = args.split()
    if len(args) not in [1, 2, 3] or not args[0].startswith("UTC") or args[0][3] not in ["+", "-"] or not args[0][4:].isdecimal():
      await self.client.send_message(m.channel, "Err: Invalid syntax. Correct usage: `" + self.data["prefix"] + "register TIMEZONE` where `TIMEZONE` is in the format of `UTC+/-NUMBER`.")
      return
    dst = True
    if len(args) > 1:
      try:
        dst = bool(args[1])
      except ValueError:
        await self.client.send_message(m.channel, "Err: Has DST value must be `True` or `False`.")
    person = m.author
    if len(args) == 3:
      person = await util.getUser(args[2], self.client)
    self.data[person.id] = (int(args[0][3:]), dst)
    with open(pjoin("data", "meetingData.json"), "w") as outfile:
      outfile.write(json.dumps(self.data))
    await self.client.send_message(m.channel, "Successfully registered " + person.mention + "'s timezone as " + args[0] + ".")
