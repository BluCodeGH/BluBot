import json
import asyncio
from os.path import join as pjoin
from . import util

with open(pjoin("data", "perms.json"),"r") as infile:
  permData = json.loads(infile.read())

async def check(uid, perms):
  if isinstance(perms, str):
    perms = [perms]
  for perm in perms:
    if uid in permData.get(perm, []):
      return True
  return False

async def addPerm(perm):
  if permData.get(perm, None) is not None:
    return "Err: Perm already exists."
  else:
    permData[perm] = []
  with open(pjoin("data", "perms.json"), "w+") as out:
    out.write(json.dumps(permData))
  return True

async def delPerm(perm):
  if permData.pop(perm, None) is None:
    return "Err: Perm doesn't exist."
  with open(pjoin("data", "perms.json"), "w+") as out:
    out.write(json.dumps(permData))
  return True

async def getPerms(uid):
  res = []
  for perm, uids in permData.items():
    if uid in uids:
      res += [perm]
  return res

async def allPerms():
  return list(permData.keys())

async def allow(uid, perm):
  if permData.get(perm, None) is None:
    return "Err: Perm doesn't exist."
  elif uid in permData[perm]:
    return "Err: UID already has perm."
  else:
    permData[perm].append(uid)
  with open(pjoin("data", "perms.json"), "w+") as out:
    out.write(json.dumps(permData))
  return True

async def deny(uid, perm):
  if permData.get(perm, None) is None:
    return "Err: Perm doesn't exist."
  elif uid in permData[perm]:
    permData[perm].remove(uid)
  else:
    return "Err: UID doesn't have perm."
  with open(pjoin("data", "perms.json"), "w+") as out:
    out.write(json.dumps(permData))
  return True

async def getIDs(perm):
  if permData.get(perm, None) is None:
    return "Err: Perm doesn't exist."
  else:
    return permData[perm]

async def allIDs():
  ids = []
  for perm in permData:
    for uid in perm:
      if uid not in ids:
        ids.append(uid)
  return ids
