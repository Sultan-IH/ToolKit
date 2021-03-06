from threading import Thread
from Tools import InSync, Spotify, Cellarium
import time
from notifications import notify

# TODO: include server backup


tools = [
    #InSync(),
    #Spotify(),
    Cellarium()
]

print('================= Starting main loop =================')
notify('Main', 'ToolKit is up and Running')
time.sleep(1)
for tool in tools:
    time.sleep(1)
    Thread(target=tool.main).start()
