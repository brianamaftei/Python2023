import sys
from Folder import Folder
from Ftp import Ftp
from Zip import Zip


def parse_location(location):
    try:
        if location.count(":") < 1:
            raise ValueError("Invalid location format")
        type_location = location.split(":", 1)[0]
        location_path = location.split(":", 1)[1]
        if type_location == "ftp":
            return Ftp(location_path)
        elif type_location == "zip":
            return Zip(location_path)
        elif type_location == "folder":
            return Folder(location_path)
        else:
            raise ValueError("Invalid location format")
    except ValueError as e:
        print(type(e), str(e))
        sys.exit(1)


class Sync:
    def __init__(self, arg1, arg2):
        self.location_1 = parse_location(arg1)
        self.location_2 = parse_location(arg2)

    def start(self):
        print(self.location_1)
        print(self.location_2)


def main():
    if len(sys.argv) != 3:
        print("Sunt necesare 3 argumente: advanced_rsync.py <location_1> <location_2>!")
        sys.exit(1)

    sync = Sync(sys.argv[1], sys.argv[2])
    sync.start()


main()
