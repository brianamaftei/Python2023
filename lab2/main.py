def fibonacci_n(n):
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        list_f = fibonacci_n(n - 1)
        list_f.append(list_f[-1] + list_f[-2])
        return list_f


def prime_list(list_of_number):
    return [number for number in list_of_number if
            len([div for div in range(2, number // 2 + 1) if number % div == 0]) == 0]


# no duplicates requirement
def reunion_intersection_minus(list_a, list_b):
    list_reunion = []
    list_intersection = []
    list_a_minus_b = []
    list_b_minus_a = []

    for number in list_a:
        if number in list_b:
            list_intersection.append(number)
        else:
            list_a_minus_b.append(number)
        list_reunion.append(number)

    for number in list_b:
        if number not in list_a:
            list_b_minus_a.append(number)
            list_reunion.append(number)

    return list_reunion, list_intersection, list_a_minus_b, list_b_minus_a


def eliminate_duplicates(list_x):
    index = 0
    while index < len(list_x):
        if list_x.count(list_x[index]) > 1:
            del list_x[index]
        else:
            index += 1

    return sorted(list_x)


def union(list_a, list_b):
    return eliminate_duplicates(list_a + list_b)


def intersection(list_a, list_b):
    return [number for number in list_a if number in list_b]


def list_minus_list(list_a, list_b):
    return [number for number in list_a if list_b.count(number) == 0]


def operation_with_lists(list_a, list_b):
    print(union(list_a, list_b))
    print(intersection(list_a, list_b))
    print(list_minus_list(list_a, list_b))
    print(list_minus_list(list_b, list_a))


def compose(musical_notes, moves, current_position):
    composition = [musical_notes[current_position]]
    for move in moves:
        current_position = (current_position + move + int(current_position + move < 0) * (len(musical_notes))) % len(
            musical_notes)
        composition.append(musical_notes[current_position])
    return composition


def fill_diagonal(matrix):
    i = 0
    while i < len(matrix[0]):
        for index in range(0, i):
            matrix[i][index] = 0
        i += 1

    while i < len(matrix):
        for index in range(0, len(matrix[0])):
            matrix[i][index] = 0
        i += 1

    return matrix


def x_times(*lists, x):
    merged_list = []
    for lst in lists:
        merged_list.extend(lst)
    return [number for index, number in enumerate(merged_list) if
            merged_list.count(number) == x and number not in merged_list[:index]]


def palindrome_tuple(lst):
    list_palindromes = [number for number in lst if str(number) == str(number)[::-1]]
    return len(list_palindromes), max(list_palindromes)


# def unicode_x(list_of_strings, x=1, flagged=True):
#     list_of_lists = []
#     if flagged:
#         for string in list_of_strings:
#             list_of_lists.append([char for char in string if ord(char) % x == 0])
#     else:
#         for string in list_of_strings:
#             list_of_lists.append([char for char in string if ord(char) % x != 0])
#
#     return list_of_lists

def unicode_x(list_of_strings, x=1, flag=True):
    return [[char for char in string if ord(char) % x == 0] if flag else [char for char in string if ord(char) % x != 0]
            for string in list_of_strings]


def problem_seats(matrix):
    transpose_tuple = tuple(zip(*matrix))
    list_of_seats = []
    for row in range(0, len(transpose_tuple)):
        for column in range(1, len(transpose_tuple[0])):
            if transpose_tuple[row][column] <= max(transpose_tuple[row][:column]):
                list_of_seats.append((column, row))
    return list_of_seats


def zip_of_lists(*lists):
    max_length = max([len(lst) for lst in lists])
    # return list(zip(*[lst + [None] * (max_length - len(lst)) if len(lst) != max_length else lst for lst in lists]))
    return list(zip(*[lst + [None] * (max_length - len(lst)) for lst in lists]))


def sort_by_2nd_3rd(list_of_string_tuples):
    return sorted(list_of_string_tuples, key=lambda x: x[1][2])


def rhyme(list_of_words):
    list_sorted = sorted(list_of_words, key=lambda x: x[-2:])
    list_of_lists = []
    a_list = [list_sorted[0]]
    for index in range(1, len(list_sorted)):
        if list_sorted[index][-2:] == list_sorted[index - 1][-2:]:
            a_list.append(list_sorted[index])
        else:
            list_of_lists.append(a_list)
            a_list = [list_sorted[index]]
    list_of_lists.append(a_list)
    return list_of_lists


def rhyme_2(list_of_words):
    return list(list(filter(lambda element: element[-2:] == last_two_letters, list_of_words)) for last_two_letters in
                set([word[-2:] for word in list_of_words]))


if __name__ == '__main__':
    # print(fibonacci_n(7))

    # list_1 = [12, 45, 2]
    # print(prime_list(list_1))

    # list_A = [1, 2, 3, 4, 5]
    # list_B = [3, 4, 5, 6, 7]
    # operation_with_lists(list_A, list_B)
    # print(reunion_intersection_minus(list_A, list_B))

    # print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
    # print(compose(["do", "re", "mi", "fa", "sol", "la", "si"], [1, -6, 4, -2], 2))

    # matrix_2 = [['1', '2', '3', '4', '5', '6'],
    #           ['20', '21', '22', '23', '24', '7'],
    #           ['19', '32', '33', '34', '25', '8'],
    #           ['18', '31', '36', '35', '26', '9'],
    #           ['17', '30', '29', '28', '27', '10'],
    #           ['16', '15', '14', '13', '12', '11'],
    #           ['16', '15', '14', '13', '12', '11']]
    #
    # print(fill_diagonal(matrix_2))

    # print(x_times([1, 2, 3, 4, 6], [1, 2], [1, 2, 3], [6], [1, 2, 4], [5, 2, 6], [1, 5], [1, 5, 3], [4, 6], x=))
    # print(x_times([1,2,3], [2,3,4],[4,5,6], [4,1, "test"] , x=2))

    # print(palindrome_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 121, 1100, 1001, 35, 345]))

    # print(unicode_x(["abc", "bcd", "cde"], 3, True))

    # matrix_ = [[1, 2, 3, 2, 1, 1],
    #            [2, 4, 4, 3, 7, 2],
    #            [5, 5, 2, 5, 6, 4],
    #            [6, 6, 7, 6, 7, 5]]
    # print(problem_seats(matrix_))

    # print(zip_of_lists([1, 2, 3], [4, 5, 6], [7, 8, 9]))
    # print(zip_of_lists([1, 2, 3], [5, 6, 7], ["a", "b"]))

    # print(sort_by_2nd_3rd([('abc', 'bcd'), ('abc', 'zza'), ('aaa', 'saas', 'yy')]))

    # print(rhyme(['ana', 'banana', 'carte', 'arme', 'parte']))
    print(rhyme_2(['ana', 'banana', 'carte', 'arme', 'parte']))
