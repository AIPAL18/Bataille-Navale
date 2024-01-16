# https://www.pythonguis.com/tutorials/qml-qtquick-python-application/
from functions import *

"""from random import choices

default_color = Fore.LIGHTWHITE_EX + Back.BLACK

brd = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
brd_coord = [["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1"],
             ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2", "J2"],
             ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3", "J3"],
             ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4", "J4"],
             ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5", "J5"],
             ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", "I6", "J6"],
             ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", "I7", "J7"],
             ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8", "J8"],
             ["A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9", "I9", "J9"],
             ["A10", "B10", "C10", "D10", "E10", "F10", "G10", "H10", "I10", "J10"]]
empty_value = 0
first_tier = 40
second_tier = 80
full_tier = 100


def give_ones(brd_):
    ones_ = []
    for i, row in enumerate(brd_, 0):
        for j, cell in enumerate(row, 0):
            if cell == 1:
                ones_.append((i, j))

    return ones_


def compute_odds1(ones_):
    odds_ = [[empty_value for _ in range(10)] for _ in range(10)]

    for x, y in ones_:
        for i, row in enumerate(odds_, 0):
            for j in range(len(row)):
                if odds_[i][j] == empty_value:
                    if i == x and j == y:
                        odds_[i][j] = full_tier

    return odds_


def compute_odds2(ones_):
    odds_ = [[empty_value for _ in range(10)] for _ in range(10)]

    for x, y in ones_:
        for i, row in enumerate(odds_, 0):
            for j in range(len(row)):
                if odds_[i][j] == empty_value:
                    if x - 2 <= i <= x + 2 and y - 2 <= j <= y + 2:
                        odds_[i][j] = first_tier

                if odds_[i][j] == first_tier:
                    if x - 1 <= i <= x + 1 and y - 1 <= j <= y + 1:
                        odds_[i][j] = second_tier

                if odds_[i][j] == second_tier:
                    if i == x and j == y:
                        odds_[i][j] = full_tier

    return odds_


def compute_odds3(ones_):
    odds_ = [[empty_value for _ in range(10)] for _ in range(10)]

    for x, y in ones_:
        for i, row in enumerate(odds_, 0):
            for j in range(len(row)):
                if odds_[i][j] == empty_value:
                    if x - 1 <= i <= x + 1 and y - 1 <= j <= y + 1:
                        odds_[i][j] = second_tier

                if odds_[i][j] == second_tier:
                    if i == x and j == y:
                        odds_[i][j] = full_tier

    return odds_


def display(odds_):
    for row in odds_:
        print("|", end="")
        for cell in row:
            if cell == empty_value:
                print(f"     ", end="")
            elif cell == first_tier:
                colour(Fore.LIGHTYELLOW_EX)
                print(f"  ◯  ", end="")
            elif cell == second_tier:
                colour(Fore.LIGHTMAGENTA_EX)
                print(f"  ◯  ", end="")
            elif cell == full_tier:
                colour(Fore.LIGHTRED_EX)
                print(f"  ●  ", end="")
            colour(default_color)
            print(f"|", end="")
        print()


def flatten_extend(matrix):
    flat_list = []
    for row_ in matrix:
        flat_list.extend(row_)
    return flat_list


colour(default_color)
ones = give_ones(brd)
odds = compute_odds3(ones)
display(odds)

dico = {}
for _ in range(100):
    c = choices(flatten_extend(brd_coord), flatten_extend(odds), k=1)[0]
    # c = choices(flatten_extend(brd_coord))[0]
    if c not in dico:
        dico[c] = 1
    else:
        dico[c] += 1

print()

for row_, coord in zip(odds, brd_coord):
    print("|", end="")
    for cell_, case in zip(row_, coord):
        if case in dico:
            if cell_ == empty_value:
                colour(Fore.WHITE)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell_ == first_tier:
                colour(Fore.LIGHTYELLOW_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell_ == second_tier:
                colour(Fore.LIGHTMAGENTA_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell_ == full_tier:
                colour(Fore.LIGHTRED_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
        else:
            if cell_ == empty_value:
                colour(Fore.WHITE)
                print(f"  0  ", end="")
            elif cell_ == first_tier:
                colour(Fore.LIGHTYELLOW_EX)
                print(f"  0  ", end="")
            elif cell_ == second_tier:
                colour(Fore.LIGHTMAGENTA_EX)
                print(f"  0  ", end="")
            elif cell_ == full_tier:
                colour(Fore.LIGHTRED_EX)
                print(f"  0  ", end="")
        colour(default_color)
        print(f"|", end="")
    print()

"""

"""
def accuracy(brd) -> tuple[float, int]:
    Calculates the accuracy of the player and the computer.
    :param brd:
    :return:

    # En fin de compte, accuracy retourne la précision (entre 0 et 1, car c'est un pourcentage).
    # C'est dans le fichier les fonctions de mode de jeu qu'on affichera lequel des deux a été le meilleur.
    water_shots = 0
    nice_shots = 0
    
    for row in range(len(brd)):
        print(brd[row])
        for cell in brd[row]:
            if cell == 1:
                water_shots += 1
            elif cell > 1:
                nice_shots += 1

    total_shots = water_shots + nice_shots
    result = nice_shots / total_shots
    return round(result, 2), total_shots, water_shots, nice_shots
"""
"""
use -> https://docs.python.org/3/library/configparser.html
from https://en.wikipedia.org/wiki/Box-drawing_character

bold = True/False
minimal = True/False

minimal = True and bold = False:
1 │
2 │
minimal = False and bold = False
1 │
──┼──
2 │
minimal = True and bold = True:
1 ┃
2 ┃
minimal = False and bold = True
1 ┃
━━╋━━
2 ┃

In config add colors:
[COLORS]
intact = blue
hit = yellow
...

Make an interpreter after !

Separate functions into several files (logically)
"""
"""
bold = False


if bold:
    vertical_line = "┃"
    vertical_border_left = "┣"
    vertical_border_right = "┫"
    horizontal_line = "━"
    horizontal_border_up = "┳"
    horizontal_border_down = "┻"
    intersection_line = "╋"
    right_up_corner = "┓"
    right_down_corner = "┛"
    left_up_corner = "┏"
    left_down_corner = "┗"
else:
    vertical_line = "│"
    vertical_border_left = "├"
    vertical_border_right = "┤"
    horizontal_line = "─"
    horizontal_border_up = "┬"
    horizontal_border_down = "┴"
    intersection_line = "┼"
    right_up_corner = "┐"
    right_down_corner = "┘"
    left_up_corner = "┌"
    left_down_corner = "└"

"""

brd_player = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
              [0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
              [1, 1, 1, 0, 0, 0, 0, 0, 0, 1]]
brd_pc_view = [[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [3, 0, 1, 0, 0, 0, 0, 0, 0, 0],
               [3, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 1, 0, 0, 3],
               [0, 0, 0, 0, 0, 1, 3, 3, 0, 3],
               [1, 0, 0, 3, 3, 3, 1, 0, 0, 3],
               [3, 3, 3, 0, 0, 0, 0, 0, 1, 3]]
boats_player_dict = {
    'porte-avion': {(0, 0): False, (1, 0): False, (2, 0): False, (3, 0): False, (4, 0): False},
    'croiseur': {(6, 9): False, (7, 9): False, (8, 9): False, (9, 9): False},
    'contre-torpilleur': {(8, 3): False, (8, 4): False, (8, 5): False},
    'sous-marin': {(9, 0): False, (9, 1): False, (9, 2): False},
    'torpilleur': {(7, 6): False, (7, 7): False}
}

print('result:', delete_boat(brd_player, boats_player_dict,"porte-avion"))