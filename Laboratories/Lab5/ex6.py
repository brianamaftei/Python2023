class LibraryItem:
    def __init__(self, id, title, year):
        self.id = id
        self.title = title
        self.year = year
        self.genre = ""
        self.language = ""

    def set_parameter(self, parameter, value):
        old_value = getattr(self, parameter)
        if type(old_value) == type(value):
            setattr(self, parameter, value)
        else:
            print("Invalid value type.")

    def get_parameter(self, parameter):
        return getattr(self, parameter)

    def checkout(self, parameter, value):
        if self.get_parameter(parameter) == value:
            print(f"Item {self.id} checked out.")
        else:
            print(f"Item {self.id} not checked out.")

    def display_info(self):
        result = ""
        all_attributes = vars(self)
        for attribute_name, attribute_value in all_attributes.items():
            result += f"{attribute_name} is {attribute_value}\n"
        print(result)

    def __eq__(self, other):
        return self.id == other.id

class Book(LibraryItem):
    def __init__(self, id, title, year, author):
        super().__init__(id, title, year)
        self.author = author
        self.pages = 0
        self.cardboard = False
        self.isbn = ""
        self.publishing_house = ""

class Magazine(LibraryItem):
    def __init__(self, id, title, year, issue):
        super().__init__(id, title, year)
        self.publishing_agency = ""
        self.pages = 0
        self.paper = ""
        self.issn = ""

class DVD(LibraryItem):
    def __init__(self, id, title, year, director):
        super().__init__(id, title, year)
        self.director = director
        self.dubbed = False
        self.duration = 0
        self.language = ""
        self.subtitles = ""


lib = LibraryItem(1, "Ion", 1914)
lib2 = LibraryItem(1, "Ion", 1914)
book = Book(2, "Morometii", 1955, "Marin Preda")
book.set_parameter("pages", 500)
book.set_parameter("cardboard", True)
book.set_parameter("isbn", "123456789")
book.set_parameter("publishing_house", "Humanitas")
book.set_parameter("genre", "Roman")
book.set_parameter("language", "Romanian")
book.display_info()
magazine = Magazine(3, "National Geographic", 1888, 1)
magazine.set_parameter("publishing_agency", "National Geographic Society")
magazine.set_parameter("pages", 100)
magazine.set_parameter("paper", "Glossy")
magazine.set_parameter("issn", "123456789")
magazine.set_parameter("genre", "Adventure")
magazine.set_parameter("language", "English")
magazine.set_parameter("year", 2021)
magazine.display_info()
dvd = DVD(4, "The King's Speech", 2010, "Tom Hooper")
dvd.set_parameter("dubbed", True)
dvd.set_parameter("duration", 120)
dvd.set_parameter("language", "English")
dvd.set_parameter("subtitles", "Romanian")
dvd.set_parameter("genre", "Drama")
dvd.set_parameter("year", 2011)
dvd.display_info()
print(lib == book)
