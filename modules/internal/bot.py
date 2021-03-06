import inspect
import asyncio
from discord import Client

class Bot(Client):
  def __init__(self, prefix=".", **kwargs):
    super().__init__(**kwargs)
    self.prefix = prefix
    self.sent = []
    self.sent_log = kwargs.get("sent_log", 25)
    self.isRestart = None

  async def send_message(self, destination, content=None, *, tts=False, embed=None): #add sent message log
    channel_id, guild_id = await self._resolve_destination(destination)
    content = str(content) if content is not None else None
    if len(self.sent) >= self.sent_log:
      self.sent.pop()
    if content is not None:
      self.sent.insert(0, content.strip("\n"))
    if embed is not None:
      embed = embed.to_dict()
    data = await self.http.send_message(channel_id, content, guild_id=guild_id, tts=tts, embed=embed)
    channel = self.get_channel(data.get('channel_id'))
    message = self.connection._create_message(channel=channel, **data)
    if content is not None:
      self.sent[self.sent.index(content.strip("\n"))] = message
    else:
      self.sent.append(message)
    return message

  def was_sent(self, m):
    return m.content in self.sent or m in self.sent
