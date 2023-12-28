import os
import sys
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
            return Ftp(location_path)
        elif type_location == "zip":
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))
            return Zip(name=name, data_modified=data_modified, real_parent=real_parent)
        elif type_location == "folder":
            name = os.path.basename(location_path)
            real_parent = location_path.split(name)[0]
            data_modified = datetime.fromtimestamp(os.path.getmtime(location_path))
            return Folder(name=name, data_modified=data_modified, real_parent=real_parent)
        else:
            raise ValueError("Invalid location type")

    except ValueError as e:
        print(type(e), str(e))
        sys.exit(1)


def print_dictionary(dictionary):
    for key in dictionary:
        print("Key: " + key + " Value: " + dictionary[key].__str__())


def object_specific_type(name, current_path, data_modified, real_path):
    if "." not in name:
        return Folder(name=name, data_modified=data_modified, real_parent=real_path,
                      temporary_parent=current_path)
    elif name.split(".")[-1] == "zip":
        return Zip(name=name, data_modified=data_modified, real_parent=real_path,
                   temporary_parent=current_path)
    else:
        return File(name=name, data_modified=data_modified, real_parent=real_path,
                    temporary_parent=current_path)


def folder_walk(current_path, location_number, location_current_files, location_1_2_files, real_path):
    try:
        list_of_files = os.listdir(current_path)
        if len(location_1_2_files) == 3:
            for file in location_1_2_files[3].keys():
                key = file
                data_modified = datetime.fromtimestamp(os.path.getmtime(os.path.join(current_path, file)))
                object_of_type = object_specific_type(file, current_path, data_modified, real_path)
                if file not in list_of_files:
                    location_current_files[3][key] = [object_of_type, "deleted", location_number, {}]
                else:
                    location_current_files[3][key] = [object_of_type, "unchanged", 0, {}]

        for file in list_of_files:
            key = file
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
                location_1_2_key_exists = True
            elif location_1_2_files[3][key][0].data_modified == data_modified:
                location_current_files[3][key] = [object_of_type, "unchanged", 0, {}]
                location_1_2_key_exists = True

            if isinstance(object_of_type, Folder):
                if location_1_2_key_exists:
                    location_1_2 = location_1_2_files[3][key]
                else:
                    location_1_2 = []
                folder_walk(os.path.join(current_path, file), location_number, location_current_files[3][key],
                            location_1_2, os.path.join(real_path, file))

    except OSError as e:
        print(f"Error at checking the differences in folder {current_path}", type(e), str(e))
        sys.exit(1)


class Sync:
    def __init__(self, arg1, arg2):
        self.location_1 = setup_location(arg1)
        self.location_2 = setup_location(arg2)
        self.location_1_2_files = {}
        self.location_current_files = [File(name="Original", data_modified=datetime.now(), real_parent=""), "unique", 0, {}]

    def start(self):
        print("First Location: " + self.location_1.__str__())
        print("Second Location: " + self.location_2.__str__())
        self.location_1.print_files()
        self.location_2.print_files()
        self.check_differences()
        print(self.location_current_files)
        self.set_new_state()

    def check_differences(self):
        if isinstance(self.location_1, Folder):
            folder_walk(self.location_1.get_abs_real_path(), 1, self.location_current_files,
                        self.location_1_2_files,
                        self.location_1.get_abs_real_path())

        if isinstance(self.location_2, Folder):
            folder_walk(self.location_2.get_abs_real_path(), 2, self.location_current_files,
                        self.location_1_2_files,
                        self.location_2.get_abs_real_path())

    def set_new_state(self):
        pass

    # def zip_status_files(self, first_location, main_path, location_number, location_current_files, location_1_2_files,
    #                      key=None):
    #     try:
    #         if key is None:
    #             key = main_path.split(first_location, 1)[1]
    #         with zipfile.ZipFile(main_path) as z:
    #             temp_dir = tempfile.mkdtemp()
    #             extracted_zip_path = os.path.join(temp_dir, main_path)
    #             z.extract(main_path, temp_dir)
    #             main_path = extracted_zip_path
    #             first_location = extracted_zip_path
    #
    #         location_current_files[key][0].set_temporary_path(extracted_zip_path)
    #         self.keys_directories[key] = location_current_files[key]
    #         self.folder_status_files(first_location, extracted_zip_path, location_number,
    #                                  location_current_files[key],
    #                                  location_1_2_files)
    #
    #     except zipfile.BadZipFile as e:
    #         print(f"Error at checking the differences in zip {main_path}", type(e), str(e))
    #         sys.exit(1)


#                            shutil.rmtree(temp_dir)
#                            location_current_files[key][0].set_temporary_path(None)
def main():
    if len(sys.argv) != 3:
        print("Sunt necesare 3 argumente: advanced_rsync.py <location_1> <location_2>!")
        sys.exit(1)

    print(sys.argv[1], sys.argv[2])
    sync = Sync(sys.argv[1], sys.argv[2])
    sync.start()


main()
