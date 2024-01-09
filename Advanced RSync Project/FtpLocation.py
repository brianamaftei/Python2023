import datetime
import ftplib
import io
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from ftplib import FTP

logging.basicConfig(level=logging.INFO)


class FtpLocation:
    """Class that represents a ftp location. It contains methods to connect to a ftp server, to copy files and folders,
    to delete files and folders"""

    def __init__(self, location):
        self.location = location
        parts = self.split_location()
        self.host = parts[2]
        self.username = parts[0]
        self.password = parts[1]
        self.virtual_path = parts[3]
        self.connection = self.connect_to_server()
        self.temporary_abs_path = self.get_abs_real_path()

    def split_location(self):
        """Splits the ftp location in host, username, password and virtual path
        :return: list with host, username, password and virtual path"""
        try:
            if self.location.count(":") != 1 or self.location.count("@") != 1 or self.location.count("/") != 1:
                raise ValueError("Invalid ftp location format")
            parts = []
            path = self.location.split(":", 1)
            parts.append(path[0])
            path = path[1].split("@", 1)
            parts.append(path[0])
            path = path[1].split("/", 1)
            parts.append(path[0])
            parts.append("/" + path[1])
            print(parts)
            return parts
        except ValueError as e:
            logging.error(type(e), str(e))
            sys.exit(1)

    def connect_to_server(self):
        """Connects to the ftp server
        :return: ftp connection"""
        logging.info("Trying to connect to server")
        try:
            ftp = FTP(host=self.host, user=self.username, passwd=self.password, timeout=10)
            logging.info("Connected to server")
            ftp.cwd(self.virtual_path)
            return ftp
        except ftplib.all_errors as e:
            logging.error(f"FTP connection error: {e}")
            sys.exit(1)

    def disconnect_from_server(self):
        """Disconnects from the ftp server"""
        try:
            self.connection.quit()
            logging.info("Disconnected from server")
        except ftplib.all_errors as e:
            logging.error(f"FTP disconnection error: {e}")
            sys.exit(1)

    def print_files(self):
        """Prints all the files and folders that are inside a folder"""
        try:
            list_of_files = self.connection.nlst()
            for file in list_of_files:
                print(file)
        except ftplib.all_errors as e:
            logging.error(f"FTP files error: {e}")
            self.connection.quit()
            sys.exit(1)

    def __str__(self):
        """Returns a string with the ftp location"""
        result = ("Ftp: \n" + "Host: " + self.host + " " + "Username: " + self.username +
                  " " + "Password: " + self.password + " " + "Virtual Path: " + self.virtual_path)
        return result

    def get_abs_real_path(self):
        """Returns the absolute path of the ftp location"""
        return "." + self.virtual_path

    def get_temporary_abs_path(self):
        """Returns the temporary absolute path of the ftp location"""
        return self.temporary_abs_path

    @classmethod
    def copy_file_to_ftp(cls, connection, source, destination, action):
        """Copies a file from a local path to a ftp path
        :param connection: ftp connection
        :param source: source of the file to copy
        :param destination: destination of the file to copy"""

        try:
            logging.info(f"We want File {source} to {destination}")
            with open(source, 'rb') as file:
                connection.storbinary("STOR " + destination, file)

            mod_time = os.path.getmtime(source)
            cls.set_mod_time_on_ftp(connection, destination, mod_time)
            if action == "modified":
                logging.info(f"File modified in ftp at {destination}")
            else:
                logging.info(f"File {source} copied to {destination}")
        except ftplib.all_errors as e:
            logging.error(f"Copy file to FTP error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def set_mod_time_on_ftp_from_ftp(cls, connection, path, mod_time):
        """Sets the modification time of a file in a ftp server
        :param connection: ftp connection
        :param path: path of the file
        :param mod_time: modification time of the file"""
        try:
            gmt_time = mod_time.strftime("%Y%m%d%H%M%S")
            connection.sendcmd(f"MFMT {gmt_time} {path}")
            logging.info(f"Set modification time for {path} to {gmt_time}")
        except ftplib.all_errors as e:
            logging.warning(f"Unable to set modification time on FTP for {path}: {e}")

    @classmethod
    def copy_folder_to_ftp(cls, connection, source, destination):
        """Copies a folder from a local path to a ftp path
        :param connection: ftp connection
        :param source: source of the folder to copy
        :param destination: destination of the folder to copy
        """
        try:
            try:
                connection.mkd(destination)
            except ftplib.error_perm:
                pass
            list_of_items = os.listdir(source)
            for item in list_of_items:
                name = os.path.basename(item)
                source_path = os.path.join(source, name)
                dest_path = os.path.join(destination, name)
                dest_path = dest_path.replace("\\", "/")
                logging.info(f"Source path: {source_path} Dest path: {dest_path}")
                if os.path.isdir(source_path):
                    cls.copy_folder_to_ftp(connection, source_path, dest_path)
                else:
                    with open(source_path, 'rb') as file:
                        connection.storbinary(f"STOR {dest_path}", file)
                        mod_time = os.path.getmtime(source_path)
                        cls.set_mod_time_on_ftp(connection, dest_path, mod_time)
        except ftplib.all_errors as e:
            logging.error(f"FTP copy folder to ftp error: {e} {source} {destination}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def set_mod_time_on_ftp(cls, connection, path, mod_time):
        """Sets the modification time of a file in a ftp server
        :param connection: ftp connection
        :param path: path of the file
        :param mod_time: modification time of the file"""
        gmt_time = datetime.fromtimestamp(mod_time, timezone.utc).strftime("%Y%m%d%H%M%S")
        try:
            connection.sendcmd(f'MFMT {gmt_time} {path}')
            logging.info(f"Set modification time for {path} to {gmt_time}")
        except ftplib.all_errors as e:
            logging.warning(f"Unable to set modification time on FTP for {path}: {e}")

    @classmethod
    def copy_ftp_file_to(cls, connection, source, destination, action):
        """Copies a file from a ftp path to a local path
        :param connection: ftp connection
        :param source: source of the file to copy
        :param destination: destination of the file to copy
        :param action: the name of the action in order to name the log message"""
        try:
            connection.retrbinary("RETR " + source, open(destination, 'wb').write)

            time_str = connection.voidcmd(f'MDTM {source}')[3:]
            data_modified = datetime.strptime(time_str.strip()[:14], '%Y%m%d%H%M%S')
            data_modified += timedelta(hours=2)

            timestamp = int(time.mktime(data_modified.timetuple()))
            os.utime(destination, (timestamp, timestamp))
            if action == "modified":
                logging.info(f"File {destination} overwritten in ftp from {source}")
            else:
                logging.info(f"File {source} copied to {destination}")
        except ftplib.all_errors as e:
            logging.error(f"FTP copy ftp file to error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def copy_ftp_folder_to_folder(cls, connection, source, destination):
        """Copies a folder from a ftp path to a local path
        :param connection: ftp connection
        :param source: source of the folder to copy
        :param destination: destination of the folder to copy
        """
        try:
            try:
                os.mkdir(destination)
            except FileExistsError:
                pass

            list_of_items = connection.nlst(source)
            for item in list_of_items:
                name = os.path.basename(item)
                source_path = os.path.join(source, name)
                dest_path = os.path.join(destination, name)
                dest_path = dest_path.replace("\\", "/")
                if cls.is_directory(connection, source_path):
                    cls.copy_ftp_folder_to_folder(connection, source_path, dest_path)
                else:
                    with open(dest_path, 'wb') as file:
                        connection.retrbinary(f"RETR {source_path}", file.write)

                    time_str = connection.voidcmd(f'MDTM {source_path}')[4:]
                    data_modified = datetime.strptime(time_str.strip()[:14], '%Y%m%d%H%M%S')
                    data_modified += timedelta(hours=2)

                    timestamp = int(time.mktime(data_modified.timetuple()))
                    os.utime(dest_path, (timestamp, timestamp))

        except ftplib.all_errors as e:
            logging.error(f"FTP copy ftp folder to error: {e} {source} {destination}")
            sys.exit(1)

    @classmethod
    def get_mod_time_from_ftp(cls, connection, file_path):
        """Gets the modification time of a file in a ftp server
        :param connection: ftp connection
        :param file_path: path of the file
        :return: modification time of the file
        """
        try:
            time_str = connection.voidcmd(f'MDTM {file_path}')[4:]
            data_modified = datetime.strptime(time_str.strip()[:14], '%Y%m%d%H%M%S')

            return data_modified
        except ftplib.all_errors as e:
            logging.warning(f"Unable to get modification time for {file_path}: {e}")
            return None

    @classmethod
    def copy_file_from_ftp_to_ftp(cls, connection_from, connection_to, file, action):
        """Copies a file from a ftp path to another ftp path
        :param connection_from: ftp connection from where to copy
        :param connection_to: ftp connection to where to copy
        :param file: file to copy
        :param action: the name of the action in order to name the log message"""
        try:
            mod_time = cls.get_mod_time_from_ftp(connection_from, file)

            with io.BytesIO() as buffer:
                connection_from.retrbinary("RETR " + file, buffer.write)
                buffer.seek(0)
                connection_to.storbinary("STOR " + file, buffer)
            if action == "modified":
                logging.info(f"File {file} overwritten in ftp from {file}")
            else:
                logging.info(f"File {file} {action} from ftp to ftp")

            if mod_time:
                cls.set_mod_time_on_ftp_from_ftp(connection_to, file, mod_time)

        except ftplib.all_errors as e:
            logging.error(f"FTP copy file from ftp to ftp error: {e}")
            connection_from.quit()
            connection_to.quit()
            sys.exit(1)

    @staticmethod
    def is_directory(connection, name):
        """Checks if a path from a ftp location is a directory
        :param connection: ftp connection
        :param name: path to check"""
        current_directory = connection.pwd()
        try:
            connection.cwd(name)
            is_dir = True
        except ftplib.error_perm:
            is_dir = False
        finally:
            connection.cwd(current_directory)
        return is_dir

    @classmethod
    def is_file(cls, connection, name):
        """Checks if a path from a ftp location is a file
        :param connection: ftp connection
        :param name: path to check
        """
        return not cls.is_directory(connection, name)

    @classmethod
    def copy_folder_from_ftp_to_ftp(cls, connection_from, connection_to, source, dest):
        """Copies a folder from a ftp path to another ftp path
        :param connection_from: ftp connection from where to copy
        :param connection_to: ftp connection to where to copy
        :param source: source of the folder to copy
        :param dest: destination of the folder to copy
        """
        try:
            try:
                connection_to.mkd(dest)
            except ftplib.error_perm as e:
                logging.info(f"Directory {dest} already exists or cannot be created: {e}")

            list_of_items = connection_from.nlst(source)
            for item in list_of_items:
                name = os.path.basename(item)
                source_path = os.path.join(source, name).replace("\\", "/")
                dest_path = os.path.join(dest, name).replace("\\", "/")
                if cls.is_directory(connection_from, source_path):
                    cls.copy_folder_from_ftp_to_ftp(connection_from, connection_to, source_path, dest_path)
                else:
                    mod_time = cls.get_mod_time_from_ftp(connection_from, source_path)
                    with io.BytesIO() as buffer:
                        connection_from.retrbinary(f"RETR {source_path}", buffer.write)
                        buffer.seek(0)
                        connection_to.storbinary(f"STOR {dest_path}", buffer)
                        if mod_time:
                            cls.set_mod_time_on_ftp_from_ftp(connection_to, dest_path, mod_time)
        except ftplib.all_errors as e:
            logging.error(f"FTP copy folder from ftp to ftp error: {e}")
            sys.exit(1)

    @classmethod
    def delete_ftp_content_folder(cls, connection, source):
        """Deletes the content of a folder from a ftp path
        :param connection: ftp connection
        :param source: path of the folder to delete
        """
        try:
            list_of_items = connection.nlst(source)
            for item in list_of_items:
                name = os.path.basename(item)
                source_path = os.path.join(source, name)
                source_path = source_path.replace("\\", "/")
                if cls.is_directory(connection, source_path):
                    cls.delete_ftp_folder(connection, source_path)
                else:
                    connection.delete(source_path)

            connection.rmd(source)
        except ftplib.all_errors as e:
            logging.error(f"FTP delete ftp folder error 1: {e} {source}")
            sys.exit(1)

    @classmethod
    def delete_ftp_folder(cls, connection, source):
        """This calls the delete_ftp_content_folder method to delete the content of a folder from a ftp location
        :param connection: ftp connection
        :param source: path of the folder to delete"""
        try:
            FtpLocation.delete_ftp_content_folder(connection, source)
            logging.info(f"Folder ftp {source} deleted")
        except ftplib.all_errors as e:
            logging.error(f"FTP delete ftp folder error 2: {e} {source}")
            sys.exit(1)

    @classmethod
    def delete_ftp_file(cls, connection, source):
        """Deletes a file from a ftp path
        :param connection: ftp connection
        :param source: path of the file to delete"""
        try:
            connection.delete(source)
            logging.info(f"File {source} deleted")
        except ftplib.all_errors as e:
            logging.error(f"FTP delete ftp file error: {e}")
            connection.quit()
            sys.exit(1)
