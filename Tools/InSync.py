import os, time, yaml
from typing import Tuple
from subprocess import PIPE, Popen, call
from notifications import notify
from datetime import datetime as dt

# TODO: check if backup dir exists
# TODO: absolute paths to icons
timef = '%d %b %H:%M'


class InSync:
    sha256_hash = os.getenv('TOOLKIT_HASH256')
    tool = "InSync"
    icon = "insync.png"
    back_up_folders = ['Documents', 'Pictures', 'Desktop', 'Projects']
    on_finish_command = "diskutil unmount "

    def __init__(self):
        print("InSync tool started")

    def main(self):
        for disk_name in disk_stream():
            print("Disk Stream: ", disk_name)
            path_to_disk = '/Volumes/' + disk_name
            files = os.listdir(path_to_disk)

            if '.insync.yaml' in files and self.auth(path_to_disk):
                self.notify("Backing up to: " + disk_name, command=None)
                self.backup(path_to_disk)
                print("Finished backing up to : ", disk_name)
                self.notify("Backed up to: " + disk_name + "; Click to unmount", self.on_finish_command + disk_name)

    def notify(self, message, command):
        notify(self.tool, message, command, icon=self.icon)

    def backup(self, path_to_disk: str):
        for folder in self.back_up_folders:
            path = path_to_disk + "/BackUps/" + folder + "/"
            if not os.path.isdir(path):
                os.makedirs(path)
            call('rsync -aE --delete ~/' + folder + '/ ' + path,
                 shell=True)
            print("Finished backing up", folder)

    def auth(self, path: str) -> bool:
        with open(path + '/.insync.yaml') as file:
            config = yaml.load(file)
        if config['auth'] == self.sha256_hash:
            return True
        return False


def disk_stream(previous: dict = {}):
    # is a generator that streams changes to the volumes folder
    current = get_disk_metadata()
    if current != previous:  # checks if any changes have been made
        for disk_name in current.keys():
            # new disk mounted or old disk remounted
            if disk_name not in previous.keys() or current[disk_name] != previous[disk_name]:
                previous[disk_name] = current[disk_name]
                yield disk_name
                yield from disk_stream(previous)

    time.sleep(3)
    yield from disk_stream(current)


def get_disk_metadata() -> dict:
    process = Popen("ls -ltr /Volumes | awk '{print $6, $7, $8, $9}'", shell=True, stdout=PIPE)
    out, _ = process.communicate()
    out = out.decode('utf-8').split('\n')
    del out[0], out[-1]
    fout = [nsplit(disk, 3, ' ') for disk in out]
    # creating a dictionary {disk_name : (date_mounted, is_backed_up) }
    disk_metadata = {disk[1]: dt.strptime(disk[0], timef) for disk in fout}
    return disk_metadata


def nsplit(s: str, n: int, c: str) -> Tuple[str, str]:
    # split string s on the nth occurrence of character c
    groups = s.split(c)
    return c.join(groups[:n]), c.join(groups[n:])
