import ctypes
import os
import shutil
import sys


class Installation:
    def __init__(self, os_name, installation_path, python_script):
        self.os_name = os_name
        self.installation_path = installation_path
        # python script to generate executable from
        self.python_script = python_script
        self.env_path = ""

    def install(self):
        if self.os_name == "windows":
            def is_admin():
                try:
                    return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                    return False

            if not is_admin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                installation_code = os.system(f"pyinstaller --hidden-import pydicom.encoders.gdcm "
                                              f"-p assets "
                                              f"--add-data app.ui;{self.installation_path}/ "
                                              # f"--icon=assets/logo.ico "
                                              f"--hidden-import pydicom.encoders.pylibjpeg --onefile {self.python_script} "
                                              f"--distpath {self.installation_path}")
                if installation_code == 0:
                    try:
                        shutil.copyfile("app.ui", f"{self.installation_path}/app.ui")
                        shutil.copytree("assets", f"{self.installation_path}/assets")
                    except shutil.SameFileError:
                        print("Config Files already exist")
                    os.system(f"mkdir {self.installation_path}/temp")
                    os.system(f"mkdir {self.installation_path}/temp/images")
                    print(f"Application Installed Successfully at {self.installation_path}/app")
            else:
                print("Error: administrator permission needed, rerun the program with administrative rights")

        if self.os_name == "linux":
            pass
