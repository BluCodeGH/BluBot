import asyncio

async def getUser(s, client):
  s = s.strip(" <>@!")
  for server in client.servers:
    res = server.get_member(s)
    if res is None:
      res = server.get_member_named(s)
    if res is not None:
      return res
  return None

async def everyone(client):
  res = []
  for server in client.servers:
    for member in server.members:
      res += member.id
  return res
