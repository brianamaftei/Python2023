def count_bits(number):
    """
    Brian Kernighan's algorithm or the "count set bits" algorithm
    :param number: the number to be checked
    :return: the number of 1 bits in the number
    """
    count = 0
    while number:
        number &= (number - 1)
        count += 1
    return count


def count_set_bits(number):
    """
    This function counts the number of set bits in a number using the bin() function and the count() method
    :param number: the number to be checked
    :return: the number of 1 bits in the number
    """
    return bin(number).count("1")


print(count_bits(1))
print(count_set_bits(1))
