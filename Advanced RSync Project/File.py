import os


class File:
    def __init__(self, name, data_modified, real_parent, temporary_parent=None, type_parent=None, relative_path=None):
        self.name = name
        if "." not in self.name:
            self.extension = "folder"
        else:
            self.extension = self.name.split(".")[-1]
        self.data_modified = data_modified
        self.real_parent = real_parent
        self.abs_path = os.path.join(self.real_parent, self.name)
        self.temporary_parent = temporary_parent
        self.type_parent = type_parent
        if self.temporary_parent is None:
            self.temporary_abs_path = None
        else:
            self.temporary_abs_path = os.path.join(self.temporary_parent, self.name)
        self.relative_path = relative_path

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    def get_data_modified(self):
        return self.data_modified

    def set_data_modified(self, data_modified):
        self.data_modified = data_modified

    def set_temporary_path_of_parent(self, temporary_parent):
        self.temporary_parent = temporary_parent

    def get_temporary_parent_path(self):
        return self.temporary_parent

    def get_abs_real_path(self):
        return self.abs_path

    def get_type_parent(self):
        return self.type_parent

    def get_temporary_abs_path(self):
        return self.temporary_abs_path

    def set_temporary_abs_path(self, temporary_location):
        self.temporary_abs_path = temporary_location

    def get_relative_path(self):
        return self.relative_path
