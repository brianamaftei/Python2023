import re
import sys


class Vocabulary:
    def __init__(self, string=None):
        if string is None:
            string = ""
        self.string = string
        self.vocabulary = self.make_vocabulary()

    def make_vocabulary(self):
        words = set(re.split("\s+", self.string))
        characters = set(char for char in self.string)
        return {"words": words, "characters": characters}

    def statistics(self):
        return f"The number of words: {len(self.vocabulary['words'])}\nThe number of characters: {len(self.vocabulary['characters'])}"

    def update(self, new_string):
        self.string += new_string
        self.vocabulary["words"].union(set(re.split("\s+", self.string)))
        self.vocabulary["characters"].union(set(char for char in self.string))

    def to_string(self):
        result = " ".join(word for word in self.vocabulary["words"])
        return result

    def compare(self, obj):
        try:
            if type(obj) is not Vocabulary:
                raise TypeError("The object must be a Vocabulary object")
            result = " "
            for word in self.vocabulary["words"]:
                if word in obj.vocabulary["words"]:
                    print(word)

            for char in self.vocabulary["characters"]:
                if char in obj.vocabulary["characters"]:
                    print(char)

        except TypeError as e:
            print(e)
            sys.exit()


a = Vocabulary("ana are mere")
print(a.statistics())
b = Vocabulary("Ana nu mai are mere")
print(b.statistics())
print(a.compare(b))
a.update("bla bla")
print(a.statistics())
a.to_string()
