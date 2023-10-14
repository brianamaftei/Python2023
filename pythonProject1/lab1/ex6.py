number_example = 1234321


def verify_palindrome(number):
    """
    Verifies if a number is a palindrome
    :param number: the number to be verified
    :return: true if the number is a palindrome, False otherwise
    """
    return str(number) == str(number)[::-1]


print(verify_palindrome(number_example))
