import os
import shutil
import sys
from datetime import datetime
from File import File


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

    def status_files(self, location_number, location_current_files, location_1_2_files):
        try:
            list_of_files = os.listdir(self.path)

            for file in location_1_2_files:
                if file not in list_of_files:
                    location_current_files[file] = (location_1_2_files[file][0], "deleted", location_number)
                else:
                    location_current_files[file][1] = (
                        location_1_2_files[file][0], "unchanged", location_1_2_files[file][2])

            for file in list_of_files:
                path = file
                data_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(self.path, file)))
                if file not in location_1_2_files:
                    if file not in location_current_files:
                        location_current_files[file] = (
                            File(path=path, name=file, data_modified=data_modified, parent=self.path),
                            "added", location_number)
                    else:
                        if location_current_files[file][0].data_modified < data_modified:
                            location_current_files[file] = (
                                File(path=path, name=file, data_modified=data_modified, parent=self.path),
                                "modified", location_number)
                        elif location_current_files[file][0].data_modified == data_modified:
                            location_current_files[file] = (
                                File(path=path, name=file, data_modified=data_modified, parent=self.path),
                                "unchanged", location_number)

                elif location_1_2_files[file][0].data_modified < data_modified:
                    location_current_files[file] = (
                        File(path=path, name=file, data_modified=data_modified, parent=self.path),
                        "modified", location_number)

        except OSError as e:
            print("Error at checking the differences in folder",type(e), str(e))
            sys.exit(1)



    def __str__(self):
        return "Folder: " + self.path
