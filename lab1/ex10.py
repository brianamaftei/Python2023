import re

text_example = "I have         Python exam"


def count_words(text):
    """
    It counts the number of words in a string
    :param text:
    :return:
    """
    # return len(text.split(" "))
    return len(re.split("\s+", text))
    # return re.split("\s+", text)

print(count_words(text_example))
