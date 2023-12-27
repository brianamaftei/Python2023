import os
import sys
import zipfile
from File import File
from datetime import datetime


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

            with zipfile.ZipFile(self.path, 'r') as z:
                if z.testzip() is not None:
                    raise zipfile.BadZipFile("Bad zip file")
            print("Zipfile is valid")

        except (FileNotFoundError, ValueError, zipfile.BadZipFile) as e:
            print(type(e), str(e))
            sys.exit(1)

    def status_files(self, location_number, location_current_files):
        try:
            with zipfile.ZipFile(self.path) as z:
                for i in z.infolist():
                    name = os.path.basename(i.filename)
                    data_modified = datetime(*i.date_time)
                    if name not in location_current_files:
                        location_current_files[name] = (
                            File(path=i.filename, name=name, data_modified=data_modified, parent=self.path),
                            "added", location_number)
                    else:
                        if location_current_files[name].data_modified > data_modified:
                            location_current_files[name] = (
                                File(path=i.filename, name=name, data_modified=data_modified, parent=self.path),
                                "modified", location_number)
                for file in location_current_files:
                    if file not in z.namelist():
                        location_current_files[file] = (location_current_files[file][0], "deleted", location_number)
        except zipfile.BadZipFile as e:
            print(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        with zipfile.ZipFile(self.path) as z:
            for i in z.infolist():
                file_name = os.path.basename(i.filename)
                print(file_name, end="\n")

    def __str__(self):
        return "Zip: " + self.path
