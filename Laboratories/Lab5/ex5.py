class Animal:
    def __init__(self, name, specie, date_of_birth):
        self.name = name
        self.species = specie
        self.date_of_birth = date_of_birth
        self.age = 0
        self.weight = 0
        self.height = 0
        self.sound = ""
        self.babies = []
        self.food = []
        self.habitat = []
        self.parents = []

    def get_parameter(self, parameter):
        return getattr(self, parameter)

    def set_parameter(self, parameter, value):
        old_value = self.get_parameter(parameter)
        if type(old_value) == type(value):
            setattr(self, parameter, value)
        else:
            print("Invalid value type.")

    def make_sound(self):
        print(self.sound)

    def feed(self, food):
        if food in self.food:
            print(f"{self.name} is eating {food}.")
        else:
            print(f"{self.name} doesn't eat {food}.")

    def __str__(self):
        result = "Info:\n"
        all_attributes = vars(self)
        for attribute_name, attribute_value in all_attributes.items():
            if isinstance(attribute_value, list) and all(isinstance(item, Animal) for item in attribute_value):
                result += f"{attribute_name} names are {list(animal.name for animal in attribute_value)}\n"
            else:
                result += f"{attribute_name} is {attribute_value}\n"
        return result


class Mammal(Animal):
    def __init__(self, name, specie, date_of_birth):
        super().__init__(name, specie, date_of_birth)
        self.fur_type = ""
        self.lactation = False
        self.paw = 0

    def give_birth(self, baby):
        if isinstance(baby, Mammal):
            self.babies.append(baby)
            baby.parents.append(self)
        else:
            print("Invalid baby type.")

    def feed_baby(self, baby):
        if not self.lactation:
            print(f"{self.name} doesn't lactate.")
        elif baby in self.babies:
            print(f"{self.name} is feeding {baby.name}.")
        else:
            print(f"{self.name} doesn't have {baby.name} as a baby.")


class Bird(Animal):
    def __init__(self, name, specie, date_of_birth):
        super().__init__(name, specie, date_of_birth)
        self.feather_color = ""
        self.migratory = False
        self.fly_speed = 0
        self.fly = False
        self.eggs = 0
        self.wings = 2

    def lay_eggs(self, eggs):
        self.eggs += eggs

    def fly(self):
        if self.fly:
            print(f"{self.name} is flying.")
        else:
            print(f"{self.name} can't fly.")


class Fish(Animal):
    def __init__(self, name, specie, date_of_birth):
        super().__init__(name, specie, date_of_birth)
        self.fin_dimension = 0
        self.water_temperature = ""
        self.roe = False

    def lay_roe(self):
        if self.roe:
            print(f"{self.name} is laying roe.")
        else:
            print(f"{self.name} can't lay roe.")

    def verify_temperature(self, temperature):
        if temperature == self.water_temperature:
            print(f"{self.name} is in the right temperature.")
        else:
            print(f"{self.name} is not in the right temperature, it should be in {self.water_temperature}.")


animal = Animal("Oscar", "cat", "12/12/2022")
print(animal)

dog = Mammal("Lizzy", "dog", "12/12/2020")
dog1 = Mammal("Bobita", "dog", "12/12/2023")
dog.set_parameter("sound", "ham ham")
dog.set_parameter("weight", 10)
dog.set_parameter("lactation", True)
dog.set_parameter("fur_type", "long")
dog.set_parameter("paw", 4)
dog.set_parameter("food", ["meat", "bones"])
dog.set_parameter("habitat", ["house", "yard"])
dog.make_sound()
dog.feed("meat")
dog.feed("vegetables")
dog.give_birth(animal)
dog.give_birth(dog1)
dog.feed_baby(animal)
print(dog)
print(dog1)


bird1 = Bird("Tweety", "bird", "12/12/2020")
bird1.set_parameter("sound", "cip cip")
bird1.set_parameter("weight", 0.5)
bird1.set_parameter("feather_color", "yellow")
bird1.set_parameter("migratory", True)
bird1.set_parameter("fly_speed", 20)
bird1.set_parameter("fly", True)
bird1.set_parameter("eggs", 2)
bird1.set_parameter("food", ["seeds", "insects"])
bird1.set_parameter("habitat", ["forest", "house"])
bird1.make_sound()
bird1.feed("seeds")
bird1.feed("meat")
bird1.lay_eggs(2)
print(bird1)

fish1 = Fish("Nemo", "fish", "12/12/2020")
fish1.set_parameter("sound", "blub blub")
fish1.set_parameter("weight", 0.5)
fish1.set_parameter("fin_dimension", 10)
fish1.set_parameter("water_temperature", "cold")
fish1.set_parameter("roe", True)
fish1.set_parameter("food", ["seeds", "insects"])
fish1.set_parameter("habitat", ["sea", "aquarium"])
fish1.make_sound()
fish1.feed("seeds")
fish1.feed("meat")
fish1.lay_roe()
fish1.verify_temperature("cold")
fish1.verify_temperature("hot")
print(fish1)

