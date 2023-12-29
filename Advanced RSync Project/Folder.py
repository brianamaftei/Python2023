import logging
import os
import shutil
import sys
from File import File


class Folder(File):
    def __init__(self, name, data_modified, real_parent=None, temporary_parent=None, type_parent=None):
        super().__init__(name, data_modified, real_parent, temporary_parent, type_parent)
        self.path = self.get_abs_real_path()

    def verify_path(self):
        try:
            if not os.path.isdir(self.path):
                raise OSError(f"The folder path {self.path} is not valid")
            print(f"Folder {self.name} exists")
        except OSError as e:
            print(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        list_of_files = os.listdir(self.path)
        for file in list_of_files:
            print(file)
        print()

    def __str__(self):
        return "Folder: " + self.path

    @classmethod
    def copy_folder(cls, folder, destination):
        try:
            shutil.copytree(folder, destination)
            logging.info(f"Folder {folder} copied from {destination}")
        except shutil.Error as e:
            logging.error(f"Folder copy error: {e}")
            sys.exit(1)

    @classmethod
    def copy_file(cls, file, destination):
        try:
            shutil.copy2(file, destination)
            logging.info(f"File {file} copied from {destination}")
        except shutil.Error as e:
            logging.error(f"Folder copy error: {e}")
            sys.exit(1)
