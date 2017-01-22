import sys
import os
import time
import asyncio
import importlib

if os.name == 'posix': #use uvloop if possible
  try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
  except ImportError:
    print("Unable to import uvloop. Reverting to asyncio.")
else:
  print("Uvloop is not supported on this system. Reverting to asyncio.")

initial = sys.modules.copy().keys() #get initial list of modules not to remove

import bluCore

count = 0
while True:
  print("Running bot.")
  isRestart = bluCore.run(count) #run the bot
  print("Bot finished with restart status " + str(isRestart) + ".")
  if isRestart:
    loop_old = asyncio.get_event_loop() #discard the old event loop
    loop_old.close()

    asyncio.set_event_loop(asyncio.new_event_loop())

    for m in [x for x in sys.modules.keys() if x not in initial]: #re-import bluCore and modules it imports
      del sys.modules[m]
    import bluCore

  else:
    print("Exiting")
    sys.exit(0)

  count += 1
  time.sleep(1)
