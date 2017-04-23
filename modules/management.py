import asyncio
from os.path import join as pjoin
import json
from .internal import commands
from .internal import util

class main:
  def __init__(self, client):
    self.client = client
    with open(pjoin("data", "filters.json"),"r") as infile:
      self.filters, self.filtersOn = json.loads(infile.read())

  async def filter(self, m):
    if self.filters.get(m.channel.id, None) is None:
      self.filters[m.channel.id] = []
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
      return
    if not self.filtersOn:
      return
    try:
      perms = m.channel.permissions_for(m.server.get_member(self.client.user.id))
    except AttributeError:
      return
    if perms.administrator or perms.manage_messages:
      for f in self.filters[m.channel.id]:
        if " " + f + " " in m.content or m.content[:len(f) + 1] == f + " " or m.content[-1 * (len(f) + 1):] == " " + f:
          await self.client.delete_message(m)
          await self.client.send_message(m.channel, m.author.mention + " Your message has been removed due to the filtering rules the owner of this bot has set in place.")
          return

  async def on_message(self, m):
    await self.filter(m)

  @commands.adminCommand("addFilter")
  async def newFilter(self, m, args):
    """Add a new filter.
USAGE:
  newfilter filter

ARGUMENTS:
  filter:  The word/phrase to be filtered."""
    if self.filters.get(m.channel.id, None) is None:
      self.filters[m.channel.id] = []
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
    try:
      perms = m.channel.permissions_for(m.server.get_member(m.author.id))
    except AttributeError:
      return
    if perms.administrator or perms.manage_messages:
      self.filters[m.channel.id].append(args.strip())
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
      await self.client.send_message(m.channel, "Successfully added filter.")
    else:
      await self.client.send_message(m.channel, "Insufficient permissions to add filters to this channel. You need **manage messages** or **administrator**.")

  @commands.adminCommand("remFilter")
  async def delFilter(self, m, args):
    """Remove a filter.
USAGE:
  delfilter filter

ARGUMENTS:
  filter:  The filter to be removed."""
    if self.filters.get(m.channel.id, None) is None:
      self.filters[m.channel.id] = []
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
      return
    try:
      perms = m.channel.permissions_for(m.server.get_member(m.author.id))
    except AttributeError:
      return
    if perms.administrator or perms.manage_messages:
      try:
        self.filters[m.channel.id].remove(args.strip())
        with open(pjoin("data", "filters.json"), "w+") as out:
          out.write(json.dumps((self.filters, self.filtersOn)))
        await self.client.send_message(m.channel, "Successfully removed filter.")
      except ValueError:
        await self.client.send_message(m.channel, "That filter does not exist")
    else:
      await self.client.send_message(m.channel, "Insufficient permissions to remove filters from this channel. You need **manage messages** or **administrator**.")

  @commands.adminCommand()
  async def toggleFilter(self, m, _):
    """Toggle the filter.
USAGE:
  togglefilter"""
    if self.filters.get(m.channel.id, None) is None:
      self.filters[m.channel.id] = []
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
    try:
      perms = m.channel.permissions_for(m.server.get_member(m.author.id))
    except AttributeError:
      return
    if perms.administrator or perms.manage_messages:
      self.filtersOn = not self.filtersOn
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
      if self.filtersOn:
        await self.client.send_message(m.channel, "Successfully enabled filters.")
      else:
        await self.client.send_message(m.channel, "Successfully disabled filters.")
    else:
      await self.client.send_message(m.channel, "Insufficient permissions to toggle filters on this channel. You need **manage messages** or **administrator**.")

  @commands.command("getFilters")
  async def listFilters(self, m, args):
    """DM all the filters for the current channel.
USAGE:
  listfilters"""
    if self.filters.get(m.channel.id, None) is None:
      self.filters[m.channel.id] = []
      with open(pjoin("data", "filters.json"), "w+") as out:
        out.write(json.dumps((self.filters, self.filtersOn)))
    if self.filters.get(m.channel.id) == []:
      res = "There are no filters for channel " + m.channel.name + "."
    else:
      res = "Filters for channel " + m.channel.name + ":\n"
      for f in self.filters.get(m.channel.id):
        res += "`" + f + "`\n"
    if m.author != self.client.user:
      await self.client.send_message(m.author, res)
      await self.client.send_message(m.channel, m.author.mention + " Please check your DMs.")
    else:
      await self.client.send_message(m.channel, "Err: Unable to DM filters.")

  @commands.adminCommand()
  async def kick(self, m, args):
    """Kick someone(s)
USAGE:
  kick [name|id|mention] ...

ARGUMENTS:
  name:  The name of the person to kick.

  id: the id of the person to kick.

  mention: a mention of the person to kick."""
    try:
      perms = m.channel.permissions_for(m.server.get_member(m.author.id))
    except AttributeError:
      return
    if perms.administrator or perms.kick_members:
      usernames = await util.getUsers(args, self.client, m.server)
      for usr in usernames:
        if isinstance(usr, str):
          res = await util.getUser(usr, self.client)
          if res is None:
            await self.client.send_message(m.channel, "Err: Invalid username " + usr + ".")
          else:
            await self.client.send_message(m.channel, "Err: User " + res.name + " is not in this server.")
          continue
        self.client.kick(usr)
        await self.client.send_message(m.channel, "Kicked " + usr.display_name + ".")
    else:
      await self.client.send_message(m.channel, "You do not have enough permission to kick users. You need **kick members** or **administrator**.")

  @commands.adminCommand()
  async def ban(self, m, args):
    """Ban someone(s)
USAGE:
  ban [name|id|mention] ...

ARGUMENTS:
  name:  The name of the person to kick.

  id: the id of the person to kick.

  mention: a mention of the person to kick."""
    try:
      perms = m.channel.permissions_for(m.server.get_member(m.author.id))
    except AttributeError:
      return
    if perms.administrator or perms.ban_members:
      usernames = await util.getUsers(args, self.client, m.server)
      for usr in usernames:
        if isinstance(usr, str):
          res = await util.getUser(usr, self.client)
          if res is None:
            await self.client.send_message(m.channel, "Err: Invalid username " + usr + ".")
          else:
            await self.client.send_message(m.channel, "Err: User " + res.name + " is not in this server.")
          continue
        self.client.ban(usr)
        await self.client.send_message(m.channel, "Banned " + usr.display_name + ".")
    else:
      await self.client.send_message(m.channel, "You do not have enough permission to ban users. You need **ban members** or **administrator**.")
