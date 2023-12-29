import os
import sys
import tempfile
import zipfile
import time
from File import File


def extract_zip_to_temp(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path) as z:
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
    return temp_dir


class Zip(File):
    def __init__(self, name, data_modified, real_parent=None, temporary_parent=None, type_parent=None):
        super().__init__(name, data_modified, real_parent, temporary_parent, type_parent)
        self.path = self.get_abs_real_path()

    def verify_path(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError("Path for zip does not exist")
            if not os.path.isfile(self.path) or not self.path.endswith(".zip"):
                raise ValueError("Invalid zip location")
            print("Zipfile exists")

            with zipfile.ZipFile(self.path, 'r') as z:
                if z.testzip() is not None:
                    raise zipfile.BadZipFile("Bad zip file")
            print("Zipfile is valid")

        except (FileNotFoundError, ValueError, zipfile.BadZipFile) as e:
            print(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        with zipfile.ZipFile(self.path) as z:
            for i in z.infolist():
                file_name = os.path.basename(i.filename)
                print(file_name, end="\n")

    def get_location(self):
        return self.path

    def __str__(self):
        return "Zip: " + self.path


