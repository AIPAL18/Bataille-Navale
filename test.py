# https://www.pythonguis.com/tutorials/qml-qtquick-python-application/
from functions import *
from random import choices

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
    for row in matrix:
        flat_list.extend(row)
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

for row, coord in zip(odds, brd_coord):
    print("|", end="")
    for cell, case in zip(row, coord):
        if case in dico:
            if cell == empty_value:
                colour(Fore.WHITE)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell == first_tier:
                colour(Fore.LIGHTYELLOW_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell == second_tier:
                colour(Fore.LIGHTMAGENTA_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
            elif cell == full_tier:
                colour(Fore.LIGHTRED_EX)
                print(f"  {dico[case]}{" " if dico[case] < 10 else ""} ", end="")
        else:
            if cell == empty_value:
                colour(Fore.WHITE)
                print(f"  0  ", end="")
            elif cell == first_tier:
                colour(Fore.LIGHTYELLOW_EX)
                print(f"  0  ", end="")
            elif cell == second_tier:
                colour(Fore.LIGHTMAGENTA_EX)
                print(f"  0  ", end="")
            elif cell == full_tier:
                colour(Fore.LIGHTRED_EX)
                print(f"  0  ", end="")
        colour(default_color)
        print(f"|", end="")
    print()
