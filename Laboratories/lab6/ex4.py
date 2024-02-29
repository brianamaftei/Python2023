import sys
import os


def calculates(path):
    try:
        dict_ = dict()
        if not os.path.isdir(path) or not os.path.exists(path):
            raise OSError("path gresit")
        for root_folder_name, dir_names, files_name in list(os.walk(path)):
            for file in files_name:
                ext = file.split('.')[-1]
                if ext not in dict_.keys():
                    dict_[ext] = 1
                else:
                    dict_[ext] += 1

    except (PermissionError, OSError, Exception) as e:
        print(type(e), str(e))
        sys.exit(1)
    else:
        print(dict_)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("nr incorect de arg")

    path = sys.argv[1]
    calculates(path)
