text_example = "ana are pere2"


def extract_number(text):
    """
    Extracts the first number from a string
    :param text: the text given to be searched for a number
    :return: the first number found in the string
    """
    number = ""
    for char in text:
        if char.isdigit():
            number += char
        elif number != "":
            break
    return number


print(extract_number(text_example))
