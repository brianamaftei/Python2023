import os
import sys


def print_file(dir_path, ext):
    try:
        if not os.path.isdir(dir_path):
            raise IsADirectoryError("wrong path")
        list_files = os.listdir(dir_path)
        for file_name in list_files:
            path = os.path.join(dir_path, file_name)
            if file_name.endswith(ext) and os.path.isfile(path):
                with open(path, 'r') as file:
                    content = file.read()
                    print(content)
    except (IsADirectoryError, Exception, OSError) as e:
        print(str(e), type(e))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("nr of arguments incorrect")
        sys.exit(1)

    dir_path = sys.argv[1]
    ext = sys.argv[2]
    print_file(dir_path, ext)
