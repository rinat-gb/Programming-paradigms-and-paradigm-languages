#!/usr/bin/python3
#
# Семинар №6 модуля "Парадигмы программирования и языки парадигм"
#
# Контекст
# Предположим, что мы хотим найти элемент в массиве (получить
# его индекс). Мы можем это сделать просто перебрав все элементы.
# Но что, если массив уже отсортирован? В этом случае можно
# использовать бинарный поиск. Принцип прост: сначала берём
# элемент находящийся посередине и сравниваем с тем, который мы
# хотим найти. Если центральный элемент больше нашего,
# рассматриваем массив слева от центрального, а если больше -
# справа и повторяем так до тех пор, пока не найдем наш элемент.
#
# Задача:
# Написать программу на любом языке в любой парадигме для
# бинарного поиска. На вход подаётся целочисленный массив и
# число. На выходе - индекс элемента или -1, в случае если искомого
# элемента нет в массиве.
#

from typing import List
from random import sample


def binary_search(array: List[int], number: int, left_idx: int, right_idx: int) -> int:
    if right_idx >= left_idx:
        middle_idx: int = left_idx + (right_idx - left_idx) // 2

        if array[middle_idx] == number:
            return middle_idx
        elif array[middle_idx] < number:
            return binary_search(array, number, middle_idx + 1, right_idx)
        else:
            return binary_search(array, number, left_idx, middle_idx - 1)
    else:
        return -1


def draw_line(line_len: int) -> None:
    print("----------", end='')
    print("+----" * line_len, end='')
    print('+')


def print_sorted_list(array: List[int]) -> None:
    draw_line(len(array))

    print("Индекс:   |", end='')
    for index in range(len(array)):
        print(f" {index:2} |", end='')
    print()
    draw_line(len(array))

    print("Значение: |", end='')
    for value in array:
        print(f" {value:2} |", end='')
    print()
    draw_line(len(array))
    print()


print('Задание к семинару №6 модуля "Парадигмы программирования и языки парадигм"\n')

arr = sample(range(100), 10)

print("Список до сортировки:")
print_sorted_list(arr)

arr.sort()

print("Список после сортировки (алгоритм бинарного поиска требует отсортированный массив):")
print_sorted_list(arr)

while True:
    num = input("Введите число которое хотите найти: ")

    try:
        num = int(num)
    except ValueError:
        print("Вы ввели какое-то не число, повторите ввод")
        continue
    break

idx = binary_search(arr, num, 0, len(arr) - 1)

if idx == -1:
    print("Такого числа в данном массиве нет!")
else:
    print(f"Число {num} находится в массиве по индексу {idx}")
