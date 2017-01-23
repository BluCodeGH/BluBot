from os.path import join as pjoin
import os

yes = ["y", "Y"]
valid = yes + ["n", "N"]
userbot = None
twofa = None
token = None
email = None
pwrd = None

print("Welcome to the setup for BluBot.\nI first need some information in order to run.")
while userbot not in valid:
  userbot = str(input("Will you use your account for this bot? [Y,N] "))
if userbot in yes:
  while twofa not in valid:
    twofa = str(input("Do you use two factor authentication? [Y/N] "))
  if twofa in yes:
    token = str(input("What is your user token? "))
  else:
    email = str(input("What is the email address associated with your account? "))
    pwrd = str(input("What is your discord password? "))
else:
  token = str(input("What is the token of the bot account? "))
prefix = str(input("What should the command prefix for the bot be? "))
uid = str(input("What is your discord id? "))

if userbot in yes:
  btype = "s"
else:
  btype = "b"

if not os.path.exists("data"):
  os.makedirs("data")

if token is None:
  with open(pjoin("data", "botData.json"), "w+") as out:
    out.write('["' + email + '", "' + pwrd + '", "s", "' + prefix + '"]')
else:
  with open(pjoin("data", "botData.json"), "w+") as out:
    out.write('["' + token + '", "' + btype + '", "' + prefix + '"]')
with open(pjoin("data", "perms.json"), "w+") as out:
  out.write('{"owner":["' + uid + '"], "admin":[]}')
with open(pjoin("data", "quotes.json"), "w+") as out:
  out.write('[]')
with open(pjoin("data", "replace.json"), "w+") as out:
  out.write('[{}, true]')
with open(pjoin("data", "filters.json"), "w+") as out:
  out.write('[{}, true]')

print("Setup finished successfully.")
