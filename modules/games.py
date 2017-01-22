import asyncio
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
