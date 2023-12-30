from functions import *

print(Fore.GREEN + Back.BLACK)

brd = [[False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, False, False, False, False, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [None, False, False, None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None, None, None, None],
       [None, None, None, None, None, False, None, None, None, None],
       [None, None, None, None, None, False, None, False, False, False],
       [None, None, None, None, None, False, None, None, None, None]]

brd_view = [[None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None]]

boats_dict = {
    "pa": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],   # porte-avion
    "c": [(4, 3), (5, 3), (6, 3), (7, 3)],            # croiseur
    "ct": [(5, 7), (5, 8), (5, 9)],                   # contre-torpilleur
    "sm": [(7, 8), (8, 8), (9, 8)],                   # sous-marin
    "t": [(1, 5), (2, 5)],                            # torpilleur
}

target = (1, 1)

brd, brd_view = pc_round(brd, brd_view)
display_brd(brd, False)
display_brd(brd_view, True)
print("\b")
