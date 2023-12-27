import os
import sys


class Folder:
    def __init__(self, location):
        self.path = location
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

    def __str__(self):
        return "Folder: " + self.path
