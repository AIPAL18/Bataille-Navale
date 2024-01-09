from ui import *
from random import randint, choice
import re


def first_player() -> bool:
    """
    Randomly defines whether the player starts playing.
    :return: is_player_round.
    """
    is_player_round = bool(randint(0, 1))
    
    if is_player_round:
        print("\nVous jouerez en premier\n")
    else:
        print("\nVotre adversaire jouera en premier\n")
    pause()
    clear()
    
    return is_player_round


def build_brd(size: int) -> tuple[list[list[int]], list[list[int]], list[list[bool | None]]]:
    """
    Build the game boards.
    :param size: Size of the (square) game boards.
    :return: brd_pc, brd_player, brd_player_view.
    """
    brd1 = [[0 for _ in range(size)] for _ in range(size)]
    brd2 = [[0 for _ in range(size)] for _ in range(size)]
    brd3 = [[None for _ in range(size)] for _ in range(size)]
    return brd1, brd2, brd3


def boat_placement_player(brd_player: list[list[int]]) -> list[list[int]]:
    """
    Makes the user place his boats.
    :param brd_player: Player's game board.
    :return: brd_player.
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    boats_size = {
        "porte-avion": 5,
        "croiseur": 4,
        "contre-torpilleur": 3,
        "sous-marin": 3,
        "torpilleur": 2
    }
    boat_name = list(boats_size.keys())

    print("\nCommencez par placer vos bateaux:\n\n"
          "Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées d'un espace.\n"
          "Par exemple: Porte-avion (5 cases) -> A1 A5.\n"
          "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")

    display_brd(brd_player, False, False)

    i = 0
    while i < len(boat_name):
        boat = boat_name[i]
        entry = input(f"{boat} ({boats_size[boat]} cases) -> ")
        entry = entry.upper()

        # intelligent recogniser:
        if re.search(r"[A-Z][0-9]+ [A-Z][0-9]+", entry):
            entry = re.search(r"[A-Z][0-9]+ [A-Z][0-9]+", entry).group()

        if re.search(r"^[A-Z][0-9]+ [A-Z][0-9]+$", entry):  # if the format is correct
            limits = tuple(entry.split(" "))  # limits = bornes
            if (limits[0][0] in letters_place.keys() and limits[1][0] in letters_place.keys() and
                    0 < int(limits[0][1:]) < 11 and 0 < int(limits[1][1:]) < 11):
                if limits[0][0] == limits[1][0]:  # vertical
                    a = int(limits[0][1:])  # start or end of the boat
                    b = int(limits[1][1:])  # start or end of the boat
                    
                    # Allows coordinates to be interchangeable
                    start, end = (b, a) if a > b else (a, b)  # start & end of the boat
                    start -= 1  # readjustment due to the for loop
                    size = abs(start - end)  # calculates the size of the boat
                    
                    if size == boats_size[boat]:
                        allowed = True
                        for row in range(start, end):
                            if not brd_player[row][letters_place[limits[0][0]]] == 0:
                                allowed = False
                        if allowed:
                            for row in range(start, end):
                                brd_player[row][letters_place[limits[0][0]]] = 1
                            clear()
                            print("\nCommencez par placer vos bateaux:\n\n"
                                  "Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées "
                                  "d'un espace.\nPar exemple: Porte-avion (5 cases) -> A1 A5.\n"
                                  "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")
                            display_brd(brd_player, False, False)
                            i += 1
                        else:
                            error(f"Le {boat} est placé à cheval sur un autre bateau!")
                    else:
                        error("La taille du bateau ne correspond pas !\n\t"
                              f"taille attendu: {boats_size[boat]}\n\t"
                              f"taille obtenue: {size}")
                elif limits[0][1:] == limits[1][1:]:  # horizontal
                    a = letters_place[limits[0][0]]  # start or end of the boat
                    b = letters_place[limits[1][0]]  # start or end of the boat
                    
                    # Allows coordinates to be interchangeable
                    start, end = (b, a) if a > b else (a, b)  # start & end of the boat
                    end += 1  # readjustment due to the for loop
                    size = abs(start - end)  # calculates the size of the boat
                    
                    if size == boats_size[boat]:
                        allowed = True
                        for cell in range(start, end):
                            if not brd_player[int(limits[0][1:]) - 1][cell] == 0:
                                allowed = False
                        if allowed:
                            for cell in range(start, end):
                                brd_player[int(limits[0][1:]) - 1][cell] = 1
                            clear()
                            print("\nCommencez par placer vos bateaux:\n\n"
                                  "Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées "
                                  "d'un espace.\nPar exemple: Porte-avion (5 cases) -> A1 A5.\n"
                                  "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")
                            display_brd(brd_player, False, False)
                            i += 1
                        else:
                            error(f"Le {boat} est placé à cheval sur un autre bateau!")
                    else:
                        error("La taille du bateau ne correspond pas !\n\t"
                              f"taille attendu: {boats_size[boat]}\n\t"
                              f"taille obtenue: {size}")
                else:
                    error("Le bateau doit être placé verticalement ou horizontalement exclusivement!")
            else:
                error("Le bateau doit être placé sur le plateau!")
        else:
            error("Le format n'est pas bon: inscrivez la première coordonnée puis la dernière séparées d'un espace"
                  "Par exemple: Porte-avion -> A1 A5.\n"
                  f"Entrée obtenue: \'{entry}\'")
    pause()
    return brd_player


def boat_placement_pc(brd_pc: list[list[int]]) -> list[list[int]]:
    """
    Place the computer's boats.
    :param brd_pc: computer's game board.
    :return: brd_pc.
    """
    boats_list = [5, 4, 3, 3, 2]
    i = 0

    print("L'adversaire positionne ses bateaux...")
    
    while i < len(boats_list):
        size = boats_list[i]
        orientation = randint(0, 1)
        
        if orientation == 0:  # vertical
            letter = randint(0, 9)
            first_number = randint(0, 9 - size)
            allowed = True
            for number in range(first_number, first_number + size):
                if not brd_pc[letter][number] == 0:
                    allowed = False
            if allowed:
                for number in range(first_number, first_number + size):
                    brd_pc[letter][number] = 1
                i += 1
        
        else:  # horizontal
            number = randint(0, 9)
            first_letter = randint(0, 9 - size)
            allowed = True
            for letter in range(first_letter, first_letter + size):
                if not brd_pc[letter][number] == 0:
                    allowed = False
            if allowed:
                for letter in range(first_letter, first_letter + size):
                    brd_pc[letter][number] = 1
                i += 1
    return brd_pc


def is_hit(brd: list[list[int]], target: tuple[int, int]) -> bool:
    """
    Returns True if the target touches a square on a boat.
    :param brd: Game board.
    :param target: Couple of coordinates.
    :return: bool.
    """
    if brd[target[0]][target[1]] == 1 or brd[target[0]][target[1]] == 3:  # Hit
        return True
    else:  # not hit
        return False


def display_brd(brd: list[list[bool | None | int]], is_view: bool = True, legend: bool = True) -> None:
    """
    Displays a game board in the console.
    :param brd: Game board view or game board.
    :param is_view: True if it is game board view.
    :param legend: Displays the legend if the value is True.
    """
    digits = {0: " 1", 1: " 2", 2: " 3", 3: " 4", 4: " 5", 5: " 6", 6: " 7", 7: " 8", 8: " 9", 9: "10"}

    print("\n\t|    | A | B | C | D | E | F | G | H | I | J |")  # Column headers

    for row in range(len(brd)):
        print(f"\t| {digits[row]} |", end="")  # Line headers

        for cell in brd[row]:
            if is_view:
                if cell:
                    colour(hit_color)
                    print(" ●", end="")
                elif cell is False:
                    colour(water_color)
                    print(" ✕", end="")
                elif cell is None:
                    print("  ", end="")
            else:
                if cell == 0:
                    print("  ", end="")
                elif cell == 1:
                    colour(intact)
                    print(" ◯", end="")
                elif cell == 2:
                    colour(water_color)
                    print(" ✕", end="")
                elif cell == 3:
                    colour(hit_color)
                    print(" ●", end="")
            colour(default_color)
            print(" |", end="")

        if legend and is_view:
            if row == 3:
                print(f"\t\t{hit_color}●{default_color}: touché", end="")
            if row == 5:
                print(f"\t\t{water_color}✕{default_color}: dans l'eau.", end="")
        elif legend:
            if row == 3:
                print(f"\t\t{hit_color}●{default_color}: touché", end="")
            elif row == 4:
                print(f"\t\t{water_color}✕{default_color}: dans l'eau.", end="")
            elif row == 5:
                print(f"\t\t{intact}◯{default_color}: intacte.", end="")

        print()  # return to line
    print()  # return to line


def player_round(brd_pc: list[list[int]], brd_player: list[list[int]], brd_player_view: list[list[bool | None]])\
        -> tuple[list[list[int]], list[list[bool | None]]]:
    """
    Makes the user play.
    :param brd_pc: Computer's game board.
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    :return: brd_pc, brd_player_view.
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    entry = ""

    print("C'est votre tour, Général!")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    while not (re.search(r"^[A-Z][0-9]+$", entry) and entry[0] in letters_place.keys() and
               0 < int(entry[1:]) < 11):
        print("Où voulez-vous tirez ? "
              "(Saisissez la coordonnée avec la lettre de la colonne suivit du chiffre de la ligne)")
        entry = input(">>> ")
        entry = entry.upper()

        # intelligent recogniser:
        if re.search(r"[A-Z][0-9]+", entry):
            entry = re.search(r"[A-Z][0-9]+", entry).group()

    target = (int(entry[1:])-1, letters_place[entry[0]])

    if is_hit(brd_pc, target):
        brd_pc[target[0]][target[1]] = 3
        brd_player_view[target[0]][target[1]] = True
    else:
        brd_pc[target[0]][target[1]] = 2
        brd_player_view[target[0]][target[1]] = False

    clear()
    print(f"Tire en {entry}")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    if is_hit(brd_pc, target):
        colour(infos_color)
        print("Touché !")
    else:
        colour(water_color)
        print("Dans l'eau...")
    colour(default_color)
    
    pause()
    return brd_pc, brd_player_view


def pc_round(brd_player: list[list[int]], brd_player_view: list[list[bool | None]], level: int)\
        -> list[list[int]]:
    """
    Makes the computer play.
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    :param level: int.
    :return: brd_player.
    """
    letters_place = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
    target = ()

    if level == 1:
        target = (randint(0, 9), randint(0, 9))
    elif level == 2:
        partial_brd = []
        choice(partial_brd)
    elif level == 3:
        partial_brd = []
        choice(partial_brd)

    if is_hit(brd_player, target):
        brd_player[target[0]][target[1]] = 3
    else:
        brd_player[target[0]][target[1]] = 2

    print("C'est au tour de l'adversaire.")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)
    print(f"\nL'adversaire tire en {letters_place[target[1]]}{target[0]+1}")
    
    if is_hit(brd_player, target):
        colour(hit_color)
        print("Touché...")
    else:
        colour(water_color)
        print("Dans l'eau!")
    colour(default_color)
    
    pause()
    return brd_player


def win(brd_player: list[list[int]], brd_pc: list[list[int]]) -> bool:
    """
    Returns True and announce the winner if there's a winner, which will stop the game.
    :param brd_player: Player's game board.
    :param brd_pc: Computer's game board.
    :return: True if someone won.
    """
    pc_won = True
    for row in brd_player:
        for cell in row:
            if cell == 1:
                pc_won = False

    player_won = True
    for row in brd_pc:
        for cell in row:
            if cell == 1:
                player_won = False

    if pc_won:  # Shame on the team
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu")
    elif player_won:  # Glory on the leader
        print("Bravo Général! Vous avez gagné !")

    return pc_won or player_won
