import os, time
from subprocess import call
from notifications import notify

# TODO: include special treatment for some files depending on metadata
# TODO: check if backup dir exists
# TODO: enable auth using big numbers
# TODO: absolute paths to icons
back_up_drive = "FloppyDisk"
backed_up = False


def backup():
    call('rsync -aE --delete ~/Documents/ "/Volumes/' + back_up_drive + '/BackUps/Documents/"', shell=True)
    call('rsync -aE --delete ~/Pictures/ "/Volumes/' + back_up_drive + '/BackUps/Pictures/"', shell=True)
    call('rsync -aE --delete ~/Desktop/ "/Volumes/' + back_up_drive + '/BackUps/Desktop/"', shell=True)


class InSync:
    tool = "InSync"
    icon = "./Icons/insync.png"
    on_finish_command = "diskutil unmount " + back_up_drive

    def main(self):
        print("InSync started")
        while True:
            if os.path.isdir("/Volumes/" + back_up_drive):

                self.notify("Backing up to: " + back_up_drive, command=None)
                backup()
                self.notify("Backed up to: " + back_up_drive + "; Click to unmount", self.on_finish_command)

                while os.path.isdir("/Volumes/" + back_up_drive):
                    print("not backing up")
                    time.sleep(10)
            time.sleep(5)

    def notify(self, message, command):
        notify(self.tool, message, command, icon=self.icon)
