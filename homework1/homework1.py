#!/usr/bin/python3
#
# Семинар №1 модуля "Парадигмы программирования и языки парадигм"
#
# Задание:
# Дан список целых чисел numbers. Необходимо написать в императивном стиле процедуру для
# сортировки числа в списке в порядке убывания. Можно использовать любой алгоритм сортировки.

import copy
import random
from typing import List


def sort_list_imperative(array: List) -> List:
    sorted_array = copy.deepcopy(array)
    listSize = len(sorted_array)
    swapped = False

    for i in range(listSize - 1):
        for j in range(0, listSize - i - 1):
            if sorted_array[j] < sorted_array[j + 1]:
                swapped = True
                sorted_array[j], sorted_array[j + 1] = sorted_array[j + 1], sorted_array[j]

        if not swapped:
            return sorted_array

    return sorted_array


def sort_list_declarative(array: List) -> List:
    return sorted(array, reverse=True)


if __name__ == '__main__':
    print('Задание к семинару №1 модуля "Парадигмы программирования и языки парадигм"\n')
    numbers = random.sample(range(1, 100), 10)

    print(f"             Несортированный список чисел: {numbers}")
    print(f" Императивно отсортированный список чисел: {sort_list_imperative(numbers)}")
    print(f"Декларативно отсортированный список чисел: {sort_list_declarative(numbers)}")
