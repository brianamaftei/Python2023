import ftplib
from datetime import datetime
from ftplib import FTP
import logging
import sys
from File import File

logging.basicConfig(level=logging.INFO)


class Ftp:
    def __init__(self, location):
        self.location = location
        parts = self.split_location()
        self.host = parts[2]
        self.username = parts[0]
        self.password = parts[1]
        self.virtual_path = parts[3]
        self.connection = self.connect_to_server()

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

    def status_files(self, location_number, location_current_files, location_1_2_files):
        try:
            list_of_files = self.connection.nlst()
            for file in location_1_2_files:
                name = file.split("/")[-1]
                if file not in list_of_files:
                    location_current_files[name] = (location_1_2_files[file][0], "deleted", location_number)
                else:
                    location_current_files[name][1] = (
                        location_1_2_files[file][0], "unchanged", location_1_2_files[file][2])

            for file in list_of_files:
                name = file.split("/")[-1]
                time_str = self.connection.voidcmd(f'MDTM {file}')[4:]  # returns 3 numbers and a space then the date
                conversion_time = datetime.strptime(time_str[:14], '%Y%m%d%H%M%S')
                if name not in location_1_2_files:
                    if name not in location_current_files:
                        location_current_files[name] = (
                            File(path=file, name=name, data_modified=conversion_time, parent=self.location),
                            "added", location_number)
                    elif location_current_files[name][0].data_modified < conversion_time:
                        location_current_files[name] = (
                            File(path=file, name=name, data_modified=conversion_time, parent=self.location),
                            "modified", location_number)
                    elif location_current_files[name][0].data_modified == conversion_time:
                        location_current_files[name] = (
                            File(path=file, name=name, data_modified=conversion_time, parent=self.location),
                            "unchanged", location_number)
                elif location_1_2_files[name][0].data_modified < conversion_time:
                    location_current_files[name] = (
                        File(path=file, name=name, data_modified=conversion_time, parent=self.location),
                        "modified", location_number)

        except ftplib.all_errors as e:
            logging.error(f"FTP files error: {e}")
            self.connection.quit()
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
