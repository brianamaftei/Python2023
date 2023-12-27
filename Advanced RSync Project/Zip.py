import os
import sys


class Zip:
    def __init__(self, path):
        self.path = path
        self.verify_path()

    def verify_path(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError("Path does not exist")
            if not os.path.isfile(self.path) or not self.path.endswith(".zip"):
                raise ValueError("Invalid zip location")
            print("Zipfile exists")
        except (FileNotFoundError, ValueError) as e:
            print(type(e), str(e))
            sys.exit(1)
