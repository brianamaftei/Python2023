import sys
import os


def calculates(path):
    try:
        if not os.path.isdir(path) or not os.path.exists(path):
            raise OSError("path gresit")
        calc = 0
        for root_folder_name, dir_names, files_name in list(os.walk(path)):
            for file in files_name:
                # value = os.path.getsize(os.path.join(root_folder_name, file))
                # if value is None:
                #     calc += value
                # else:
                #     raise PermissionError("nu ai voie sa afli dimensiunea")
                calc += os.path.getsize(os.path.join(root_folder_name, file))

    except (PermissionError, OSError, Exception) as e:
        print(type(e), str(e))
        sys.exit(1)
    else:
        print(calc)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("nr incorect de arg")

    path = sys.argv[1]
    calculates(path)
