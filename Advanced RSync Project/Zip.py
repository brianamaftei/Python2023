import os
import sys
import zipfile


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

    def print_files(self):
        with zipfile.ZipFile(self.path) as z:
            for i in z.infolist():
                file_name = os.path.basename(i.filename)
                print(file_name, end="\n")

    def __str__(self):
        return "Zip: " + self.path
