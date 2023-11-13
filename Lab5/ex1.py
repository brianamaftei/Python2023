import math
import sys


class Shape:
    def __init__(self):
        self.perimeter = 0
        self.area = 0

    def set_parameter(self, parameter, value):
        try:
            if parameter not in vars(self).keys():
                raise AttributeError(f"\"{parameter}\" is an invalid parameter")
            else:
                self.__setattr__(parameter, value)
        except AttributeError as e:
            print(e)
            sys.exit()

    def __setattr__(self, key, value):
        try:
            if type(value) not in (int, float, complex, bool):
                raise TypeError(
                    f"The value of the \"{key}\" attribute in the {type(self).__name__} class must be a number")
            elif value is None or value < 0:
                raise ValueError(
                    f"The value of the \"{key}\" attribute in the {type(self).__name__} class must be greater than 0")
            else:
                object.__setattr__(self, key, value)
        except (ValueError, TypeError) as e:
            print(e)
            sys.exit()

    def __str__(self):
        result = f"{type(self).__name__}'s attributes: \n"
        all_attributes = list(vars(self).items())
        for attribute in all_attributes:
            result += f"{attribute[0]} = {attribute[1]} \n"
        return result


class Circle(Shape):
    def __init__(self, radius):
        Shape.__init__(self)
        self.radius = radius

    def set_perimeter(self):
        self.perimeter = 2 * math.pi * self.radius
        return self.perimeter

    def set_area(self):
        self.area = math.pi * self.radius ** 2
        return self.area


class Rectangle(Shape):
    def __init__(self, length, width):
        Shape.__init__(self)
        self.length = length
        self.width = width

    def set_perimeter(self):
        self.perimeter = 2 * (self.length + self.width)
        return self.perimeter

    def set_area(self):
        self.area = self.length * self.width
        return self.area


class Triangle(Shape):
    def __init__(self, a, b, c):
        Shape.__init__(self)
        self.a = a
        self.b = b
        self.c = c

    def set_perimeter(self):
        self.perimeter = self.a + self.b + self.c
        return self.perimeter

    def set_area(self):
        s = (self.a + self.b + self.c) / 2
        self.area = math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        return self.area

    def __setattr__(self, key, value):
        try:
            Shape.__setattr__(self, key, value)
            if key in ("a", "b", "c") and value <= 0:
                raise ValueError("The value of the sides of a triangle must be greater than 0")
            if hasattr(self, "a") + hasattr(self, "b") + hasattr(self, "c") == 3:
                if self.a + self.b <= self.c or self.a + self.c <= self.b or self.b + self.c <= self.a:
                    raise ValueError("The sum of any two sides of a triangle must be greater than the third side")
        except ValueError as e:
            print(e)
            sys.exit()


shape = Shape()
print(shape)
# shape.set_parameter("volume", 5)

circle = Circle(8)
# circle = Circle(-8)
# circle.perimeter = 2
# circle.radius = 8
circle.set_perimeter()
circle.set_area()
print(circle)

rectangle = Rectangle(5, 7)
# rectangle = Rectangle(5)
# rectangle.area = 2
rectangle.set_parameter("length", 5)
rectangle.set_perimeter()
rectangle.set_area()
print(rectangle)

triangle = Triangle(3, 4, 5)
# triangle = Triangle(3, 4, "5")
triangle.set_perimeter()
triangle.set_area()
print(triangle)
triangle.set_parameter("b", 3)
# triangle.c = "briana"
# triangle.set_perimeter()
# triangle.set_area()
print(triangle)
