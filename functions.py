from colorama import Fore, Back, Style
from random import randint
f_color = Fore.LIGHTGREEN_EX


def color(clr: str) -> None:
    """
    Colore le cmd.
    :param clr: str.
    :return: None.
    """
    print(clr, end="")


def is_hit(brd: list[list[bool | None]], target: tuple[int, int]) -> bool:
    """
    Retourne True si la cible touche une case non détruite d’un bateau.
    :param brd: list[list[bool | None]].
    :param target: tuple[int, int].
    :return: bool.
    """
    if brd[target[0]][target[1]] or brd[target[0]][target[1]] is False:  # Touchée
        return True
    else:
        return False


def display_brd(brd_view: list[list[bool | None]], is_view: bool = True) -> None:
    """
    Affiche le plateau du joueur dans la console.
    :param is_view: bool.
    :param brd_view: list[list[bool | None]].
    :return: None.
    """
    true_color = Fore.RED
    false_color = Fore.LIGHTBLUE_EX if is_view else Fore.GREEN
    digits = {0: " 1",
              1: " 2",
              2: " 3",
              3: " 4",
              4: " 5",
              5: " 6",
              6: " 7",
              7: " 8",
              8: " 9",
              9: "10"}

    color(f_color)
    print("\t|    | A | B | C | D | E | F | G | H | I | J |")
    for row in range(len(brd_view)):
        print(f"\t| {digits[row]} |", end="")
        for box in brd_view[row]:
            if box:
                color(true_color)
                print(" o", end="")
            elif box is False:
                color(false_color)
                print(" x", end="")
            elif box is None:
                print("  ", end="")

            color(f_color)
            print(" |", end="")

        if row == 3:
            print(f"\t\t{true_color}o{f_color}: touché", end="")
        if row == 5 and is_view:
            print(f"\t\t{false_color}x{f_color}: dans l'eau.", end="")
        elif row == 5:
            print(f"\t\t{false_color}x{f_color}: intacte.", end="")
        # retour à la ligne
        print("")
    print("")


def pc_round(brd: list[list[bool | None]], brd_view: list[list[bool | None]])\
        -> tuple[list[list[bool | None]], list[list[bool | None]]]:
    """
    Fait jouer l’ordinateur.
    :param brd: list[list[bool]].
    :param brd_view: list[list[bool | None]].
    :return: tuple[list[list[bool | None]], list[list[bool | None]]].
    """
    target = (randint(0, 9), randint(0, 9))
    if is_hit(brd, target):
        brd[target[0]][target[1]] = True
        brd_view[target[0]][target[1]] = True
    else:
        brd_view[target[0]][target[1]] = False

    return brd, brd_view


def win(brd: list[list[bool | None]], is_player_round: bool) -> bool:  # running = win(...)
    """
    Arrête le jeu si le plateau (joueur ou pc) ne contient plus de bateau et annonce le vainqueur.
    :param brd: list[list[bool]].
    :param running: bool.
    :param is_player_round: bool.
    :return: bool.
    """
    pass
