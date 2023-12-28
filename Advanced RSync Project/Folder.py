import os
import shutil
import sys
from datetime import datetime
from File import File


class Folder(File):
    def __init__(self, name, data_modified, real_parent, temporary_parent=None):
        super().__init__(name, data_modified, real_parent, temporary_parent)
        self.path = self.get_abs_real_path()
        self.verify_path()

    def verify_path(self):
        try:
            if not os.path.isdir(self.path):
                raise OSError("The folder path is not valid")
            print("Folder exists")
        except OSError as e:
            print(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        list_of_files = os.listdir(self.path)
        for file in list_of_files:
            print(file)
        print()

    def get_location(self):
        return self.path

    def __str__(self):
        return "Folder: " + self.path
