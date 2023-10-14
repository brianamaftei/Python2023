
def recursive_count_vowels(a_string):
    """
    This function counts the number of vowels in a string using recursion
    :param a_string: the string to be searched for vowels
    :return: the number of vowels in the string
    """
    if len(a_string) == 0:
        return 0
    else:
        return int(a_string[0] in "aeiouAEIOU") + recursive_count_vowels(a_string[1:])


print(recursive_count_vowels("aeBiouaABriana"))
print(recursive_count_vowels("casian"))
