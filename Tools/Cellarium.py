import os, yaml
from subprocess import call
from Tools.InSync import disk_stream
from notifications import notify


class Cellarium:
    """
    Checks the Cellarium folder in the ~ directory, then compresses the files there and moves them into
    """
    sha256_hash = os.getenv('TOOLKIT_HASH256')
    path_to_storage = '/Users/' + os.getenv('USER') + '/Cellarium/'
    tool = 'Cellarium'
    icon = 'cellarium.png'

    def main(self):
        print('Cellarium tool started')

        for disk_name in disk_stream():

            path_to_disk = '/Volumes/' + disk_name
            disk_files = os.listdir(path_to_disk)

            _, directories, files = next(os.walk(self.path_to_storage))
            files.remove('.DS_Store')

            if directories is not [] or files is not []:  # we have something to store

                if '.insync.yaml' in disk_files and self.auth(path_to_disk):  # we have an authed disk mounted
                    for folder in directories:
                        command = (
                                "zip -r " + path_to_disk + "/Cellarium/" + folder + ".zip "
                                + self.path_to_storage + folder)
                        print(command)
                        call(command, shell=True)
                        call('rm -rf ' + self.path_to_storage + folder, shell=True)

                    for file in files:
                        command = (
                                "zip " + path_to_disk + "/Cellarium/" + file + ".zip "
                                + self.path_to_storage + file)
                        print(command)
                        call(command, shell=True)
                        call('rm ' + self.path_to_storage + file, shell=True)
                    self.notify("Housekeeping done.")

    def notify(self, message, command=None):
        notify(self.tool, message, command, icon=self.icon)

    def auth(self, path: str) -> bool:
        with open(path + '/.insync.yaml') as file:
            config = yaml.load(file)
        if config['auth'] == self.sha256_hash:
            return True
        return False
