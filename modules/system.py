import os
import json
import subprocess
import datetime
import asyncio
from .internal import commands

class main:
  """General bot maintenance."""
  def __init__(self, client):
    self.client = client
    with open(os.path.join("data","botData.json"),"r") as infile:
      data = json.loads(infile.read())
      self.startChars = data[-1]
    self.isRestart = None
    self.latencyMsg = None
    self.latencyTime = None

  @commands.command()
  async def test(self, m, _):
    """A simple test function
USAGE:
  test"""
    await self.client.send_message(m.channel, 'Everything is looking good, ' + m.author.mention)

  @commands.ownerCommand("quit")
  async def q(self, m, _):
    """Quit the bot
USAGE:
  quit"""
    await self.client.send_message(m.channel, "Logging out and quitting.")
    await self.client.logout()

  @commands.ownerCommand()
  async def restart(self, m, _):
    """Quit the bot
USAGE:
  quit"""
    self.isRestart = m
    await self.client.send_message(m.channel, "Restarting.")
    await self.client.logout()

  @commands.adminCommand("pull")
  async def update(self, m, _):
    """Updates the bot with code from the GitHub repo.
USAGE:
  update"""
    await self.client.send_message(m.channel, "Trying to self-update via the GitHub repo.")
    out = subprocess.run("git pull -v", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
    if out.returncode != 0:
      await self.client.send_message(m.channel, "Err: Update Error")
      if out.stdout != "":
        print(out.stdout, type(out.stdout))
        await self.client.send_message(m.channel, "```" + out.stdout + "```")
      else:
        await self.client.send_message(m.channel, "```No output```")
      await self.client.send_message(m.channel, "Aborting. Not restarting.")
    else:
      if out.stdout.split('\n')[-2:][0] == "Already up-to-date.":
        await self.client.send_message(m.channel, "Up to date, not restarting.")
      else:
        await self.client.send_message(m.channel, "Git output:\n```" + out.stdout.split("\n", 3)[-1] + "```")
        await self.client.send_message(m.channel, "Update successful, now restarting")
        await self.restart(m, None)

  @commands.adminCommand("push")
  async def commit(self, m, args):
    """Commit and push the current code to the GitHub repo.
USAGE:
  commit message

ARGUMENTS:
  message:  The commit message."""
    await self.client.send_message(m.channel, "Trying to commit and push to the GitHub repo.")
    out = subprocess.run(["git", "commit", "-a", "-m", args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
    if out.returncode != 0:
      await self.client.send_message(m.channel, "Err: Update Error")
      await self.client.send_message(m.channel, "```" + out.stdout + "```")
      await self.client.send_message(m.channel, "Aborting.")
    else:
      await self.client.send_message(m.channel, "Git commit output:\n```" + out.stdout + "```")
      out = subprocess.run(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
      if out.returncode != 0:
        await self.client.send_message(m.channel, "Err: Update Error")
        await self.client.send_message(m.channel, "```" + out.stdout + "```")
        await self.client.send_message(m.channel, "Aborting.")
      else:
        await self.client.send_message(m.channel, "Git push output:\n```" + out.stdout + "```")
        await self.client.send_message(m.channel, "Git commit and push successful.")

  @commands.adminCommand("startChar")
  async def prefix(self, m, args):
    """Change the command prefix for the bot.
USAGE:
  prefix chars

ARGUMENTS:
  chars:  The character(s) to set the prefix to."""
    with open(os.path.join("data", "botData.json"),"r") as inf:
      botData = json.loads(inf.read())
    self.startChars = args.split()[0]
    with open(os.path.join("data", "botData.json"), "w+") as out:
      out.write(json.dumps([botData[0], self.startChars]))
    await self.client.send_message(m.channel, "The command prefix has been updated to `" + self.startChars + "`")

  @commands.adminCommand(optional=True)
  async def latency(self, m, args):
    """Will perform a latency test.
USAGE:
  latency"""
    if self.latencyTime is None:
      self.latencyTime = datetime.datetime.now()
      self.latencyMsg = await self.client.send_message(m.channel, "The current latency is")
    else:
      if args is None:
        await self.client.send_message(m.channel, "Latency test in progress, please wait for it to finish.")
      else:
        diff =  datetime.datetime.now() - self.latencyTime
        await asyncio.sleep(0.5)
        await self.client.edit_message(self.latencyMsg, "The current latency is `" + str(diff.total_seconds() * 1000) + "`ms.")
        self.latencyTime = None

  async def say(self, m, msg):
    await self.client.send_message(m.channel, msg)

  @commands.ownerCommand("run")
  async def exec(self, m, args):
    """Runs python code.
USAGE:
  exec code

ARGUMENTS:
  code:  Python code to run."""
    try:
      exec(args)
    except Exception as e:
      res = "```" + str(type(e).__name__) + ": " + str(e).capitalize() + ".```"
      await self.client.send_message(m.channel, res)
