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

async def getUsers(s, client):
  inputs = s.split()
  usernames = []
  i = 0
  inprog = ""
  while i < len(inputs):
    inprog += inputs[i].strip("<>@!") + " "
    print(inprog)
    res = await getUser(inprog, client)
    if res is not None:
      usernames.append(res)
      inprog = ""
      inputs = inputs[i+1:]
      i = -1
    elif i + 1 == len(inputs):
      usernames.append(inputs[0])
      i = -1
      inputs = inputs[1:]
      inprog = ""
    i += 1
  return usernames

async def everyone(client):
  res = []
  for server in client.servers:
    for member in server.members:
      res += member.id
  return res
