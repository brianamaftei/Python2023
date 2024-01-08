import ftplib
import os
import sys
import zipfile
from datetime import datetime, timedelta

from File import File
from Folder import Folder
from FtpLocation import FtpLocation
from Zip import Zip


def setup_location(location):
    try:
        if location.count(":") < 2:
            raise ValueError("Invalid location type format")
        type_location = location.split(":", 1)[0]
        location_path = location.split(":", 1)[1]
        if type_location == "ftp":
            object_of_type = FtpLocation(location_path)
        elif type_location == "zip":
            Zip.verify_path(location_path)
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))

            object_of_type = Zip(name=name, data_modified=data_modified, real_parent=real_parent)
        elif type_location == "folder":
            Folder.verify_path(location_path)
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))
            object_of_type = Folder(name=name, data_modified=data_modified, real_parent=real_parent)
            object_of_type.set_temporary_abs_path(location_path)
        else:
            raise ValueError("Invalid location type")
        return object_of_type
    except ValueError as e:
        print(type(e), str(e))
        sys.exit(1)


def print_dictionary(dictionary, level=0):
    for key in dictionary.items():
        print("Key: " + key[0] + " Value: " + str(key[1]))


def print_list(item, level=0):
    print(item[0].name + " " + item[1] + " " + str(item[2]))
    print(" " * level, end="")
    print_dictionary(item[3], level + 1)


def object_specific_type(name, current_path, data_modified, real_path, type_current_location, relative_path, connection,
                         type_location):
    if (type_location != "ftp" and os.path.isdir(os.path.join(current_path, name)) or
            (type_location == "ftp" and FtpLocation.is_directory(connection, current_path + name))):
        return Folder(name=name, data_modified=data_modified, real_parent=real_path,
                      temporary_parent=current_path, type_parent=type_current_location, relative_path=relative_path)
    elif name.split(".")[-1] == "zip":
        return Zip(name=name, data_modified=data_modified, real_parent=real_path,
                   temporary_parent=current_path, type_parent=type_current_location, relative_path=relative_path)
    elif (type_location != "ftp" and os.path.isfile(os.path.join(current_path, name)) or
          (type_location == "ftp" and FtpLocation.is_file(connection, current_path + name))):
        return File(name=name, data_modified=data_modified, real_parent=real_path,
                    temporary_parent=current_path, type_parent=type_current_location, relative_path=relative_path)
    else:
        raise ValueError("Invalid file type " + str(os.path.join(current_path, name)))


def get_type(object_):
    if isinstance(object_, File):
        return "file"
    elif isinstance(object_, Folder):
        return "folder"
    elif isinstance(object_, Zip):
        return "zip"
    elif isinstance(object_, FtpLocation):
        return "ftp"


class Sync:
    def __init__(self, arg1, arg2):
        self.location_1 = setup_location(arg1)
        self.location_2 = setup_location(arg2)
        self.location_1_2_files = [
            File(name="Original", data_modified=datetime.now(), real_parent="", relative_path=""),
            "unique", 0, {}]
        if isinstance(self.location_1, FtpLocation):
            self.connection_1 = self.location_1.connection
        else:
            self.connection_1 = None

        if isinstance(self.location_2, FtpLocation):
            self.connection_2 = self.location_2.connection
        else:
            self.connection_2 = None

    def start(self):
        print("First Location: " + self.location_1.__str__())
        print("Second Location: " + self.location_2.__str__())
        self.location_1.print_files()
        self.location_2.print_files()
        while True:
            try:
                location_current_files_1 = [self.location_1, "unique", 0, {}]
                location_current_files_2 = [self.location_2, "unique", 0, {}]
                new_location_1_2_files = [
                    File(name="Original", data_modified=datetime.now(), real_parent="", relative_path=""),
                    "unique", 0, {}]
                self.check_differences(location_current_files_1, location_current_files_2)
                self.compare_location_current_files(self.location_1_2_files, location_current_files_1,
                                                    location_current_files_2, new_location_1_2_files)

                self.location_1_2_files.clear()
                self.location_1_2_files = new_location_1_2_files.copy()
                print("Location 1")
                print_dictionary(location_current_files_1[3])
                print("Location 2")
                print_dictionary(location_current_files_2[3])
                print("Location 1 2")
                print_dictionary(self.location_1_2_files[3])

                self.recursive_balance_differences(self.location_1_2_files, self.location_1, self.location_2)

                self.remove_deleted_elements(self.location_1_2_files)

                if isinstance(self.location_1, Zip):
                    Zip.compress_folder_into_zip(self.location_1.get_temporary_abs_path(),
                                                 self.location_1.get_location())

                if isinstance(self.location_2, Zip):
                    Zip.compress_folder_into_zip(self.location_2.get_temporary_abs_path(),
                                                 self.location_2.get_location())

                print("Press enter to continue or quit to exit")
                result = input()
                if result == "quit":
                    break

            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                break

        if isinstance(self.location_1, FtpLocation):
            self.location_1.disconnect_from_server()

        if isinstance(self.location_2, FtpLocation):
            self.location_2.disconnect_from_server()

    def mirror_path(self, current_relative_abs_path, location_number, location):
        if location_number == 1:
            root_ = self.location_2.get_temporary_abs_path()
        else:
            root_ = self.location_1.get_temporary_abs_path()
        # print(f"root {root_} current location relative path {current_relative_abs_path}", end=" ")

        if isinstance(location, FtpLocation):
            current_relative_abs_path_ = current_relative_abs_path.replace("\\", "/")
            mirror = root_ + current_relative_abs_path_
        else:
            current_relative_abs_path_ = current_relative_abs_path.replace("/", "\\")
            mirror = os.path.join(root_, current_relative_abs_path_)
        # print(f"mirror {mirror}")
        return mirror

    @classmethod
    def make_path(cls, location, relative_path):
        if isinstance(location, FtpLocation):
            relative_path_ = relative_path.replace("\\", "/")
            return location.get_abs_real_path() + relative_path_
        else:
            relative_path_ = relative_path.replace("/", "\\")
            return os.path.join(location.get_temporary_abs_path(), relative_path_)

    def recursive_balance_differences(self, location_current_files, location_1, location_2):
        files = location_current_files[3]
        for key in files.keys():
            file = files[key]
            relative_path = file[0].get_relative_path()
            file_path_1 = Sync.make_path(location_1, relative_path)
            # file_path_1 = os.path.join(location_1.get_temporary_abs_path(), relative_path)
            file_path_2 = Sync.make_path(location_2, relative_path)
            # file_path_2 = os.path.join(location_2.get_temporary_abs_path(), relative_path)
            # print(f"relative path {relative_path}")
            print(f"file path 1 {file_path_1}")
            print(f"file path 2 {file_path_2}")
            mirror_path_1 = self.mirror_path(relative_path, 1, location_2)
            mirror_path_2 = self.mirror_path(relative_path, 2, location_1)
            print(f"mirror path  1 {mirror_path_1}")
            print(f"mirror path  2 {mirror_path_2}")
            if file[1] == "added":
                if file[2] == 1:
                    self._add(file_path_1, mirror_path_1, location_1, location_2, file)
                else:
                    self._add(file_path_2, mirror_path_2, location_2, location_1, file)
            elif file[1] == "modified":
                # print(f"file {file[0].name}")
                if file[2] == 1:
                    if not isinstance(file[0], Folder):
                        self._modify(file_path_1, mirror_path_1, location_1, location_2)
                else:
                    if not isinstance(file[0], Folder):
                        self._modify(file_path_2, mirror_path_2, location_2, location_1)
            elif file[1] == "deleted":
                if file[2] == 1:
                    if isinstance(file[0], Folder):
                        Folder.delete_folder(file_path_2)
                    else:
                        Folder.delete_file(file_path_2)
                else:
                    if isinstance(file[0], Folder):
                        Folder.delete_folder(file_path_1)
                    else:
                        Folder.delete_file(file_path_1)

            if file[1] not in ["added"] and isinstance(file[0], Folder):
                self.recursive_balance_differences(file, location_1, location_2)

    def _add(self, source, destination, location_1, location_2, file):
        object_of_type = file[0]
        if isinstance(location_1, FtpLocation) and isinstance(location_2, FtpLocation):
            if isinstance(object_of_type, Folder):
                FtpLocation.copy_folder_from_ftp_to_ftp(location_1.connection, location_2.connection, source,
                                                        destination)
            else:
                FtpLocation.copy_file_from_ftp_to_ftp(location_1.connection, location_2.connection, source)
        # source
        elif isinstance(location_1, FtpLocation) and not isinstance(location_2, FtpLocation):
            if isinstance(object_of_type, Folder):
                FtpLocation.copy_ftp_folder_to_folder(location_1.connection, source, destination)
            else:
                FtpLocation.copy_ftp_file_to(location_1.connection, source, destination)
        elif not isinstance(location_1, FtpLocation) and isinstance(location_2, FtpLocation):
            if isinstance(object_of_type, Folder):
                FtpLocation.copy_folder_to_ftp(location_2.connection, source, destination)
            else:
                FtpLocation.copy_file_to_ftp(location_2.connection, source, destination)
        else:
            if isinstance(object_of_type, Folder):
                Folder.copy_folder(source, destination)
            else:
                Folder.copy_file(source, destination)

    def _modify(self, source, destination, location_1, location_2):
        if isinstance(location_1, FtpLocation) and isinstance(location_2, FtpLocation):
            FtpLocation.copy_file_from_ftp_to_ftp(location_1.connection, location_2.connection, source)
        elif isinstance(location_1, FtpLocation) and not isinstance(location_2, FtpLocation):
            FtpLocation.copy_ftp_file_to(location_1.connection, source, destination)
        elif not isinstance(location_1, FtpLocation) and isinstance(location_2, FtpLocation):
            FtpLocation.copy_file_to_ftp(location_2.connection, source, destination)
        else:
            Folder.copy_file(source, destination)

    def location_walk(self, current_path, location_number, location_current_files, location_1_2_files, real_path,
                      type_current_location=None, connection=None, relative_path=""):
        try:
            if type_current_location == "ftp":
                path_ftp_folder = current_path
                print(f"current path {current_path}")
                current_directory = connection.pwd()
                list_of_files = connection.nlst(path_ftp_folder)
                connection.cwd(current_directory)
            else:
                list_of_files = os.listdir(current_path)

            if len(location_1_2_files) == 4:
                for file in location_1_2_files[3].keys():
                    if type_current_location == "ftp":
                        key = file.split("/")[-1]
                    else:
                        key = file

                    if file not in list_of_files:
                        location_current_files[3][key] = [location_1_2_files[3][key][0], "deleted", location_number,
                                                          {}]

            for file in list_of_files:
                if type_current_location == "ftp":
                    key = file.split("/")[-1]
                else:
                    key = file

                if type_current_location == "ftp":
                    time_str = connection.voidcmd(f'MDTM {file}')[4:]
                    data_modified = datetime.strptime(time_str.strip()[:14], '%Y%m%d%H%M%S')
                    data_modified += timedelta(hours=2)
                else:
                    data_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(current_path, file)))

                relative_ = os.path.join(relative_path, key)
                object_of_type = object_specific_type(key, current_path, data_modified, real_path,
                                                      type_current_location, relative_, connection,
                                                      type_current_location)
                location_1_2_key_exists = False
                if len(location_1_2_files) < 4 or key not in location_1_2_files[3].keys():
                    location_current_files[3][key] = [object_of_type, "added", location_number, {}]
                elif location_1_2_files[3][key][0].data_modified != data_modified:
                    location_current_files[3][key] = [object_of_type, "modified", location_number, {}]
                    print(data_modified)
                    location_1_2_key_exists = True
                elif location_1_2_files[3][key][0].data_modified == data_modified:
                    location_current_files[3][key] = [location_1_2_files[3][key][0], "unchanged", 57, {}]
                    location_1_2_key_exists = True

                if location_1_2_key_exists:
                    location_1_2 = location_1_2_files[3][key]
                else:
                    location_1_2 = []

                if isinstance(object_of_type, Folder):
                    if type_current_location == "ftp":
                        current_path_next = current_path + key + "/"
                    else:
                        current_path_next = os.path.join(current_path, file)
                    self.location_walk(current_path_next, location_number,
                                       location_current_files[3][key],
                                       location_1_2, os.path.join(real_path, key), type_current_location, connection,
                                       relative_)

        except (OSError, zipfile.BadZipFile) as e:
            print(f"1 Error at checking the differences in {type(location_current_files[0])} {current_path}",
                  type(e), str(e))
            sys.exit(1)
        except ftplib.all_errors as e:
            print(f"2 Error at checking the differences in {type(location_current_files[0])} {current_path}",
                  type(e), str(e))
            connection.quit()
            sys.exit(1)

    def compare_location_current_files(self, location_1_2_files, location_1_files, location_2_files,
                                       new_location_1_2_files):
        if len(location_1_files) == 4:
            new_location_1_2_files[3] = location_1_files[3].copy()

        if len(location_2_files) == 4:
            for key in location_2_files[3].keys():
                if len(location_1_files) < 4 or key not in location_1_files[3].keys():
                    new_location_1_2_files[3][key] = location_2_files[3][key]
                else:
                    if location_1_files[3][key][1] == "deleted" or location_2_files[3][key][1] == "deleted":
                        new_location_1_2_files[3][key] = Sync.deleted_comparison(location_1_files[3][key],
                                                                                 location_2_files[3][key])
                    elif location_1_files[3][key][1] == "modified" or location_2_files[3][key][1] == "modified":
                        new_location_1_2_files[3][key] = Sync.modified_comparison(location_1_files[3][key],
                                                                                  location_2_files[3][key],
                                                                                  location_1_2_files[3][key])
                    elif location_1_files[3][key][1] == "added" and location_2_files[3][key][1] == "added":
                        new_location_1_2_files[3][key] = Sync.added_comparison(location_1_files[3][key],
                                                                               location_2_files[3][key])

        for key in new_location_1_2_files[3].keys():
            file = new_location_1_2_files[3][key]
            if len(location_1_2_files) < 4 or key not in location_1_2_files[3].keys():
                next_1_2 = []
            else:
                next_1_2 = location_1_2_files[3][key]  # IN MOD NORMAL NU INTRA AICI

            if len(location_1_files) < 4 or key not in location_1_files[3].keys():
                next_1 = []
            else:
                next_1 = location_1_files[3][key]

            if len(location_2_files) < 4 or key not in location_2_files[3].keys():
                next_2 = []
            else:
                next_2 = location_2_files[3][key]

            if isinstance(file[0], Folder) and file[1] != "deleted":
                self.compare_location_current_files(next_1_2, next_1, next_2,
                                                    new_location_1_2_files[3][key])

    def check_differences(self, location_current_files_1, location_current_files_2):
        if isinstance(self.location_1, Folder):
            self.location_walk(self.location_1.get_abs_real_path(), 1, location_current_files_1,
                               self.location_1_2_files,
                               self.location_1.get_abs_real_path(), "folder", self.connection_1, "")
        elif isinstance(self.location_1, Zip):
            temp_dir = Zip.extract_zip_to_temp(self.location_1.get_location())
            self.location_1.set_temporary_abs_path(temp_dir)
            # self.location_1.set_name(os.path.basename(temp_dir))
            self.location_walk(temp_dir, 1, location_current_files_1, self.location_1_2_files,
                               self.location_1.get_temporary_abs_path(), "zip", relative_path="")
        elif isinstance(self.location_1, FtpLocation):
            self.location_walk(self.location_1.get_abs_real_path(), 1, location_current_files_1,
                               self.location_1_2_files,
                               self.location_1.get_abs_real_path(), "ftp", self.connection_1, "")

        if isinstance(self.location_2, Folder):
            self.location_walk(self.location_2.get_abs_real_path(), 2, location_current_files_2,
                               self.location_1_2_files,
                               self.location_2.get_abs_real_path(), "folder", relative_path="")
        elif isinstance(self.location_2, Zip):
            temp_dir = Zip.extract_zip_to_temp(self.location_2.get_location())
            self.location_2.set_temporary_abs_path(temp_dir)
            self.location_walk(temp_dir, 2, location_current_files_2, self.location_1_2_files,
                               self.location_2.get_temporary_abs_path(), "zip", relative_path="")
        elif isinstance(self.location_2, FtpLocation):
            self.location_walk(self.location_2.get_abs_real_path(), 2, location_current_files_2,
                               self.location_1_2_files,
                               self.location_2.get_abs_real_path(), "ftp", self.connection_2, "")

    def set_new_state(self):
        pass

    @classmethod
    def deleted_comparison(cls, location_1, location_2):
        if location_1[1] == "deleted":
            return [location_1[0], "deleted", location_1[2], {}]
        elif location_2[1] == "deleted":
            return [location_2[0], "deleted", location_2[2], {}]

    @classmethod
    def modified_comparison(cls, location_1, location_2, location_1_2):
        old_data = location_1_2[0].data_modified
        location_1_data = location_1[0].data_modified
        location_2_data = location_2[0].data_modified

        if location_1_data == location_2_data:
            return [location_1[0], "unchanged", 88, location_1[3]]

        if location_1_data == old_data:
            return [location_2[0], "modified", location_2[2], location_2[3]]

        if location_2_data == old_data:
            return [location_1[0], "modified", location_1[2], location_1[3]]

        if location_1_data > location_2_data:
            return [location_1[0], "modified", location_1[2], location_1[3]]

        if location_1_data < location_2_data:
            return [location_2[0], "modified", location_2[2], location_2[3]]

    @classmethod
    def added_comparison(cls, location_1, location_2):
        location_1_data = location_1[0].data_modified
        location_2_data = location_2[0].data_modified

        if location_1_data == location_2_data:
            return [location_1[0], "unchanged", 0, {}]

        if location_1_data > location_2_data:
            return [location_1[0], "modified", location_1[2], {}]

        if location_1_data < location_2_data:
            return [location_2[0], "modified", location_2[2], {}]

        print("AICI NU TREBUIE SA AJUNGA")

    def remove_deleted_elements(self, location_1_2_files):
        keys_to_remove = []
        for key in location_1_2_files[3].keys():
            file = location_1_2_files[3][key]
            if file[1] == "deleted":
                keys_to_remove.append(key)

        for key in keys_to_remove:
            location_1_2_files[3].pop(key)

        for key, file in location_1_2_files[3].items():
            if isinstance(file[0], Folder):
                self.remove_deleted_elements(file)


def main():
    if len(sys.argv) != 3:
        print("Sunt necesare 3 argumente: advanced_rsync.py <location_1> <location_2>!")
        sys.exit(1)

    print(sys.argv[1], sys.argv[2])
    sync = Sync(sys.argv[1], sys.argv[2])
    sync.start()


main()