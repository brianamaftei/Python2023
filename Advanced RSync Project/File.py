import os
import hashlib


class File:
    def __init__(self, name, data_modified, real_parent, temporary_parent=None):
        self.name = name
        if "." not in self.name:
            self.extension = "folder"
        else:
            self.extension = self.name.split(".")[-1]
        self.data_modified = data_modified
        self.real_parent = real_parent
        self.abs_path = os.path.join(self.real_parent, self.name)
        self.temporary_parent = temporary_parent

    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    def get_data_modified(self):
        return self.data_modified

    def set_data_modified(self, data_modified):
        self.data_modified = data_modified

    def set_temporary_path(self, temporary_parent):
        self.temporary_parent = temporary_parent

    def get_abs_real_path(self):
        return self.abs_path
