import sys
from Folder import Folder
from Ftp import Ftp
from Zip import Zip


def parse_location(location):
    try:
        if location.count(":") < 1:
            raise ValueError("Invalid location type")
        type_location = location.split(":", 1)[0]
        location_path = location.split(":", 1)[1]
        if type_location == "ftp":
            return Ftp(location_path)
        elif type_location == "zip":
            return Zip(location_path)
        elif type_location == "folder":
            return Folder(location_path)
        else:
            raise ValueError("Invalid location type")
    except ValueError as e:
        print(type(e), str(e))
        sys.exit(1)


def print_dictionary(dictionary):
    for key in dictionary:
        print("Key: " + key + " Value: " + dictionary[key].__str__())


class Sync:
    def __init__(self, arg1, arg2):
        self.location_1 = parse_location(arg1)
        self.location_2 = parse_location(arg2)
        self.location_1_2_files = {}
        self.location_1_modification = {}
        self.location_2_modification = {}

    def start(self):
        print("First Location: " + self.location_1.__str__())
        print("Second Location: " + self.location_2.__str__())
        self.location_1.print_files()
        self.location_2.print_files()
        self.search_differences()

    def search_differences(self):
        self.location_1.status_files(1, self.location_1_modification, self.location_1_2_files)
        self.location_2.status_files(2, self.location_2_modification, self.location_1_2_files)


def main():
    if len(sys.argv) != 3:
        print("Sunt necesare 3 argumente: advanced_rsync.py <location_1> <location_2>!")
        sys.exit(1)

    print(sys.argv[1], sys.argv[2])
    sync = Sync(sys.argv[1], sys.argv[2])
    sync.start()


main()
