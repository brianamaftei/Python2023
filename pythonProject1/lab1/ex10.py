text_example = "I have Python exam"


def count_words(text):
    """
    It counts the number of words in a string
    :param text:
    :return:
    """
    return len(text.split(" "))


print(count_words(text_example))
