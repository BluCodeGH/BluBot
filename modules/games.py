import asyncio
import socket
import json
import struct
import random
import discord
from .internal import commands
from .gameLogic.BlackJack import BlackJack
from .gameLogic.War import War

class main():
  """Some simple games."""
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def blackJack(self, m, _):
    """Play blackJack against the computer.
USAGE:
  blackJack"""
    await self.client.change_presence(game=discord.Game(name="BlackJack"))
    game = BlackJack()
    await self.client.send_message(m.channel, "You have started a game of BlackJack!")
    game.startGame()
    await self.client.send_message(m.channel, game.flipOneCard())
    lose = False
    while not lose:
      await self.client.send_message(m.channel, "These are your cards" + game.getCards())
      if game.getPlayerScore() == 21:
        await self.client.send_message(m.channel,"21!!!! :100: :100: :100: :100:   ")
        break
      await self.client.send_message(m.channel, "Type 'Y' hit or 'N' to stay.")
      reply = await self.client.wait_for_message(author=m.author)
      if reply.content == "Y":
        game.hit()
      elif reply.content == "N":
        await self.client.send_message(m.channel,game.finishGame())
        break
      if game.getPlayerScore() > 21:  # in case player tried to keep playing with an illegal score
        await self.client.send_message(m.channel, "You have gone over 21 and lost!!!!")
        lose = True
    await self.client.change_presence(game=None)

  @commands.command()
  async def war(self, m, _):
    """Play war.
USAGE:
  war"""
    g = War()
    await self.client.send_message(m.channel, "You have started a game of War!")
    g.startGame()
    await asyncio.sleep(1)
    await self.client.send_message(m.channel, 'You were delt: \n' + str(g.getPlayerCards()) + '\n')
    await asyncio.sleep(1)
    await self.client.send_message(m.channel, 'The dealer was delt: \n' + str(g.getDealerCards()) + '\n')
    await asyncio.sleep(1)
    await self.client.send_message(m.channel, g.finishGame())

  def popint(self, s):
    acc = 0
    shift=0
    b = ord(s.recv(1))
    while b & 0x80:
      acc = acc | ((b&0x7f)<<shift)
      shift = shift + 7
      b = ord(s.recv(1))
    return (acc)|(b<<shift)

  def pack_varint(self, d):
    return bytes([(0x40*(i!=d.bit_length()//7))+((d>>(7*(i)))%128) for i in range(1+d.bit_length()//7)])

  def pack_data(self, d):
    return self.pack_varint(len(d)) + d

  def get_info(self, host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(self.pack_data(bytes(2)+self.pack_data(bytes(host,'utf8'))+struct.pack('>H',port)+bytes([1]))+bytes([1,0]))
    self.popint(s)   # Packet length
    self.popint(s)   # Packet ID
    l,d = self.popint(s),bytes()
    while len(d) < l: d += s.recv(1024)
    s.close()
    return json.loads(d.decode('utf8'))

  @commands.command("server")
  async def mc(self, m, args):
    """Get information about a minecraft server
USAGE:
  mc [ip[:port]]

ARGUMENTS:
  ip:  The ip of a minecraft server.

  port: The server's port. Defaults to 25565."""
    if len(args.split(":")) > 1:
      s, p = args.split(":")
      p = int(p)
    else:
      s = args
      p = 25565
    data=self.get_info(s, p)
    desc = data['description'] if isinstance(data["description"], str) else data["description"]["text"]
    e = discord.Embed(title=s+":"+str(p),description=desc,colour=int('0x%06X' % random.randint(0, 256**3-1), 16))
    e.add_field(name="Total Players",value=str(data['players']['online']) + " / " + str(data['players']['max']))
    if data["players"].get("sample", None) is not None:
      players = ""
      if len(data['players']['sample']) > 1:
        for i, p in enumerate(data['players']['sample'][:10]):
          if i + 1 == len(data['players']['sample']):
            players += " and " + p["name"]
          else:
            players += ", " + p["name"]
        if len(data['players']['sample']) > 10:
          players += "..."
        e.add_field(name="Players",value=players[2:])
      elif len(data["players"]["sample"]) > 0:
        players = "  " + data['players']['sample'][0]["name"]
        e.add_field(name="Players",value=players)
      else:
        e.add_field(name="Players",value="No sample given.")
    e.add_field(name="Version",value=data["version"]["name"])
    if data.get("modinfo", None) is not None and data['modinfo']['modList'] != []:
      mods = ""
      for i, mod in enumerate(data['modinfo']['modList']):
        if i + 1 == len(data['modinfo']['modList']):
          mods += " and " + mod["modid"].capitalize() + " " + mod["version"]
        else:
          mods += ", " + mod["modid"].capitalize() + " " + mod["version"]
      e.add_field(name="Mods",value=mods[2:])
    print(e.to_dict())
    await self.client.send_message(m.channel, embed=e)
