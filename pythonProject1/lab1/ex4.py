upper_string_example = "UpperCamelCase"


def transform_underscore(upper_string):
    """
    Transforms a string from UpperCamelCase to lower_underscore_case
    :param upper_string: the string to be transformed
    :return: the transformed string
    """
    lower_string = ""
    for char in upper_string:
        if "A" <= char <= "Z":
            lower_string += ("_" + char.lower())
        else:
            lower_string += char
    lower_string = lower_string[1:]
    return lower_string


print(transform_underscore(upper_string_example))
