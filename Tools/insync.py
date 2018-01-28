import os, time
from subprocess import call
from notifications import notify

# TODO: include special treatment for some files depending on metadata
# TODO: check if backup dir exists
# TODO: enable auth using big numbers
# TODO: absolute paths to icons
back_up_drive = "FloppyDisk"
backed_up = False


class InSync:
    tool = "InSync"
    icon = "insync.png"
    back_up_folders = ['Documents', 'Pictures', 'Desktop', 'Projects']
    on_finish_command = "diskutil unmount " + back_up_drive

    def main(self):
        print("InSync started")
        while True:
            if os.path.isdir("/Volumes/" + back_up_drive):

                self.notify("Backing up to: " + back_up_drive, command=None)
                self.backup()
                self.notify("Backed up to: " + back_up_drive + "; Click to unmount", self.on_finish_command)

                while os.path.isdir("/Volumes/" + back_up_drive):
                    print("not backing up")
                    time.sleep(10)
            time.sleep(5)

    def notify(self, message, command):
        notify(self.tool, message, command, icon=self.icon)

    def backup(self):

        for folder in self.back_up_folders:
            path = "/Volumes/" + back_up_drive + "/BackUps/" + folder + "/"
            if not os.path.isdir(path):
                os.makedirs(path)
            call('rsync -aE --delete ~/' + folder + '/ ' + path,
                 shell=True)
