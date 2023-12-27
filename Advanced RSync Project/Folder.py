import os
import sys


class Folder:
    def __init__(self, location):
        self.path = location
        self.verify_path()

    def verify_path(self):
        try:
            if os.path.isdir(self.path):
                raise OSError("The folder path is not valid")
        except OSError as e:
            print(type(e), str(e))
            sys.exit(1)
