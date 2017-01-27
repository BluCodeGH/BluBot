import asyncio
from discord import opus
from .internal import perms
from .internal import commands

class main:
  def __init__(self, client):
    self.client = client
    if not opus.is_loaded():
      try:
        opus.load_opus("opus") #windows provides opus
      except OSError: #not on windows
        try:
          opus.load_opus("libopus") #use the provided opus for OSX, linux provides under this name
        except OSError:
          print("Could not load OPUS, therefore voice will work.")
    self.channels = {}
    self.servers = {}

  @commands.command()
  async def play(self, m, args):
    """Search youtube for and play a song
USAGE:
  play query

ARGUMENTS:
  query:  The youtube search query to use."""
    channel = m.server.get_member(m.author.id).voice.voice_channel
    if channel is not None:
      if self.channels.get(channel.id, None) is None:
        if m.server.id in self.servers.keys():
          await self.client.send_message(m.channel, "You must be in the same voice channel as me to control me.")
          return
        vc = voiceChannel()
        await vc.init(self.client, channel, m, self)
        self.channels[channel.id] = vc
        self.servers[m.server.id] = vc
      else:
        vc = self.channels[channel.id]
      await self.client.send_message(m.channel, "Added your request to the queue.")
      try:
        await vc.add(args, m)
      except Exception as e:
        if type(e).__name__.endswith('IndexError'):
          await self.client.send_message(m.channel, "Something went wrong adding your song. Please try again.")
        elif type(e).__name__.endswith('DownloadError'):
          await self.client.send_message(m.channel, "There were no youtube results for that search term. Please try another search.")
        else:
          raise e
    else:
      await self.client.send_message(m.channel, "Err: Please join a voice channel first.")

  @commands.command()
  async def skip(self, m, _):
    """Skip the current song.
USAGE:
  skip"""
    channel = m.server.get_member(m.author.id).voice.voice_channel
    if channel is not None:
      if self.channels.get(channel.id, None) is not None:
        vc = self.channels[channel.id]
        if m.author.id == vc.m.author.id:
          await self.client.send_message(m.channel, "The requester of this song has requested to skip it. Skipping...")
          await vc.next()
        elif await perms.check(m.author.id, "owner"):
          await self.client.send_message(m.channel, "The bot owner has requested to skip this song. Skipping...")
          await vc.next()
        else:
          if m.author.id in vc.skipVotes:
            await self.client.send_message(m.channel, "You have already voted to skip this song.")
            return
          vc.skipVotes.append(m.author.id)
          if len(vc.skipVotes) >= len(channel.voice_members) // 2:
            await self.client.send_message(m.channel, "Half of the people listening have voted to skip this song. Skipping...")
            await vc.next()
          else:
            await self.client.send_message(m.channel, str(len(vc.skipVotes)) + " people have voted to skip the current song, out of a needed " + str(len(channel.voice_members) // 2) + ".")
      elif m.server.id in self.servers.keys():
        await self.client.send_message(m.channel, "You must be in the same voice channel as me to control me.")
      else:
        await self.client.send_message(m.channel, "I am not playing voice in this server right now.")
    else:
      await self.client.send_message(m.channel, "Err: Please join a voice channel first.")

  @commands.adminCommand()
  async def stop(self, m, _):
    """Stop playing voice for the current server
USAGE:
  stop"""
    if m.server.id in self.servers.keys():
      await self.servers[m.server.id].disconnect()
      await self.client.send_message(m.channel, "Stopped playing audio.")

  @commands.command(optional=True)
  async def volume(self, m, args):
    """Set the volume of the current song.
USAGE:
  volume [percentage|up|down]

ARGUMENTS:
  percentage:  10-200, The percentage volume.

  up:  Increase the volume by 10%.

  down Decrease the volume by 10%."""
    channel = m.server.get_member(m.author.id).voice.voice_channel
    if channel is not None:
      if self.channels.get(channel.id, None) is not None:
        vc = self.channels[channel.id]
        if vc.playing is not None:
          if args is None:
            await self.client.send_message(m.channel, "The current volume is " + str(int(vc.playing.volume * 100)) + "%.")
            return
          elif args == "up":
            args = str(int((vc.playing.volume * 100) + 10))
          elif args == "down":
            args = str(int((vc.playing.volume * 100) - 10))
          try:
            num = int(args)
          except ValueError:
            await self.client.send_message(m.channel, "You must input a number between 10 and 200, or 'up' or 'down'.")
            return
          if num < 10 or num > 200:
            await self.client.send_message(m.channel, "Err: Input must be between 10 and 200.")
          else:
            vc.playing.volume = num / 100
            await self.client.send_message(m.channel, "Volume set to " + str(int(vc.playing.volume * 100)) + "%.")
        else:
          await self.client.send_message(m.channel, "Nothing is playing right now.")
      elif m.server.id in self.servers.keys():
        await self.client.send_message(m.channel, "You must be in the same voice channel as me to control me.")
      else:
        await self.client.send_message(m.channel, "I am not playing voice in this server right now.")
    else:
      await self.client.send_message(m.channel, "Err: Please join a voice channel first.")

  @commands.command()
  async def pause(self, m, _):
    """Pauses the current song.
USAGE:
  pause"""
    channel = m.server.get_member(m.author.id).voice.voice_channel
    if channel is not None:
      if self.channels.get(channel.id, None) is not None:
        vc = self.channels[channel.id]
        if vc.playing is not None:
          vc.playing.pause()
          await self.client.send_message(m.channel, "Paused audio.")
        else:
          await self.client.send_message(m.channel, "Nothing is playing right now.")
      elif m.server.id in self.servers.keys():
        await self.client.send_message(m.channel, "You must be in the same voice channel as me to control me.")
      else:
        await self.client.send_message(m.channel, "I am not playing voice in this server right now.")
    else:
      await self.client.send_message(m.channel, "Err: Please join a voice channel first.")

  @commands.command()
  async def resume(self, m, _):
    """Resumes the current song.
USAGE:
  resume"""
    channel = m.server.get_member(m.author.id).voice.voice_channel
    if channel is not None:
      if self.channels.get(channel.id, None) is not None:
        vc = self.channels[channel.id]
        if vc.playing is not None:
          vc.playing.resume()
          await self.client.send_message(m.channel, "Resumed audio.")
        else:
          await self.client.send_message(m.channel, "Nothing is playing right now.")
      elif m.server.id in self.servers.keys():
        await self.client.send_message(m.channel, "You must be in the same voice channel as me to control me.")
      else:
        await self.client.send_message(m.channel, "I am not playing voice in this server right now.")
    else:
      await self.client.send_message(m.channel, "Err: Please join a voice channel first.")

class voiceChannel:
  async def init(self, client, channel, m, parent):
    self.client = client
    self.channel = channel
    self.m = m
    self.parent = parent
    self.queue = []
    self.voice = await self.client.join_voice_channel(self.channel)
    self.playing = None
    self.event = asyncio.Event()
    self.skipVotes = []
    self.task = None
    self.timeoutTask = None

  async def add(self, song, m):
    self.timeoutTask = asyncio.get_event_loop().create_task(self.timeout()) #leave if the search fails
    player = await self.voice.create_ytdl_player(song, ytdl_options={'default_search': 'ytsearch','quiet': True,}, after=self.setEvent)
    self.queue.append((player, m))
    if self.playing is None:
      await self.next()
    elif self.timeoutTask is not None:
      self.timeoutTask.cancel()

  def setEvent(self):
    self.event.set()

  async def nextEvent(self):
    try:
      await self.event.wait()
    except asyncio.CancelledError:
      self.task = None
      self.event.clear()
      return
    self.event.clear()
    self.task = None
    await self.next()

  async def next(self):
    if self.task is not None:
      self.task.cancel()
    if self.timeoutTask is not None:
      self.timeoutTask.cancel()
    if self.playing is not None:
      await self.stop()
    if len(self.queue) > 0:
      self.skipVotes = []
      self.playing = self.queue[0][0]
      self.m = self.queue[0][1]
      dur = str(self.playing.duration // 60) + "m" + str(self.playing.duration % 60) + "s"
      await self.client.send_message(self.m.channel, "Playing *" + self.playing.title + "*, requested by " + self.queue[0][1].author.display_name + ", duration " + dur + ".")
      self.task = asyncio.get_event_loop().create_task(self.nextEvent())
      self.playing.start()
    else:
      self.timeoutTask = asyncio.get_event_loop().create_task(self.timeout())

  async def stop(self):
    if self.playing is not None and self.playing.is_playing():
      self.playing.stop()
    await self.client.send_message(self.m.channel, "Done playing *" + self.playing.title + "*.")
    self.playing = None
    self.queue = self.queue[1:]

  async def timeout(self):
    try:
      await asyncio.sleep(30)
    except asyncio.CancelledError:
      self.timeoutTask = None
      return
    await self.disconnect()

  async def disconnect(self):
    await self.voice.disconnect()
    del self.parent.channels[self.parent.servers[self.m.server.id].channel.id]
    del self.parent.servers[self.m.server.id]
