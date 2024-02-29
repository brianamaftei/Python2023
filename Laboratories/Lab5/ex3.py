class Vehicle:
    def __init__(self, made_by, model, year, consumption, weight, fuel=None):
        self.made_by = made_by
        self.model = model
        self.year = year
        self.weight = weight
        self.kilometers = 0
        if fuel is None:
            self.fuel = 0
        else:
            self.fuel = fuel
        self.consumption = consumption
        self.fuel_consumed = 0


    def fill_up(self, fuel):
        self.fuel += fuel

    def mileage(self, kilometers):
        try:
            if kilometers < 0:
                raise ValueError("Kilometers can't be negative")
            if self.fuel < kilometers * self.consumption / 100:
                raise ValueError("Not enough fuel")
            else:
                self.kilometers += kilometers
                self.fuel_consumed += kilometers * self.consumption / 100
                self.fuel -= kilometers * self.consumption / 100
        except ValueError as e:
            print(e)

    def towing(self, weight):
        try:
            if weight < 0:
                raise ValueError("Weight can't be negative")
            if weight >= self.weight:
                raise ValueError(f"Not enough power for {self.model} to tow {weight}")
            else:
                self.weight -= weight
        except ValueError as e:
            print(e)

    def set_made(self, made):
        self.made_by = made

    def set_model(self, model):
        self.model = model

    def set_year(self, year):
        self.year = year

    def get_made(self):
        return self.made_by

    def get_model(self):
        return self.model

    def get_year(self):
        return self.year

    def __str__(self):
        result = f"{type(self).__name__}'s information: \n"
        all_attributes = list(vars(self).items())
        for attribute in all_attributes:
            result += f"{attribute[0]} is {attribute[1]} \n"
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self)

class Car(Vehicle):
    def __init__(self, made_by, model, year, consumption, weight, fuel=None):
        Vehicle.__init__(self, made_by, model, year, consumption, weight, fuel)

class Truck(Vehicle):
    def __init__(self, made_by, model, year, consumption, weight, fuel=None):
        Vehicle.__init__(self, made_by, model, year, consumption, weight, fuel)

class Motorcycle(Vehicle):
    def __init__(self, made_by, model, year, consumption, weight, fuel=None):
        Vehicle.__init__(self, made_by, model, year, consumption, weight, fuel)


with Car("BMW", "X5", 2019, 8, 2000) as car:
    car.fill_up(100)
    car.mileage(100)
    car.towing(100)
    car.set_made("Mercedes")
    car.set_model("E")
    car.set_year(2020)

with Truck("Mercedes", "Actros", 2019, 20, 10000) as truck:
    truck.fill_up(100)
    truck.mileage(100)
    truck.towing(1000000)
    truck.set_made("Mercedes")
    truck.set_model("E")
    truck.set_year(2020)

motorcycle = Motorcycle("Honda", "CBR", 2019, 5, 200)
motorcycle.fill_up(100)
motorcycle.mileage(100)
motorcycle.towing(100)
print(motorcycle)

