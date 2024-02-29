import math


def find_gcd(number1, number2):
    """
    Find the greatest common divisor of two numbers
    :param number1: first number
    :param number2: second number
    :return:
    """
    while number2 != 0:
        remainder = number1 % number2
        number1 = number2
        number2 = remainder

    return number1


def split_in_numbers(string):
    """
    Split a string by spaces and return a list of numbers after verifying each element is a number
    :param string: the string to be split
    :return:
    """
    elements = string.split(" ")
    return [int(number) for number in elements if number.isdigit()]


def find_numbers(length):
    """
    Return a list of number depending on the length given
    :param length: the length of the list of numbers we want to return
    :return:
    """
    numbers = []
    while len(numbers) < length:
        numbers.extend(split_in_numbers(input()))
    numbers = numbers[:length]

    return numbers


def resolve():
    """
    Use the functions defined above to obtain the numbers and then find the gcd of those numbers
    """
    print("Write the number of numbers:")
    length = find_numbers(1)[0]

    print("Write the numbers with spaces:")
    numbers = find_numbers(length)

    print("Input numbers:", numbers)

    for i in range(1, length):
        numbers[i] = find_gcd(numbers[i], numbers[i - 1])
        # numbers[i] = math.gcd(numbers[i], numbers[i - 1])
    print("GCD of the numbers:", numbers[length - 1])


resolve()
