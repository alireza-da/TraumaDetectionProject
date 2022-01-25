import ctypes
import os
import shutil
import sys
import logging


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
                except Exception as ex:
                    logging.error(ex)
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
                        shutil.copyfile("page2.ui", f"{self.installation_path}/page2.ui")
                        shutil.copyfile("history.ui", f"{self.installation_path}/history.ui")
                        shutil.copytree("assets", f"{self.installation_path}/assets")
                        shutil.copytree("../MASKS_DICOM", f"{self.installation_path}/MASKS_DICOM")
                        shutil.copytree("../PATIENT_DICOM", f"{self.installation_path}/PATIENT_DICOM")
                    except (shutil.SameFileError, FileExistsError):
                        logging.info("Config Files already exist")
                    try:
                        os.makedirs(f"{self.installation_path}/temp")
                        os.makedirs(f"{self.installation_path}/temp/images")

                    except (FileExistsError, FileNotFoundError) as e:
                        logging.error(e)
                        logging.info("Failed to create temp dir")

                    logging.info(f"Application Installed Successfully at {self.installation_path}/app")
            else:
                logging.error("Error: administrator permission needed, rerun the program with administrative rights")

        if self.os_name == "linux":
            installation_code = os.system(f"pyinstaller --hidden-import pydicom.encoders.gdcm "
                                          f"-p assets "
                                          f"--add-data app.ui;{self.installation_path}/ "
                                          # f"--icon=assets/logo.ico "
                                          f"--hidden-import pydicom.encoders.pylibjpeg --onefile {self.python_script} "
                                          f"--distpath {self.installation_path}")
            if installation_code == 0:
                try:
                    shutil.copyfile("app.ui", f"{self.installation_path}/app.ui")
                    shutil.copyfile("page2.ui", f"{self.installation_path}/page2.ui")
                    shutil.copyfile("history.ui", f"{self.installation_path}/history.ui")
                    shutil.copytree("assets", f"{self.installation_path}/assets")
                except (shutil.SameFileError, FileExistsError):
                    logging.info("Config Files already exist")
                try:
                    os.makedirs(f"{self.installation_path}/temp")
                    os.makedirs(f"{self.installation_path}/temp/images")

                except FileExistsError as e:
                    logging.error(e)
                    logging.info("Failed to create temp dir")

                print(f"Application Installed Successfully at {self.installation_path}/app")
