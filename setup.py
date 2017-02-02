from os.path import join as pjoin
import os
import sys
import pickle
import subprocess

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
    twofa = str(input("Will you use your token to log in? (token only if you use 2fa) [Y/N] "))
  if twofa in yes:
    token = str(input("What is your user token? "))
  else:
    email = str(input("What is the email address associated with your account? "))
    pwrd = str(input("What is your discord password? "))
else:
  token = str(input("What is the token of the bot account? "))
prefix = str(input("What should the command prefix for the bot be? "))
if userbot in yes:
  uid = "replaceMe"
  btype = "s"
else:
  uid = str(input("What is your discord id? "))
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
with open(pjoin("data", "replace.pkl"), "w+") as out:
  out.write(pickle.dumps([{}, True]))
with open(pjoin("data", "filters.json"), "w+") as out:
  out.write('[{}, true]')

print("Data files setup, now installing modules (this may take a while).")

if userbot in yes:
  out = subprocess.run([sys.executable, "-m", "pip", "install", "-U", "-r", "selfbot_requirements.txt"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
else:
  out = subprocess.run([sys.executable, "-m", "pip", "install", "-U", "-r", "bot_requirements.txt"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
if out.returncode != 0:
  print("Error in automatic general pip, please manually install requirements.txt.")
  print("Automatic general pip output:")
  print(out.stdout)

if os.name == 'posix':
  out = subprocess.run([sys.executable, "-m", "pip", "install", "uvloop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
  if out.returncode != 0:
    print("Error in automatic uvloop pip, please manually install uvloop if possible (not necessary).")
    print("Automatic uvloop pip output:")
    print(out.stdout)

print("Setup finished successfully.")
