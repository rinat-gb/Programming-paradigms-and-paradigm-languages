#!/usr/bin/python3
#
# Семинар №4 модуля "Парадигмы программирования и языки парадигм"
#
# Контекст
# Корреляция - статистическая мера, используемая для оценки
# связи между двумя случайными величинами.
#
# Задача:
# Написать скрипт для расчета корреляции Пирсона между
# двумя случайными величинами (двумя массивами). Можете
# использовать любую парадигму, но рекомендую использовать
# функциональную, т.к. в этом примере она значительно
# упростит вам жизнь.
#
from random import sample
from typing import List
from statistics import mean


def pearson(array_x, array_y: List) -> float:
    mean_x = mean(array_x)
    mean_y = mean(array_y)
    numerator = sum(list(map(lambda x, y: (x - mean_x) * (y - mean_y), array_x, array_y)))
    sum_of_x_squares = sum(list(map(lambda x: (x - mean_x) ** 2, array_x)))
    sum_of_y_squares = sum(list(map(lambda y: (y - mean_y) ** 2, array_y)))
    denominator = (sum_of_x_squares * sum_of_y_squares) ** 0.5
    return numerator / denominator


print('Задание к семинару №4 модуля "Парадигмы программирования и языки парадигм"\n')

list0 = sample(range(100), 10)
print(f"Первый список: {list0}")
list1 = sample(range(100), len(list0))
print(f"Второй список: {list1}")

print(f"Корреляция Пирсона: {pearson(list0, list1)}")
