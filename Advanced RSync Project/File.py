import os
import hashlib


class File:
    def __init__(self, path, name, data_modified, parent):
        self.path = path
        self.name = name
        if "." not in self.name:
            self.extension = "folder"
        else:
            self.extension = self.name.split(".")[-1]
        self.data_modified = data_modified
        self.parent = parent
        self.abs_path = os.path.join(self.parent, self.name)

    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    def get_data_modified(self):
        return self.data_modified

    def set_data_modified(self, data_modified):
        self.data_modified = data_modified

