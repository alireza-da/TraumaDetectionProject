import os


class Installation:
    def __init__(self, os_name, installation_path, python_script):
        self.os_name = os_name
        self.installation_path = installation_path
        # python script to generate executable from
        self.python_script = python_script
        self.env_path = ""

    def install(self):
        if self.os_name == "windows":
            installation_code = os.system("pyinstaller " +
                                          # "--add-data " + "../assets:. " +
                                          "--onefile " + "--hidden-import pydicom.encoders.gdcm "
                                          "--hidden-import pydicom.encoders.pylibjpeg " +
                                          self.python_script + " --distpath " + self.installation_path)
            print(installation_code)

