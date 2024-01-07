from ui import *
from random import randint
import re


def build_brd(size: int)\
        -> tuple[list[list[int]], list[list[int]], list[list[bool | None]]]:
    """
    Construit les plateaux de jeu et retourne dans l'ordre: brd_pc, brd_player, brd_player_view.
    :param size: int.
    :return: tuple[list[list[int]], list[list[int]], list[list[bool | None]]].
    """
    brd1 = [[0 for _ in range(size)] for _ in range(size)]
    brd2 = [[0 for _ in range(size)] for _ in range(size)]
    brd3 = [[None for _ in range(size)] for _ in range(size)]
    return brd1, brd2, brd3


def boat_placement_player(brd_player: list[list[int]]) -> list[list[int]]:
    """
    Fait placer les bateaux à l'utilisateur et brd_player.
    :param brd_player: list[list[int]].
    :return: list[list[int]].
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

    print("\nCommencez par placer vos bateaux:\n\n", end="")

    print("Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées d'un espace.\n"
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
                    a = int(limits[0][1:])  # borne a
                    b = int(limits[1][1:])  # borne b
                    a, b = (b, a) if a > b else (a, b)  # coordonnées interchangeables
                    a -= 1  # réajustement à cause de la boucle for
                    size = abs(a - b)
                    if size == boats_size[boat]:
                        allowed = True
                        for row in range(a, b):
                            if not brd_player[row][letters_place[limits[0][0]]] == 0:
                                allowed = False
                        if allowed:
                            for row in range(a, b):
                                brd_player[row][letters_place[limits[0][0]]] = 1
                            clear()
                            print("\nCommencez par placer vos bateaux:\n\n"
                                  "Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées "
                                  "d'un espace.\nPar exemple: Porte-avion (5 cases) -> A1 A5.\n"
                                  "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")
                            display_brd(brd_player, False, False)
                            i += 1
                        else:
                            color(Fore.LIGHTRED_EX)
                            print(f"Le {boat} est placé à cheval sur un autre bateau!")
                            color(default_color)
                    else:
                        color(Fore.LIGHTRED_EX)
                        print("La taille du bateau ne correspond pas !\n\t"
                              f"taille attendu: {boats_size[boat]}\n\t"
                              f"taille obtenue: {size}")
                        color(default_color)
                elif limits[0][1:] == limits[1][1:]:  # horizontal
                    a = letters_place[limits[0][0]]  # borne a
                    b = letters_place[limits[1][0]]  # borne b
                    a, b = (b, a) if a > b else (a, b)  # coordonnées interchangeables
                    b += 1  # réajustement à cause de la boucle for
                    size = abs(a - b)
                    if size == boats_size[boat]:
                        allowed = True
                        for cell in range(a, b):
                            if not brd_player[int(limits[0][1:]) - 1][cell] == 0:
                                allowed = False
                        if allowed:
                            for cell in range(a, b):
                                brd_player[int(limits[0][1:]) - 1][cell] = 1
                            clear()
                            print("\nCommencez par placer vos bateaux:\n\n"
                                  "Pour chaque bateau, inscrivez la première coordonnée puis la dernière séparées "
                                  "d'un espace.\nPar exemple: Porte-avion (5 cases) -> A1 A5.\n"
                                  "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")
                            display_brd(brd_player, False, False)
                            i += 1
                        else:
                            color(Fore.LIGHTRED_EX)
                            print(f"Le {boat} est placé à cheval sur un autre bateau!")
                            color(default_color)
                    else:
                        color(Fore.LIGHTRED_EX)
                        print("La taille du bateau ne correspond pas !\n\t"
                              f"taille attendu: {boats_size[boat]}\n\t"
                              f"taille obtenue: {size}")
                        color(default_color)
                else:
                    color(Fore.LIGHTRED_EX)
                    print("Le bateau doit être placé verticalement ou horizontalement exclusivement!")
                    color(default_color)
            else:
                color(Fore.LIGHTRED_EX)
                print("Le bateau doit être placé sur le plateau!")
                color(default_color)
        else:
            color(Fore.LIGHTRED_EX)
            print("Le format n'est pas bon: inscrivez la première coordonnée puis la dernière séparées d'un espace"
                  "Par exemple: Porte-avion -> A1 A5.\n"
                  f"Entrée obtenue: \'{entry}\'")
            color(default_color)
    pause()
    return brd_player


def boat_placement_pc(brd_pc: list[list[int]]) -> list[list[int]]:
    """
    Place les bateaux de l'ordinateur et retourne brd_pc.
    :param brd_pc: list[list[int]].
    :return: list[list[int]].
    """
    boats_list = [5, 4, 3, 3, 2]
    i = 0

    while i < len(boats_list):
        size = boats_list[i]
        orientation = randint(0, 1)
        if orientation == 0:    # vertical
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
        else:                   # horizontal
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
    Retourne True si la cible touche une case d’un bateau.
    :param brd: list[list[int]].
    :param target: tuple[int, int].
    :return: bool.
    """
    if brd[target[0]][target[1]] == 1 or brd[target[0]][target[1]] == 3:  # Touchée
        return True
    else:
        return False


def display_brd(brd: list[list[bool | None | int]], is_view: bool = True, legend: bool = True) -> None:
    """
    Affiche un plateau du joueur dans la console.
    :param brd: list[list[bool | None | int]].
    :param is_view: bool.
    :param legend: bool.
    """
    digits = {0: " 1", 1: " 2", 2: " 3", 3: " 4", 4: " 5", 5: " 6", 6: " 7", 7: " 8", 8: " 9", 9: "10"}

    print("\n\t|    | A | B | C | D | E | F | G | H | I | J |")  # Entête des colonnes

    for row in range(len(brd)):
        print(f"\t| {digits[row]} |", end="")  # Entête des lignes •✕º⌀●◯■

        for cell in brd[row]:
            if is_view:
                if cell:
                    color(hit_color)
                    print(" ●", end="")
                elif cell is False:
                    color(water_color)
                    print(" ✕", end="")
                elif cell is None:
                    print("  ", end="")
            else:
                if cell == 0:
                    print("  ", end="")
                elif cell == 1:
                    color(intact)
                    print(" ◯", end="")
                elif cell == 2:
                    color(water_color)
                    print(" ✕", end="")
                elif cell == 3:
                    color(hit_color)
                    print(" ●", end="")
            color(default_color)
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

        print("")  # retour à la ligne
    print("")  # retour à la ligne


def player_round(brd_pc: list[list[int]], brd_player: list[list[int]], brd_player_view: list[list[bool | None]])\
        -> tuple[list[list[int]], list[list[bool | None]]]:
    """
    Fait jouer le joueur et retourne brd_pc, brd_player_view.
    :param brd_pc: list[list[int]].
    :param brd_player: list[list[int]].
    :param brd_player_view: list[list[bool | None]].
    :return: list[list[int]].
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    entry = ""

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
        print("Touché !")
    else:
        print("Dans l'eau...")
    return brd_pc, brd_player_view


def pc_round(brd_player: list[list[int]], brd_player_view: list[list[bool | None]])\
        -> list[list[int]]:
    """
    Fait jouer l’ordinateur et retourne brd_player.
    :param brd_player: list[list[int]].
    :param brd_player_view: list[list[bool | None]].
    :return: list[list[int]].
    """
    letters_place = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
    target = (randint(0, 9), randint(0, 9))

    if is_hit(brd_player, target):
        brd_player[target[0]][target[1]] = 3
    else:
        brd_player[target[0]][target[1]] = 2

    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    print(f"\nL'adversaire tire en {letters_place[target[1]]}{target[0]+1}")
    if is_hit(brd_player, target):
        color(hit_color)
        print("Touché...")
    else:
        color(water_color)
        print("Dans l'eau!")

    color(default_color)
    return brd_player


def win(brd_player: list[list[int]], brd_pc: list[list[int]]) -> bool:
    """
    Retourne True s'il y a un vainqueur, ce qui aura pour effet d'arrêter le jeu et annonce le vainqueur.
    :param brd_player: list[list[int]].
    :param brd_pc: list[list[int]].
    :return: bool.
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

    if pc_won:          # Shame on the team
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu")
    elif player_won:    # Glory on the leader
        print("Bravo Général! Vous avez gagné !")

    return pc_won or player_won
