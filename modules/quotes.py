import asyncio
import random
import json
from os.path import join as pjoin
from .internal import commands

class main():
  """Commands dealing with quotes."""
  def __init__(self, client):
    self.client = client
    with open(pjoin("data", "quotes.json"),"r") as infile:
      self.quotes = json.loads(infile.read())

  @commands.command(optional=True)
  async def quote(self, m, args):
    """Prints a randomly selected quote.
USAGE:
  quote [quote]

ARGUMENTS:
  quote:  The specific quote number to output."""
    if args is None:
      if len(self.quotes) > 1:
        q = random.randint(0, len(self.quotes) - 1)
        print(q)
        await self.client.send_message(m.channel, str(q + 1) + ": " + self.quotes[q])
      else:
        await self.client.send_message(m.channel, "There are no quotes yet.")
    else:
      try:
        await self.client.send_message(m.channel, args + ": " + self.quotes[int(args)])
      except IndexError:
        await self.client.send_message(m.channel, "That quote doesn't exist yet.")

  @commands.command()
  async def allQuotes(self, m, _):
    """Outputs a list of all quotes.
USAGE:
  allQuotes"""
    res = ""
    for i, q in enumerate(self.quotes):
      res +=  str(i + 1) + ": " + q + "\n"
    await self.client.send_message(m.channel, res)

  @commands.adminCommand("quoteAdd", True)
  async def addQuote(self, m, args):
    """Adds a quote.
USAGE:
  addQuote [quote]

ARGUMENTS:
  quote:  The quote to add. Will ask interactively if not specified."""
    if args != None:
      self.quotes.append(args)
    else:
      await self.client.send_message(m.channel, 'What quote should I add?')
      reply = await self.client.wait_for_message(author=m.author)
      self.quotes.append(reply.content)
    with open("quotes.json", "w+") as out:
      out.write(json.dumps(self.quotes))
    await self.client.send_message(m.channel, 'Quote Added Successfully')

  @commands.adminCommand(["quoteDel", "remQuote, quoteRem"], True)
  async def delQuote(self, m, args):
    """Deletes a quote.
USAGE:
  delQuote [quote]

ARGUMENTS:
  quote:  The quote number to delete. Will ask interactively if not specified."""
    if args != None:
      for qu in args.split():
        if int(qu) > -1 and int(qu) < len(self.quotes):
          self.quotes.pop(int(qu))
          await self.client.send_message(m.channel, "Quote removed successfully")
        else:
          await self.client.send_message(m.channel, "Err: quote " + qu + " doesn't exist.")
    else:
      await self.client.send_message(m.channel, 'What quote should I remove?')
      reply = await self.client.wait_for_message(author=m.author)
      if int(reply.content) > -1 and int(reply.content) < len(self.quotes):
        self.quotes.pop(int(reply.content))
        await self.client.send_message(m.channel, "Quote removed successfully")
      else:
        await self.client.send_message(m.channel, "Err: quote " + reply.content + " doesn't exist.")
    with open("quotes.json", "w+") as out:
      out.write(json.dumps(self.quotes))
