import asyncio
import subprocess
import os
import sys
from os.path import join as pjoin
import json
from .internal import commands

class main:
  def __init__(self, client):
    self.client = client
    with open(pjoin("data", "replace.json"),"r") as infile:
      self.substitutions, self.subsOn = json.loads(infile.read())

  @commands.command()
  async def screenshot(self, m, _):
    """Takes a screenshot
USAGE:
  screenshot"""
    subprocess.run([sys.executable, os.path.join("modules", "internal", "screenshot.py")], shell=True)
    await self.client.send_file(m.channel, "screenshot.png", content="My screen:")
    os.remove("screenshot.png")

  async def substitute(self, m, _):
    if m.author.id != self.client.user.id:
      return
    res = m.content
    for before, after in self.substitutions.items():
      res = res.replace(before, str(after))
    if res != m.content:
      await self.client.edit_message(m, res)
      m.content = res

  @commands.command(["newSub", "addSubstitution", "addSub"])
  async def newSubstitution(self, m, args):
    """Add a new substitution
USAGE:
  newsubstitution before after

ARGUMENTS:
  before:  The word/characters to be replaced.

  after:  The word/characters to replace it with."""
    args = args.split()
    if len(args) != 2:
      await self.client.send_message(m.channel, "Err: Wrong number of arguments. Must be 2.")
    else:
      self.substitutions[args[0]] = args[1]
      with open(pjoin("data", "replace.json"), "w+") as out:
        out.write(json.dumps((self.substitutions, self.subsOn)))
      await self.client.send_message(m.channel, "Successfully added replacement.")

  @commands.command(["delSub", "remSubstitution", "remSub"])
  async def delSubstitution(self, m, args):
    """Remove a substitution
USAGE:
  delsubstitution substitution

ARGUMENTS:
  substitution:  The before argument of the substitution."""
    args = args.split()
    if len(args) != 1:
      await self.client.send_message(m.channel, "Err: Wrong number of arguments. Must be 1.")
    else:
      if self.substitutions.pop(args[0], None) is not None:
        with open(pjoin("data", "replace.json"), "w+") as out:
          out.write(json.dumps((self.substitutions, self.subsOn)))
        await self.client.send_message(m.channel, "Successfully removed replacement.")
      else:
        await self.client.send_message(m.channel, "That replacement does not exist")

  @commands.command("toggleSub")
  async def toggleSubstitutions(self, m, _):
    """Toggle substitutions
USAGE:
  togglesubstitutions"""
    self.subsOn = not self.subsOn
    with open(pjoin("data", "replace.json"), "w+") as out:
      out.write(json.dumps((self.substitutions, self.subsOn)))
    if self.subsOn:
      await self.client.send_message(m.channel, "Successfully enabled substitutions.")
    else:
      await self.client.send_message(m.channel, "Successfully disabled substitutions.")
