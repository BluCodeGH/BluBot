import asyncio
from .internal import code_async as code
from .internal import commands

class main:
  def __init__(self, client):
    self.client = client
    self.sessions = {}
    self.coreGlobals = {}
    self.coreLocals = {}

  @commands.ownerCommand(optional=True)
  async def repl(self, m, args):
    """Start a repl session.
USAGE:
  repl [prefix]

ARGUMENTS:
  prefix: The prefix to start python commands with. Defaults to `."""
    if self.sessions.get(m.channel.id, None) is None:
      if args is None:
        args = "`"
      sh = Shell(self.client, m, args, glob=self.coreGlobals, loc=self.coreLocals)
      self.sessions[m.channel.id] = sh, args
      await sh.interact(banner="REPL session started.\nThe prefix is " + args, exitmsg="Exiting REPL session...")
      del self.sessions[m.channel.id]
    else:
      await self.client.send_message(m.channel, "Err: There is already a REPL session running in this channel. Use " + self.sessions[m.channel.id][1] + "quit() to quit it.")

  @commands.ownerCommand("quitrepl")
  async def replquit(self, m, _):
    """Quit a repl session.
USAGE:
  replquit"""
    if self.sessions.get(m.channel.id, None) is None:
      await self.client.send_message(m.channel, "Err: There is no REPL session running in this channel.")
    else:
      del self.sessions[m.channel.id]
      await self.client.send_message(m.channel, "REPL session quit.")

class Shell(code.InteractiveConsole):
  def __init__(self, client, message, prefix="`", glob={}, loc={}):
    self.client = client
    self.m = message
    self.prefix = prefix
    code.InteractiveConsole.__init__(self)
    self.locals.update(glob)
    self.locals.update(loc)

  async def write(self, data):
    await self.client.send_message(self.m.channel, "```python\n" + str(data) + "```")

  async def raw_input(self, p=">>>"):
    prompt = await self.client.send_message(self.m.channel, "`" + p + "`")
    def check(m):
      return m.content.startswith(self.prefix) and (not m.content.startswith("```")) and (not m.content == "`" + p + "`")
    inp = await self.client.wait_for_message(author=self.m.author, channel=self.m.channel, check=check)
    res = str(inp.content)
    if res.lstrip(self.prefix).lower() in ["quit()", "quit", "exit()", "exit"]:
      raise EOFError
    if inp.author.id == self.client.user.id:
      await self.client.edit_message(inp, prompt.content + " " + res.strip(self.prefix))
      await self.client.delete_message(prompt)
    return res.strip("`\n")
