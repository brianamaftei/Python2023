def max_letter(text):
    """
    Finds the most frequent letter in a string
    :param text: the string to be searched for the most frequent letter
    :return: the most frequent letter
    """
    counter_max = 0
    char_max = ""

    for char in text:
        if text == "":
            break
        if char.isalpha():
            if text.count(char) > counter_max:
                counter_max = text.count(char)
                char_max = char
        text = text.replace(char, "")

    return char_max


print(max_letter("aabbccddccccc zzzzzzzzzzzzzzzzzz"))
