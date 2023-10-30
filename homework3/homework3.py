#!/usr/bin/python3
#
# Семинар №3 модуля "Парадигмы программирования и языки парадигм"
#
# Задача:
# Написать игру в “Крестики-нолики”. Можете использовать
# любые парадигмы, которые посчитаете наиболее
# подходящими. Можете реализовать доску как угодно - как
# одномерный массив или двумерный массив (массив массивов).
# Можете использовать как правила, так и хардкод, на своё
# усмотрение. Главное, чтобы в игру можно было поиграть через
# терминал с вашего компьютера.
#
import sys
# !/usr/bin/env python3

from abc import ABC, abstractmethod
from copy import deepcopy
from random import randint
from typing import List, Literal, Optional, Tuple

Player = Literal['X', 'O']


class TicTacToe(ABC):
    ROWS = 3
    COLS = 3

    def __init__(self: 'TicTacToe') -> None:
        self._human_player: Player = 'X'
        self._computer_player: Player = 'O'
        self._is_computer_move: bool = False
        self._board: List = [[(r * TicTacToe.ROWS + c + 1)
                              for c in range(0, TicTacToe.COLS)] for r in range(0, TicTacToe.ROWS)]

    @property
    def human_player(self: 'TicTacToe') -> Player:
        return self._human_player

    @human_player.setter
    def human_player(self: 'TicTacToe', value: Player) -> None:
        self._human_player = value

    @property
    def computer_player(self: 'TicTacToe') -> Player:
        return self._computer_player

    @computer_player.setter
    def computer_player(self: 'TicTacToe', value: Player) -> None:
        self._computer_player = value

    @property
    def is_computer_move(self: 'TicTacToe') -> bool:
        return self._is_computer_move

    @is_computer_move.setter
    def is_computer_move(self: 'TicTacToe', value: bool) -> None:
        self._is_computer_move = value

    @abstractmethod
    def calc_move(self: 'TicTacToe') -> int:
        pass

    def print_board(self: 'TicTacToe') -> None:
        for r in self._board:
            print('|', end='')

            for c in r:
                print(f'{c}|', end='')
            print()
        print()

    def has_game_over(self: 'TicTacToe') -> List:
        return TicTacToe._has_game_over(self._board)

    def do_move(self, move, player) -> Optional[int]:
        return TicTacToe._do_move(self._board, move, player)

    @staticmethod
    def _has_game_over(board: List) -> List:
        if TicTacToe._has_won(board, 'X'):
            return [True, 'X']
        elif TicTacToe._has_won(board, 'O'):
            return [True, 'O']
        elif not TicTacToe._moves_available(board):
            return [True, '-']
        else:
            return [False, '']

    @staticmethod
    def _do_move(board: List, move: int, player: Player) -> Optional[int]:
        if move not in range(1, TicTacToe.ROWS * TicTacToe.COLS + 1):
            return None

        r, c = TicTacToe._move_to_row_col(move)

        if board[r][c] != 'X' and board[r][c] != 'O':
            prev_move = board[r][c]
            board[r][c] = player
            return prev_move

        return None

    @staticmethod
    def _move_to_row_col(move: int) -> Tuple:
        r = (move - 1) // TicTacToe.ROWS
        c = (move - 1) % TicTacToe.COLS

        return (r, c)

    @staticmethod
    def _moves_available(board: List) -> List:
        availables = []

        for r in board:
            for c in r:
                if c != 'X' and c != 'O':
                    availables.append(c)

        return availables

    @staticmethod
    def _has_won(board: List, player: Player) -> bool:
        for r in board:
            if r.count(player) == TicTacToe.COLS:
                return True

        for c in range(TicTacToe.COLS):
            column_complete = True

            for r in range(TicTacToe.ROWS):
                if board[r][c] != player:
                    column_complete = False
                    break

            if column_complete:
                return True

        for x in range(TicTacToe.ROWS):
            if board[x][x] != player:
                break
        else:
            return True

        for x in range(TicTacToe.ROWS):
            if board[x][TicTacToe.ROWS - x - 1] != player:
                break
        else:
            return True

        return False


class EasyTicTacToe(TicTacToe):

    def calc_move(self: 'EasyTicTacToe') -> int:
        availables = self._moves_available(self._board)
        return availables[randint(0, len(availables) - 1)]


class HardTicTacToe(TicTacToe):

    def calc_move(self: 'HardTicTacToe') -> int:
        if len(TicTacToe._moves_available(self._board)) == TicTacToe.ROWS * TicTacToe.COLS:
            return TicTacToe.ROWS // 2 * TicTacToe.ROWS + TicTacToe.COLS // 2 + 1

        return HardTicTacToe._minimax(self._board, self.computer_player == 'X')[1]

    @staticmethod
    def _check_board(board: List) -> int:
        if TicTacToe._has_won(board, 'X'):
            return 1
        elif TicTacToe._has_won(board, 'O'):
            return -1
        else:
            return 0

    @staticmethod
    def _minimax(board: List, is_next_move_x: bool) -> Tuple[float, int]:
        check = TicTacToe._has_game_over(board)
        if check[0]:
            return HardTicTacToe._check_board(board), 0

        computed_move = 0

        if is_next_move_x:
            computed_value = -float('Inf')
            player = 'X'
        else:
            computed_value = float('Inf')
            player = 'O'

        board_cloned = deepcopy(board)

        for move in TicTacToe._moves_available(board):
            prev_move = TicTacToe._do_move(board_cloned, move, player)
            new_value = HardTicTacToe._minimax(
                board_cloned, not is_next_move_x)[0]

            if is_next_move_x and new_value > computed_value:
                computed_value = new_value
                computed_move = move
            elif not is_next_move_x and new_value < computed_value:
                computed_value = new_value
                computed_move = move

            r, c = TicTacToe._move_to_row_col(move)
            board_cloned[r][c] = prev_move

        return computed_value, computed_move


# def show_board(game, showMsg=True):
#     msg = "Выбирай на какое поле\n" \
#           "ты поставишь свой {}".format(game.human_player)
#
#     if showMsg:
#         return (msg, game.print_board())
#     else:
#         return ('', game.print_board())
#
#
# def show_winner(call, game, winner):
#     if winner == game.human_player:
#         bot.send_message(call.message.chat.id, 'Чёрт! Ты выиграл!')
#     elif winner == game.computer_player:
#         bot.send_message(call.message.chat.id,
#                          'Я выиграл!\nНо я и подозревал что я умнее тебя!')
#     else:
#         bot.send_message(call.message.chat.id,
#                          'Однако победила дружба - НИЧЬЯ!')
#
#
# @bot.callback_query_handler(func=None)
# def callback_reply(call: CallbackQuery):
#     game: TicTacToe = unique_dict.get(call.message.chat.id)
#
#     if call.data == CHOOSE_LEVEL:
#         msg, markup = choose_level()
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data == CHOOSE_EASY:
#         unique_dict[call.message.chat.id] = EasyTicTacToe()
#         msg, markup = choose_player()
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data == CHOOSE_HARD:
#         unique_dict[call.message.chat.id] = HardTicTacToe()
#         msg, markup = choose_player()
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data == CHOOSE_X:
#         game.human_player = 'X'
#         game.computer_player = 'O'
#         bot.send_message(call.message.chat.id, 'Тогда ты начинаешь!')
#         msg, markup = show_board(game)
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data == CHOOSE_O:
#         game.human_player = 'O'
#         game.computer_player = 'X'
#         bot.send_message(call.message.chat.id, 'Тогда я начинаю!')
#
#         move = game.calc_move()
#         game.do_move(move, 'X')
#         msg, markup = show_board(game)
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data == OCCUPIED:
#         bot.send_message(call.message.chat.id,
#                          'На эту клетку уже ходили, переходи!')
#         msg, markup = show_board(game, False)
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#         return
#
#     elif call.data.startswith('CHOOSE_'):
#         move = int(call.data[7:])
#         game.do_move(move, game.human_player)
#         msg, markup = show_board(game)
#         bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#
#         status, winner = game.has_game_over()
#         if status:
#             show_winner(call, game, winner)
#
#             msg, markup = new_game()
#             bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#             return
#
#         move = game.calc_move()
#         game.do_move(move, game.computer_player)
#         msg, markup = show_board(game, False)
#         bot.send_message(call.message.chat.id,
#                          'А я отвечу вот так!', reply_markup=markup)
#
#         status, winner = game.has_game_over()
#         if status:
#             show_winner(call, game, winner)
#
#             msg, markup = new_game()
#             bot.send_message(call.message.chat.id, msg, reply_markup=markup)
#             return
#
#         bot.send_message(call.message.chat.id, 'Твой ход!')
#         return
#
#     else:
#         return


print('Задание к семинару №3 модуля "Парадигмы программирования и языки парадигм"\n')


# game = HardTicTacToe()
# game.human_player = 'O'
# game.computer_player = 'X'
#
# while True:
#     move = game.calc_move()
#     game.do_move(move, game.computer_player)
#     game.print_board()
#     status = game.has_game_over()
#     if status[0]:
#         break
#     move = int(input('Ваш ход: '))
#     game.do_move(move, game.human_player)
#     game.print_board()
#     status = game.has_game_over()
#     if status[0]:
#         break

def wait_certain_letter(msg: str, availables: str) -> str:
    while True:
        print(msg, end='')

        answer = input().lower()
        if len(answer) != 1 or answer not in availables:
            print("Неправильный ввод!")
            continue
        return answer


answer = wait_certain_letter('Если хочешь сыграть в "Крестики-нолики"?\n' \
                             'Ответь [Д]а или [Н]ет ([Y]es или [N]o: ', 'днyn')
if answer in 'нn':
    print("Пока! Увидимся в следующий раз!")
    sys.exit(0)

answer = wait_certain_letter('Хочешь играть когда я [Т]упой или [У]мный?: ', 'ту')

game = EasyTicTacToe() if answer == 'т' else HardTicTacToe()

answer = wait_certain_letter('Хочешь играть крестиками [X] или ноликами [O]?: ', 'xoхо')

if answer in 'xх':
    game.human_player = 'X'
    game.computer_player = 'O'
else:
    game.human_player = 'O'
    game.computer_player = 'X'

if game.computer_player == 'X':
    print("Я начинаю!")
    game.is_computer_move = True
else:
    print("Ты начинаешь!")
    game.is_computer_move = False

print()

while True:
    game.print_board()

    if game.is_computer_move:
        move = game.calc_move()
        print(f"Я поставлю свой '{game.computer_player}' на клетку под номером {move}!")
        game.do_move(move, game.computer_player)
        game.print_board()

        status = game.has_game_over()
        if status[0]:
            if status[1] == game.computer_player:
                print("Ха! Я выиграл!")
            else:
                print("Я сделал ничью!")

            break

        print('Отвечай!')

    while True:
        print(f"Выбирай куда ты поставишь свой '{game.human_player}': ", end='')
        move = input()

        try:
            move = int(move)
        except ValueError:
            print("Ты ввёл не число, повтори ввод!")
            continue

        if game.do_move(move, game.human_player) is None:
            print("На какую-то странную клетку ты пошёл, повтори ввод!")
            continue
        else:
            break

    game.print_board()

    status = game.has_game_over()
    if status[0]:
        if status[1] == game.human_player:
            print("Ты выиграл!")
        else:
            print("Ты сделал ничью!")

        break

    game.is_computer_move = True
