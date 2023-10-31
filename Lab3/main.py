def set_operations(list_a, list_b):
    # return [set(list_a) & set(list_b), set(list_a) | set(list_b), set(list_a) - set(list_b),
    # set(list_b) - set(list_a)]
    return [set(list_a).intersection(set(list_b)), set(list_b).union(set(list_a)), set(list_a).difference(set(list_b)),
            set(list_b).difference(set(list_a))]


def set_of_occurrences(string):
    return {char: string.count(char) for char in set(string)}  # set conversteste stringul in multime


# def recursive_values(entry):
#     if type(entry) == dict:
#         return [[recursive_values(item[0]), recursive_values(item[1])] for item in entry.items()]
#     elif type(entry) in (list, tuple, set, frozenset):
#         return [recursive_values(item) for item in entry]
#     # elif type(entry) == frozenset:
#     #     return [recursive_values(item) for item in set(entry)]
#     else:  # string, number, etc
#         return str(entry)
#

def recursive_values(dict1, dict2):
    if type(dict1) != type(dict2):
        return 0
    elif type(dict) in (list, tuple, set, frozenset):
        if len(dict1) != len(dict2):
            return 0
        else:
            for i in range(len(dict1)):
                if recursive_values(dict1[i], dict2[i]) == 0:
                    return 0
            return 1
    elif type(dict1) == dict:
        if len(dict1) != len(dict2):
            return 0
        else:
            for key in dict1.keys():
                if key not in dict2.keys():
                    return 0
                if recursive_values(dict1[key], dict2[key]) == 0:
                    return 0
            return 1
    elif type(dict1) in (int, float, str):
        return 1 if dict1 == dict2 else 0


def build_xml_element(tag, content, **key_values):
    merged_key_values = ""
    for key, value in key_values.items():
        merged_key_values += f"{key}=\\\"{value}\\\""
    return f"<{tag} {merged_key_values}>{content}</{tag}>"


def validate_dict(rules, dictionary):
    m_rules = {rule[0]: [rule[1], rule[2], rule[3]] for rule in rules}
    return all([item[0] in m_rules and item[1].startswith(m_rules[item[0]][0])
                and item[1].endswith(m_rules[item[0]][2])
                and m_rules[item[0]][1] in item[1][len(m_rules[item[0]][0]): len(item[1]) - len(m_rules[item[0]][2])]
                for item in dictionary.items()])

#7
def operation_dictionary(*sets):
    dictionary = {}
    for index1, s1 in enumerate(sets):
        for index2, s2 in enumerate(sets):
            if s2 != s1 and index2 > index1:
                dictionary[f"{s1}|{s2}"] = s1.union(s2)
                dictionary[f"{s1}&{s2}"] = s1.intersection(s2)
                dictionary[f"{s1}-{s2}"] = s1.difference(s2)

    return dictionary

#6
def count_uniqueness_duplicates(lst):
    uniqueness = 0
    duplicates = 0
    for el in set(lst):
        if lst.count(el) == 1:
            uniqueness += 1
        else:
            duplicates += 1
    return uniqueness, duplicates

    # varianta mai misto
    # return sum(lst.count(el) == 1 for el in set(lst)), sum(lst.count(el) != 1 for el in set(lst))


# 8
def loop(mapping):
    lst = []
    last_value = mapping['start']
    while last_value not in lst:
        lst.append(last_value)
        last_value = mapping[last_value]
    return lst


def count_values(*values, **key_values):
    return len([value for value in values if value in set(key_values.values())])


if __name__ == '__main__':
    # print(set_operations([1, 2, 3, 8], [0, 2, 3, 4, 4]))

    # print(set_of_occurrences("adrenaline"))
    # print(set_of_occurrences("Ana has apples."))

    # print(compare_dictionary({("abc", frozenset({"a", 34, frozenset({2, 3})})): [1, 2, 3]}, {5: (3, 4)}))
    # print(compare_dictionary({("abc", frozenset({"a", 34, frozenset({2, 3})})): [1, 2, 3], 5: 3},
    #                          {5: 3, ("abc", frozenset({"a", 34, frozenset({3, 2})})): [1, 2, 3]}))
    print(recursive_values({("abc", frozenset({"a", 34, frozenset({2, 3})})): [1, 2, 3], 5: 3},
                           {5: 3, ("abc", frozenset({"a", 34, frozenset({3, 2})})): [1, 2, 3]}))
    print(recursive_values({("abc", frozenset({"a", 34, frozenset({2, 3})})): [1, 2, 3]}, {5: (3, 4)}))
    print(recursive_values({"a": (3, 4), "b": {1: "5"}}, {"a": (3, 4), "b": {1: "6"}}))

    # print(compare_dictionary({"a": (0, 3, 4), 5: 7, 'b': -2}, {5: 7, 'b': -2, "a": (0, 3, 4)}))
    # print(compare_dictionary({"a": (0, 3, 4), 9: 7, 'b': -2}, {5: 0, 'b': -2, "a": (0, 3, 4)}))

    # print(build_xml_element("a", "Hello there", href=" http://python.org ", _class=" my-link ", id=" someid "))

    # print(validate_dict({("key1", "r", "inside", "t"), ("key2", "start", "middle", "winter")}, {"key1": "rinsidet"}))
    # print(validate_dict({("key1", "", "inside", ""), ("key2", "start", "middle", "winter")},
    #                     {"key1": "come inside, it's too cold out", "key3": "this is not valid"}))

    # print(count_uniqueness_duplicates([1, 7, 2, 3, 2, 5, 7]))

    # print(operation_dictionary({1, 2}, {2, 3}, {0}))

    # print(loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))

    # print(count_values(1, 2, 'rea', 4, x=1, y='rea', z=3, w=5))
    # print(count_values(1, 2, 3, 4, x=1, y=2, z=3, w=5))
