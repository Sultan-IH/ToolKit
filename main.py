from threading import Thread
from Tools import insync
import time
from notifications import notify

# TODO: include server backup

# TODO: include encryption

tools = [
    insync.InSync()
]

print('Starting main loop')
notify('Main', 'ToolKit is up and Running')
time.sleep(1)
for tool in tools:
    Thread(target=tool.main).start()
