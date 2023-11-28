import os.path
import sys


def handle(path):
    try:
        if not os.path.isdir(path):
            raise OSError("path don t lead to a directory")

        files = os.listdir(path)
        for index, file in enumerate(files, start=1):
            if os.rename(os.path.join(path, file),
                         os.path.join(path, f"{file.split('.')[-2]}{index}.{file.split('.')[-1]}")) is not None:
                raise Exception("nu se poate redenumi")

    except (OSError, NameError, Exception) as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("nr gresit de arg")

    dir_path = sys.argv[1]

    handle(dir_path)
