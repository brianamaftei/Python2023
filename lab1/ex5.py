matrix_example = [['1', '2', '3', '4', '5', '6'],
          ['20', '21', '22', '23', '24', '7'],
          ['19', '32', '33', '34', '25', '8'],
          ['18', '31', '36', '35', '26', '9'],
          ['17', '30', '29', '28', '27', '10'],
          ['16', '15', '14', '13', '12', '11']]

def spiral_walk(matrix):
    """
    The walk is symmetric, so we can walk in a direction and also in the opposite direction on the same line or column
    And at the end we can concatenate the two strings at every step
    :param matrix:
    :return:
    """
    length = len(matrix)

    for k in range(int(length / 2) + length % 2):
        first_part = ""
        second_part = ""

        for i in range(k, length - k):
            first_part += matrix[k][i]
            second_part += matrix[length - k - 1][length - i - 1]

        for i in range(k + 1, length - k - 1):
            first_part += matrix[i][length - k - 1]
            second_part += matrix[length - i - 1][k]

        print(first_part + second_part, end="")

spiral_walk(matrix_example)