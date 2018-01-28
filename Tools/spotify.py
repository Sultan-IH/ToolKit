import os, time
from subprocess import call
from notifications import notify


class Spotify:
    tool = "Spotify Tool"
    icon = "spotify.png"
    path_to_app = '~/Projects/ToolKit/Tools/Spotify-API/app.js'
    path_to_node = '/Users/DevAccount/.nvm/versions/node/v6.5.0/bin/node '

    def main(self):
        print("Spotify tool started")
        call(self.path_to_node + self.path_to_app, shell=True)

    def notify(self, message, command):
        notify(self.tool, message, command, icon=self.icon)
