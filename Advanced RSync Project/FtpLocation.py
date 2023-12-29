import ftplib
import io
import os
from ftplib import FTP
import logging
import sys

logging.basicConfig(level=logging.INFO)


class FtpLocation:
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
            print(type(e), str(e))
            sys.exit(1)

    def connect_to_server(self):
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
        try:
            self.connection.quit()
            logging.info("Disconnected from server")
        except ftplib.all_errors as e:
            logging.error(f"FTP disconnection error: {e}")
            sys.exit(1)

    def print_files(self):
        try:
            list_of_files = self.connection.nlst()
            for file in list_of_files:
                print(file)
        except ftplib.all_errors as e:
            logging.error(f"FTP files error: {e}")
            self.connection.quit()
            sys.exit(1)

    def __str__(self):
        result = ("Ftp: \n" + "Host: " + self.host + " " + "Username: " + self.username +
                  " " + "Password: " + self.password + " " + "Virtual Path: " + self.virtual_path)
        return result

    def get_abs_real_path(self):
        return self.virtual_path

    @classmethod
    def copy_file_to_ftp(cls, connection, file, destination):
        try:
            connection.storbinary("STOR " + file, open(destination, 'rb'))
            logging.info(f"File {file} copied from {destination}")
        except ftplib.all_errors as e:
            logging.error(f"FTP copy file to ftp error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def copy_folder_to_ftp(cls, connection, source, destination):
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
                if os.path.isdir(source_path):
                    cls.copy_folder_to_ftp(connection, source_path, dest_path)
                else:
                    with open(source_path, 'rb') as file:
                        connection.storbinary(f"STOR {dest_path}", file)
        except ftplib.all_errors as e:
            logging.error(f"FTP copy folder to ftp error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def copy_ftp_file_to(cls, connection, file, destination):
        try:
            connection.retrbinary("RETR " + file, open(destination, 'wb').write)
            logging.info(f"File {file} copied to {destination}")
        except ftplib.all_errors as e:
            logging.error(f"FTP copy ftp file to error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def copy_ftp_folder_to(cls, connection, source, destination):
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
                if cls.is_directory(connection, source_path):
                    cls.copy_ftp_folder_to(connection, source_path, dest_path)
                else:
                    with open(dest_path, 'wb') as file:
                        connection.retrbinary(f"RETR {source_path}", file.write)
        except ftplib.all_errors as e:
            logging.error(f"FTP copy ftp folder to error: {e}")
            connection.quit()
            sys.exit(1)

    @classmethod
    def copy_file_from_ftp_to_ftp(cls, connection_from, connection_to, file):
        try:
            with io.BytesIO() as buffer:
                connection_from.retrbinary("RETR " + file, buffer.write)
                buffer.seek(0)
                connection_to.storbinary("STOR " + file, buffer)
            logging.info(f"File {file} copied from {connection_from} to {connection_to}")
        except ftplib.all_errors as e:
            logging.error(f"FTP copy file from ftp to ftp error: {e}")
            connection_from.quit()
            connection_to.quit()
            sys.exit(1)

    @classmethod
    def is_directory(cls, connection, name):
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
    def copy_folder_from_ftp_to_ftp(cls, connection_from, connection_to, source_folder, dest_folder):
        try:
            try:
                connection_to.mkd(dest_folder)
            except ftplib.error_perm:
                pass
            list_of_items = connection_from.nlst(source_folder)
            for item in list_of_items:
                name = os.path.basename(item)
                source_path = os.path.join(source_folder, name)
                dest_path = os.path.join(dest_folder, name)
                if cls.is_directory(connection_from, source_path):
                    cls.copy_folder_from_ftp_to_ftp(connection_from, connection_to, source_path, dest_path)
                else:
                    with io.BytesIO() as buffer:
                        connection_from.retrbinary(f"RETR {source_path}", buffer.write)
                        buffer.seek(0)
                        connection_to.storbinary(f"STOR {dest_path}", buffer)
        except ftplib.all_errors as e:
            logging.error(f"FTP copy folder from ftp to ftp error: {e}")
            connection_from.quit()
            connection_to.quit()
            sys.exit(1)
