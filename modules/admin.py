import asyncio
from .internal import commands
from .internal import perms
from .internal import util

class main():
  """Commands dealing with admin management."""
  def __init__(self, client):
    self.client = client

  @commands.adminCommand("adminAdd", True)
  async def addAdmin(self, m, args):
    """Adds an admin.
USAGE:
  addAdmin [username|id|mention] ...

ARGUMENTS:
  username:  The username of a user. Will ask interactively if not specified.

  id:  The id of the a user. Will ask interactively if not specified.

  mention:  A mention of a user. Will ask interactively if not specified."""
    if args != None:
      success = True
      for person in args.split():
        if await util.getUser(person, self.client) is not None:
          person = await util.getUser(person, self.client)
          msg = await perms.allow(person.id, "admin")
          if isinstance(msg, str):
            await self.client.send_message(m.channel, msg)
            success = False
        else:
          await self.client.send_message(m.channel, "Err: Invalid user: " + person)
          success = False
      if success:
        await self.client.send_message(m.channel, 'Admin(s) Added Successfully')
    else:
      await self.client.send_message(m.channel, 'Who should I add as an admin?')
      reply = await self.client.wait_for_message(author=m.author)
      if await util.getUser(reply.content, self.client) is not None:
        person = await util.getUser(reply.content, self.client)
        msg = await perms.allow(person.id, "admin")
        if isinstance(msg, str):
          await self.client.send_message(m.channel, msg)
        else:
          await self.client.send_message(m.channel, 'Admin(s) Added Successfully')
      else:
        await self.client.send_message(m.channel, "Err: Invalid user: " + reply.content)

  @commands.adminCommand(["adminDel", "remAdmin", "adminRem"], True)
  async def delAdmin(self, m, args):
    """Deletes an admin.
USAGE:
  delAdmin [username|id|mention] ...

ARGUMENTS:
  username:  The username of a user. Will ask interactively if not specified.

  id:  The id of a user. Will ask interactively if not specified.

  mention:  A mention of a user. Will ask interactively if not specified."""
    if args != None:
      for person in args.split():
        if await perms.check(m.server.get_member_named(person).id, "admin"):
          msg = await perms.deny(m.server.get_member_named(person).id, "admin")
          if isinstance(msg, str):
            await self.client.send_message(m.channel, msg)
          else:
            await self.client.send_message(m.channel, person + " is no longer an admin.")
        else:
          await self.client.send_message(m.channel, "Err:" + person + " was never an admin.")
    else:
      await self.client.send_message(m.channel, 'Who should I remove as an admin?')
      reply = await self.client.wait_for_message(author=m.author)
      if await perms.check(m.server.get_member_named(reply.content).id, "admin"):
        msg = await perms.deny(m.server.get_member_named(reply.content).id, "admin")
        if isinstance(msg, str):
          await self.client.send_message(m.channel, msg)
        else:
          await self.client.send_message(m.channel, reply.content + " is no longer an admin.")
      else:
        await self.client.send_message(m.channel, "Err:" + reply.content + " was never an admin.")

  @commands.command(["admins", "allAdmins"])
  async def getAdmins(self, m, _):
    """Outputs a list of all admins.
Usage:
  getAdmins"""
    res = ""
    msg = await perms.getIDs("admin")
    if isinstance(msg, str):
      await self.client.send_message(m.channel, msg)
      return
    for admin in msg:
      if m.server.get_member(admin) is not None:
        res += m.server.get_member(admin).display_name + "\n"
      else:
        res += "Not in this server: Id: " + admin + "\n"
    await self.client.send_message(m.channel, "Admins:\n" + res)

  @commands.adminCommand("adminTest")
  async def testAdmin(self, m, _):
    """Test if someone is an admin.
Usage:
  testAdmin"""
    await self.client.send_message(m.channel, m.author.mention + ", you're an admin!")
