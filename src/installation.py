import os


class Installation:
    def __init__(self, os_name, installation_path, python_script):
        self.os_name = os_name
        self.installation_path = installation_path
        # python script to generate executable from
        self.python_script = python_script

    def install(self):
        if self.os_name == "windows":
            installation_code = os.system("pyinstaller --onefile " + self.python_script + " --distpath " + self.installation_path + " --hidden-import pydicom")
            print(installation_code)

            # if installation_dir == 0:
