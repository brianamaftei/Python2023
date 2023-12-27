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
        self.hash = self.set_hash()

    def set_hash(self):
        m = hashlib.md5()
        with open(os.path.join(self.parent, self.name), "rb") as f:
            while 1:
                data = f.read(4096)
                if len(data) == 0:
                    break
                m.update(data)
        return m.digest()

    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    def get_data_modified(self):
        return self.data_modified

    def set_data_modified(self, data_modified):
        self.data_modified = data_modified

    def get_hash(self):
        return self.hash
