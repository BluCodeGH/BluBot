import asyncio
from .internal import commands

class main:
  """General bot maintenance."""
  def __init__(self, client):
    self.client = client

  @commands.adminCommand()
  async def ttspam(self, m, args):
    """Spam text-to-speech.
USAGE:
  ttspam msg [count]

ARGUMENTS:
  msg:  The message to spam.

  count: The number of times to spam msg. Defaults to until its over 1000 chars."""
    try:
      n = int(args.split()[-1])
      m2 = await self.client.send_message(m.channel, "".join(args.split()[:-1] * n), tts=True)
    except ValueError:
      l = len(args) + 1
      n = 2000 // l
      m2 = await self.client.send_message(m.channel, (args.strip(" ") + " ") * n, tts=True)
    await self.client.delete_message(m2)
