import errno
import logging
import os
import shutil
import sys
from File import File


class Folder(File):
    def __init__(self, name, data_modified, real_parent=None, temporary_parent=None, type_parent=None, relative_path=None):
        super().__init__(name, data_modified, real_parent, temporary_parent, type_parent, relative_path)
        self.path = self.get_abs_real_path()

    @classmethod
    def verify_path(cls, path):
        try:
            if not os.path.isdir(path):
                raise OSError(f"The folder path {path} is not valid")
            print(f"Folder {path} exists")
        except (OSError, FileNotFoundError) as e:
            print(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        list_of_files = os.listdir(self.path)
        for file in list_of_files:
            print(file)
        print()

    def __str__(self):
        return "Folder: " + self.path

    @classmethod
    def copy_folder(cls, folder, destination):
        try:
            shutil.copytree(folder, destination)
            logging.info(f"Folder {folder} copied from {destination}")
        except shutil.Error as e:
            logging.error(f"Folder copy error: {e}")
            sys.exit(1)

    @classmethod
    def copy_file(cls, file, destination):
        try:
            shutil.copy2(file, destination)
            logging.info(f"File {file} copied from {destination}")
        except shutil.Error as e:
            if isinstance(e, PermissionError) and e.errno == errno.EACCES:
                logging.warning(f"Permission error at copying: {e}. Maybe a file is opened...")
                sys.exit(1)
            else:
                logging.error(f"Folder copy error: {e}")
                sys.exit(1)

    @classmethod
    def modify_file(cls, file, destination):
        try:
            print(f"file {file} modified from {destination}")
            shutil.copy2(file, destination)
            logging.info(f"File {file} overwritten from {destination}")
        except shutil.Error as e:
            if isinstance(e, PermissionError) and e.errno == errno.EACCES:
                logging.warning(f"Permission error at overwritten: {e}. Maybe a file is opened...")
                sys.exit(1)
            else:
                logging.error(f"Folder overwritten error: {e}")
                sys.exit(1)

    @classmethod
    def delete_folder(cls, file_path_1):
        try:
            shutil.rmtree(file_path_1)
            logging.info(f"Folder {file_path_1} deleted")
        except shutil.Error as e:
            logging.error(f"Delete folder error: {e}")
            sys.exit(1)

    @classmethod
    def delete_file(cls, file_path_1):
        try:
            os.remove(file_path_1)
            logging.info(f"File {file_path_1} deleted")
        except OSError as e:
            logging.error(f"Delete file error: {e}")
            sys.exit(1)
