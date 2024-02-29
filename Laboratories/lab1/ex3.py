first_string_example = "an"
second_string_example = "ana and dan land in a land"


def occurrences(first_string, second_string):
    """
    Counts the occurrences of a string in another string
    Args:
        first_string: the string to be searched for
        second_string: the string to be searched in

    Returns:
        the number of occurrences of a_string in b_string
    """
    return len(second_string.split(first_string)) - 1


print(occurrences(first_string_example, second_string_example))
