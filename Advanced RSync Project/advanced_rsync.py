import ftplib
import os
import sys
import tempfile
import zipfile
import time
from datetime import datetime

from Folder import Folder
from Ftp import Ftp
from Zip import Zip
from File import File


def setup_location(location):
    try:
        if location.count(":") < 1:
            raise ValueError("Invalid location type")
        type_location = location.split(":", 1)[0]
        location_path = location.split(":", 1)[1]
        if type_location == "ftp":
            object_of_type = Ftp(location_path)
        elif type_location == "zip":
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))
            object_of_type = Zip(name=name, data_modified=data_modified, real_parent=real_parent)
            object_of_type.verify_path()
        elif type_location == "folder":
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))
            object_of_type = Folder(name=name, data_modified=data_modified, real_parent=real_parent)
            object_of_type.verify_path()
        else:
            raise ValueError("Invalid location type")
        return object_of_type
    except ValueError as e:
        print(type(e), str(e))
        sys.exit(1)


def print_dictionary(dictionary):
    for key in dictionary:
        print("Key: " + key + " Value: " + dictionary[key].__str__())


def object_specific_type(name, current_path, data_modified, real_path):
    if os.path.isdir(os.path.join(current_path, name)):
        return Folder(name=name, data_modified=data_modified, real_parent=real_path,
                      temporary_parent=current_path)
    elif name.split(".")[-1] == "zip":
        return Zip(name=name, data_modified=data_modified, real_parent=real_path,
                   temporary_parent=current_path)
    elif os.path.isfile(os.path.join(current_path, name)):
        return File(name=name, data_modified=data_modified, real_parent=real_path,
                    temporary_parent=current_path)
    else:
        raise ValueError("Invalid file type")


class Sync:
    def __init__(self, arg1, arg2):
        self.location_1 = setup_location(arg1)
        self.location_2 = setup_location(arg2)

        self.location_1_2_files = {}
        self.location_current_files = [File(name="Original", data_modified=datetime.now(), real_parent=""), "unique", 0,
                                       {}]
        if isinstance(self.location_1, Ftp):
            self.connection = self.location_1.connection
        elif isinstance(self.location_2, Ftp):
            self.connection = self.location_2.connection
        else:
            self.connection = None

    def start(self):
        print("First Location: " + self.location_1.__str__())
        print("Second Location: " + self.location_2.__str__())
        self.location_1.print_files()
        self.location_2.print_files()
        while True:
            self.check_differences()
            print_dictionary(self.location_current_files[3])
            self.set_new_state()
            print("Press enter to continue")
            input()

    def location_walk(self, current_path, location_number, location_current_files, location_1_2_files, real_path,
                      type_current_location="folder"):
        try:
            if type_current_location == "ftp":
                list_of_files = self.connection.nlst()
            else:
                list_of_files = os.listdir(current_path)
            if len(location_1_2_files) == 3:
                for file in location_1_2_files[3].keys():
                    if type_current_location == "ftp":
                        key = file.split("/")[-1]
                    else:
                        key = file
                    data_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(current_path, file)))
                    object_of_type = object_specific_type(file, current_path, data_modified, real_path)
                    if file not in list_of_files:
                        location_current_files[3][key] = [object_of_type, "deleted", location_number, {}]
                    else:
                        location_current_files[3][key] = [object_of_type, "unchanged", 0, {}]

            for file in list_of_files:
                key = file
                if type_current_location == "ftp":
                    time_str = self.connection.voidcmd(f'MDTM {file}')[4:]
                    data_modified = datetime.strptime(time_str[:14], '%Y%m%d%H%M%S')
                else:
                    data_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(current_path, file)))
                object_of_type = object_specific_type(file, current_path, data_modified, real_path)
                location_1_2_key_exists = False
                if len(location_1_2_files) < 3 or file not in location_1_2_files[3].keys():
                    if file not in location_current_files[3].keys():
                        location_current_files[3][key] = [object_of_type, "added", location_number, {}]
                    elif location_current_files[3][key][0].data_modified < data_modified:
                        location_current_files[3][key] = [object_of_type, "modified", location_number, {}]
                    elif location_current_files[3][key][0].data_modified == data_modified:
                        location_current_files[3][key] = [object_of_type, "unchanged", 0, {}]
                elif location_1_2_files[3][key][0].data_modified < data_modified:
                    location_current_files[3][key] = [object_of_type, "modified", location_number, {}]
                    print("de fapt de asta ")
                    location_1_2_key_exists = True
                elif location_1_2_files[3][key][0].data_modified == data_modified:
                    location_current_files[3][key] = [object_of_type, "unchanged", 0, {}]
                    location_1_2_key_exists = True

                if location_1_2_key_exists:
                    location_1_2 = location_1_2_files[3][key]
                else:
                    location_1_2 = []

                if isinstance(object_of_type, Folder):
                    self.location_walk(os.path.join(current_path, file), location_number,
                                       location_current_files[3][key],
                                       location_1_2, os.path.join(real_path, file))
                elif isinstance(object_of_type, Zip):
                    temp_dir = tempfile.mkdtemp()
                    print("Asta e calea: " + temp_dir)
                    with zipfile.ZipFile(os.path.join(current_path, file)) as z:
                        z.extractall(temp_dir)
                        for file_info in z.infolist():
                            if os.path.isdir(os.path.join(temp_dir, file_info.filename)):
                                continue
                            extracted_path = os.path.join(temp_dir, file_info.filename)
                            date_modified = time.mktime(file_info.date_time + (0, 0, -1))
                            os.utime(extracted_path, (date_modified, date_modified))

                        for file_info in z.infolist():
                            if os.path.isdir(os.path.join(temp_dir, file_info.filename)):
                                extracted_path = os.path.join(temp_dir, file_info.filename)
                                date_modified = time.mktime(file_info.date_time + (0, 0, -1))
                                os.utime(extracted_path, (date_modified, date_modified))

                    location_current_files[3][key][0].set_temporary_path(temp_dir)
                    self.location_walk(temp_dir, location_number, location_current_files[3][key], location_1_2,
                                       os.path.join(real_path, file))
        except (OSError, zipfile.BadZipFile) as e:
            print(f"Error at checking the differences in {type(location_current_files[0])} {current_path}",
                  type(e), str(e))
            sys.exit(1)
        except ftplib.all_errors as e:
            print(f"Error at checking the differences in {type(location_current_files[0])} {current_path}",
                  type(e), str(e))
            self.connection.quit()
            sys.exit(1)

    def check_differences(self):
        if isinstance(self.location_1, Folder):
            self.location_walk(self.location_1.get_abs_real_path(), 1, self.location_current_files,
                               self.location_1_2_files,
                               self.location_1.get_abs_real_path())
        elif isinstance(self.location_1, Zip):
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(self.location_1.get_location()) as z:
                z.extractall(temp_dir)
            self.location_1.set_temporary_path(temp_dir)
            self.location_walk(temp_dir, 1, self.location_current_files, self.location_1_2_files,
                               self.location_1.get_abs_real_path())
        elif isinstance(self.location_1, Ftp):
            self.location_walk(self.location_1.get_abs_real_path(), 1, self.location_current_files,
                               self.location_1_2_files,
                               self.location_1.get_abs_real_path(), "ftp")

        if isinstance(self.location_2, Folder):
            self.location_walk(self.location_2.get_abs_real_path(), 2, self.location_current_files,
                               self.location_1_2_files,
                               self.location_2.get_abs_real_path())
        elif isinstance(self.location_2, Zip):
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(self.location_2.get_location()) as z:
                z.extractall(temp_dir)
            self.location_2.set_temporary_path(temp_dir)
            self.location_walk(temp_dir, 2, self.location_current_files, self.location_1_2_files,
                               self.location_2.get_abs_real_path())
        elif isinstance(self.location_2, Ftp):
            self.location_walk(self.location_2.get_abs_real_path(), 2, self.location_current_files,
                               self.location_1_2_files,
                               self.location_2.get_abs_real_path(), "ftp")

    def set_new_state(self):
        self.location_1_2_files.clear()
        self.location_1_2_files = self.location_current_files.copy()
        self.location_current_files.clear()
        self.location_current_files = [File(name="Original", data_modified=datetime.now(), real_parent=""), "unique",
                                       0, {}]


def main():
    if len(sys.argv) != 3:
        print("Sunt necesare 3 argumente: advanced_rsync.py <location_1> <location_2>!")
        sys.exit(1)

    print(sys.argv[1], sys.argv[2])
    sync = Sync(sys.argv[1], sys.argv[2])
    sync.start()


main()
