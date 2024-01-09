import errno
import logging
import os
import shutil
import sys
from File import File


class Folder(File):
    """Folder class that inherits from File class. It has the same attributes and methods of File class, but it has
    some more methods that are useful for operating with folders"""

    def __init__(self, name, data_modified, real_parent=None, temporary_parent=None, type_parent=None,
                 relative_path=None):
        super().__init__(name, data_modified, real_parent, temporary_parent, type_parent, relative_path)
        self.path = self.get_abs_real_path()

    @classmethod
    def verify_path(cls, path):
        """Method that verifies if a path is valid
        :param path: path to verify
        """
        try:
            if not os.path.isdir(path):
                raise OSError(f"The folder path {path} is not valid")
            logging.info(f"Folder {path} exists")
        except (OSError, FileNotFoundError) as e:
            logging.error(type(e), str(e))
            sys.exit(1)

    def print_files(self):
        """Prints all the files and folders that are inside folder"""
        list_of_files = os.listdir(self.path)
        for file in list_of_files:
            print(file)
        print()

    def __str__(self):
        """Returns a string with the path of the folder"""
        return "Folder: " + self.path

    @classmethod
    def copy_folder(cls, folder, destination):
        """Copies a folder from a path to another
        :param folder: folder to copy
        :param destination: destination of the folder"""
        try:
            shutil.copytree(folder, destination)
            logging.info(f"Folder {folder} copied from {destination}")
        except shutil.Error as e:
            logging.error(f"Folder copy error: {e}")
            sys.exit(1)

    @classmethod
    def copy_file(cls, file, destination, action):
        """Copies a file from a path to another
        :param file: file to copy
        :param destination: destination of the file to copy"""
        try:
            shutil.copy2(file, destination)
            if action == "modified":
                logging.info(f"File {destination} modified from {file}")
            else:
                logging.info(f"File {destination} copied from {file}")
        except shutil.Error as e:
            if isinstance(e, PermissionError) and e.errno == errno.EACCES:
                logging.warning(f"Permission error at copying: {e}. Maybe a file is opened...")
                sys.exit(1)
            else:
                logging.error(f"Folder copy error: {e}")
                sys.exit(1)

    @classmethod
    def modify_file(cls, file, destination):
        """Overwrites a file from a path to another
        :param file: file that overwrites
        :param destination: destination of the file to overwrite"""
        try:
            # print(f"file {file} modified from {destination}")
            shutil.copy2(file, destination)
        except shutil.Error as e:
            if isinstance(e, PermissionError) and e.errno == errno.EACCES:
                logging.warning(f"Permission error at overwritten: {e}. Maybe a file is opened...")
                sys.exit(1)
            else:
                logging.error(f"Folder overwritten error: {e}")
                sys.exit(1)

    @classmethod
    def delete_folder(cls, file_path_1):
        """Deletes a folder from a path
        :param file_path_1:  the folder to delete"""
        try:
            shutil.rmtree(file_path_1)
            logging.info(f"Folder {file_path_1} deleted")
        except (OSError, shutil.Error) as e:
            logging.error(f"Delete folder error: {e}")
            sys.exit(1)

    @classmethod
    def delete_file(cls, file_path_1):
        """Deletes a file from the given path
        :param file_path_1:  the file to delete"""
        try:
            os.remove(file_path_1)
            logging.info(f"File {file_path_1} deleted")
        except OSError as e:
            logging.error(f"Delete file error: {e}")
            sys.exit(1)
