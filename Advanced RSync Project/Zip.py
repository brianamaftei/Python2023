import logging
import os
import shutil
import sys
import tempfile
import zipfile
import time
from File import File


class Zip(File):
    def __init__(self, name, data_modified, real_parent=None, temporary_parent=None, type_parent=None, relative_path=None):
        super().__init__(name, data_modified, real_parent, temporary_parent, type_parent, relative_path)
        self.path = self.get_abs_real_path()
        self.copy_name = self.name

    @classmethod
    def verify_path(cls, path):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("Path for zip does not exist")
            if not os.path.isfile(path) or not path.endswith(".zip"):
                raise ValueError("Invalid zip location")
            print("Zipfile exists")

            with zipfile.ZipFile(path, 'r') as z:
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

    @classmethod
    def extract_zip_to_temp(cls, zip_path):
        try:
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(zip_path) as zip_file:
                zip_file.extractall(temp_dir)
                for file_info in zip_file.infolist():
                    if os.path.isdir(os.path.join(temp_dir, file_info.filename)):
                        continue
                    extracted_path = os.path.join(temp_dir, file_info.filename)
                    date_modified = time.mktime(file_info.date_time + (0, 0, -1))
                    os.utime(extracted_path, (date_modified, date_modified))

                for file_info in zip_file.infolist():
                    if os.path.isdir(os.path.join(temp_dir, file_info.filename)):
                        extracted_path = os.path.join(temp_dir, file_info.filename)
                        date_modified = time.mktime(file_info.date_time + (0, 0, -1))
                        os.utime(extracted_path, (date_modified, date_modified))
            print(f"Zip {zip_path} extracted to temporary folder {temp_dir}")
            return temp_dir
        except zipfile.BadZipFile as e:
            print(type(e), str(e))
            sys.exit(1)

    @classmethod
    def delete_temp_dir(cls, temp_dir):
        try:
            shutil.rmtree(temp_dir)
            logging.info(f"Folder temp_dir {temp_dir} deleted")
        except shutil.Error as e:
            logging.error(f"Delete temp folder error: {e}")
            sys.exit(1)

    @classmethod
    def compress_folder_into_zip(cls, temp_dir, destination):

        try:
            with zipfile.ZipFile(destination, 'w') as zip_file:
                for root, dirs, files in os.walk(temp_dir):
                    for folder in dirs:
                        dir_path = os.path.join(root, folder)
                        file_mtime = time.localtime(os.path.getmtime(dir_path))
                        zip_info = zipfile.ZipInfo(os.path.relpath(dir_path, temp_dir))
                        zip_info.date_time = file_mtime[:6]
                        zip_file.write(dir_path, os.path.relpath(dir_path, temp_dir) + '/')
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_mtime = time.localtime(os.path.getmtime(file_path))
                        zip_info = zipfile.ZipInfo(os.path.relpath(file_path, temp_dir))
                        zip_info.date_time = file_mtime[:6]
                        zip_file.write(file_path, os.path.relpath(file_path, temp_dir))

            logging.info(f"Folder {temp_dir} compressed into {destination}")
            cls.delete_temp_dir(temp_dir)

        except zipfile.BadZipFile as e:
            print(type(e), str(e))
            sys.exit(1)
