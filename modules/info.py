import asyncio
import random
from os.path import join as pjoin
from yahoo_finance import Share, Currency
from google import search
import discord
from .internal import commands
from .internal import util
from .internal import perms

class main():
  """Commands that give info about things."""
  def __init__(self, client):
    self.client = client

  @commands.command(["google", "search", "lookup"])
  async def searchFor(self, m, args):
    """A google search command.
USAGE:
  searchFor search [count]

ARGUMENTS:
  search:  What to search for.

  count: How many results to return. Defaults to 2 and is capped at 5."""
    i = args.rfind(' ')
    try:
      if i > 0:
        n = int(args[i:])
        args = args[:i]
        if n > 5:
          n = 5
      else:
        n = 2
    except:
      n = 2
    await self.client.send_message(m.channel, "Here are the top " + str(n) + " google results for " + args + '\n')
    msg = await self.client.send_message(m.channel, 'Searching...')
    await self.client.send_typing(m.channel)
    count = 1
    res = ""
    for url in search(str(args)):
      res += url + "\n"
      if count >= n:
        break
      count += 1
    await self.client.edit_message(msg, res)
    await self.client.send_message(m.channel, "Search Finished.")

  @commands.command(["getStock", "stocks", "getStocks"])
  async def stock(self, m, args):
    """Outputs the stock value for one or more stocks.
USAGE:
  stock (code) ...

ARGUMENTS:
  code:  A stock code to look up, eg: 'GOOG'."""
    args = args.split()
    for code in args:
      try:
        s = Share(code)
        await self.client.send_message(m.channel, "The current stock price of " + s.get_name() + " is " + str(s.get_price() + "."))
      except:
        await self.client.send_message(m.channel, "Err: Invalid stock code " + code + ".")

  @commands.command(["getCurrency", "currencies", "getCurrencies"])
  async def currency(self, m, args):
    """Outputs the value of one currency in another.
USAGE:
  currency (code|codea[/]codeb) ...

ARGUMENTS:
  code:  A currency code to be represented in USD, CAD, EUR and PLN.

  codea, codeb:  A currency pair separated by an optional slash."""
    args = args.split()
    res = ""
    for code in args:
      if len(code) == 3:
        compare = ["USD", "CAD", "EUR", "PLN"]
        res = ""
        for c in compare:
          if code != c:
            res += code + c + " "
        await self.currency(m, res[:-1])
      else:
        try:
          curs = code.split("/")
          if len(curs) > 1:
            cur = Currency(curs[0] + curs[1])
          else:
            cur = Currency(code)
            curs = code[:3], code[3:]
          res += "1 " + curs[0] + " is equal to " + cur.get_rate() + " " + curs[1] + ".\n"
        except:
          res += "Err: Invalid currency code " + code + ".\n"
    await self.client.send_message(m.channel, res)

  @commands.command("userData", True)
  async def user(self, m, args):
    """Get data about a user.
USAGE:
  user [username|id|mention] ...

ARGUMENTS:
  username:  The username of a user. Will ask interactively if not specified.

  id:  The id of a user. Will ask interactively if not specified.

  mention:  A mention of a user. Will ask interactively if not specified."""
    if args is None:
      usernames = [await util.getUser(m.author.id, self.client)]
    else:
      usernames = await util.getUsers(args, self.client)
    for usr in usernames:
      if isinstance(usr, str):
        await self.client.send_message(m.channel, "Invalid username " + usr + ".")
        continue
      e = discord.Embed(colour=int('0x%06X' % random.randint(0, 256**3-1), 16))
      e.add_field(name='Username:', value=usr.name)
      if usr.nick is not None:
        e.add_field(name='Nickname:', value=usr.nick)
      else:
        e.add_field(name='Nickname:', value="No nickname set.")
      e.add_field(name='Current Status:', value=str(usr.status).capitalize())
      e.add_field(name='Playing:', value=usr.game)
      e.add_field(name='Joined Server:', value=usr.joined_at.strftime('%m-%d-%Y'))
      e.add_field(name='User Roles:', value=', '.join([i.name.replace('@', '') for i in usr.roles]))
      perm = await perms.getPerms(usr.id)
      if perm == []:
        e.add_field(name='Bot Perm(s):', value="User has no bot roles.")
      else:
        e.add_field(name='Bot Perm(s):', value=', '.join([i for i in perm]))
      e.add_field(name='Account Created:', value=usr.created_at.strftime('%m-%d-%Y'))
      if usr.avatar is None:
        avatar = usr.default_avatar_url
      else:
        avatar = usr.avatar_url
      e.set_author(name=usr.display_name, icon_url=avatar)
      await self.client.send_message(m.channel, embed=e)

  @commands.command("help", True)
  async def h(self, m, args):
    """Help. Use help [command] for more info.
USAGE:
  help [command] ...

ARGUMENTS:
  command:  The name of a command to get more detailed info on."""
    if args is None:
      e = discord.Embed(title="General Help", colour=int('0x%06X' % random.randint(0, 256**3-1), 16))
      for cName, cmds in commands.commandHelpClass.items():
        res = ""
        for cmd, hlp in cmds.items():
          if len(hlp) == 2:
            res += "• **" + cmd + "**: " + hlp[0] + "\n"
        e.add_field(name=cName.capitalize() + ":", value=res, inline=False)
      e.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
      if self.client.user == m.author:
        await self.client.send_message(m.channel, "Unable to dm help, as this is a user bot.")
        await self.client.send_message(m.channel, embed=e)
      else:
        await self.client.send_message(m.channel, "I have dm'd you my help.")
        await self.client.send_message(m.author, embed=e)
    else:
      for name in args.split():
        comm = name.strip(".")
        if comm == "":
          comm = "NOT A COMMAND"
        if comm in commands.commandHelp.keys():
          hlp = commands.commandHelp[comm][0] + "\n" + commands.commandHelp[comm][1]
        else:
          await self.client.send_message(m.channel, "Err: Unknown command "  + name + ".")
          return
        e = discord.Embed(colour=int('0x%06X' % random.randint(0, 256**3-1), 16))
        e.add_field(name=comm, value=hlp)
        e.set_author(name=m.author.display_name, icon_url=m.author.avatar_url)
        if self.client.user == m.author:
          await self.client.send_message(m.channel, "Unable to dm help, as this is a user bot.")
          await self.client.send_message(m.channel, embed=e)
        else:
          await self.client.send_message(m.channel, "I have dm'd you my help.")
          await self.client.send_message(m.author, embed=e)
