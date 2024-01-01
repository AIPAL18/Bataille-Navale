########################################################################################################################
#                                                                                                                      #
#                                                    BATAILLE NAVAL                                                    #
#                                                                                                                      #
#                                          Par Elie Ruggiero et Enzo Chauvet                                           #
#                                                                                                                      #
#                                             Décembre 2023 - Janvier 2024                                             #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#   This is free and unencumbered software released into the public domain.                                            #
#                                                                                                                      #
#   Anyone is free to copy, modify, publish, use, compile, sell, or                                                    #
#   distribute this software, either in source code form or as a compiled                                              #
#   binary, for any purpose, commercial or non-commercial, and by any                                                  #
#   means.                                                                                                             #
#                                                                                                                      #
#   In jurisdictions that recognize copyright laws, the author or authors                                              #
#   of this software dedicate any and all copyright interest in the                                                    #
#   software to the public domain. We make this dedication for the benefit                                             #
#   of the public at large and to the detriment of our heirs and                                                       #
#   successors. We intend this dedication to be an overt act of                                                        #
#   relinquishment in perpetuity of all present and future rights to this                                              #
#   software under copyright law.                                                                                      #
#                                                                                                                      #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                                                    #
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                                                 #
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                                             #
#   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR                                                  #
#   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,                                              #
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR                                              #
#   OTHER DEALINGS IN THE SOFTWARE.                                                                                    #
#                                                                                                                      #
#   For more information, please refer to <https://unlicense.org>                                                      #
#                                                                                                                      #
########################################################################################################################
from colorama import Fore, Back, Style
from random import randint
from os import system
from time import sleep
f_color = Fore.LIGHTGREEN_EX


def start() -> None:
    """
    Initialise le jeu : lance l'écran d'accueil avec les crédits , affiche les recommandations de jeu et color l'écran.
    :return: None.
    """
    color(f_color, Back.BLACK)
    print("""\n
    \t##########################################################
    \t#                    BATAILLE NAVAL                      #
    \t#                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾                      #
    \t#                                                        #
    \t#           Par Elie Ruggiero et Enzo Chauvet            #
    \t#                                                        #
    \t#              Décembre 2023 - Janvier 2024              #
    \t##########################################################\n\n""")
    color(Fore.RED)
    print("Nous vous conseillons, pour avoir une meilleur expérience, de démarrer ce programme "
          "dans un invite de commande.\n\n")
    sleep(5)
    clear()
    color(f_color)


def color(*args) -> None:
    """
    Colore le cmd.
    :param clr_foreground: str.
    :param clr_background: str.
    :return: None.
    """
    for i in args:
        print(i, end="")


def clear() -> None:
    """
    Efface la console.
    :return: None.
    """
    system("cls")


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
    digits = {0: " 1", 1: " 2", 2: " 3", 3: " 4", 4: " 5", 5: " 6", 6: " 7", 7: " 8", 8: " 9", 9: "10"}

    print("\t|    | A | B | C | D | E | F | G | H | I | J |")  # Entête des colonnes

    for row in range(len(brd_view)):
        print(f"\t| {digits[row]} |", end="")  # Entête des lignes

        for cell in brd_view[row]:
            if cell:
                color(true_color)
                print(" o", end="")
            elif cell is False:
                color(false_color)
                print(" x", end="")
            elif cell is None:
                print("  ", end="")
            color(f_color)
            print(" |", end="")
        if row == 3:
            print(f"\t\t{true_color}o{f_color}: touché", end="")

        if row == 5 and is_view:
            print(f"\t\t{false_color}x{f_color}: dans l'eau.", end="")
        elif row == 5:
            print(f"\t\t{false_color}x{f_color}: intacte.", end="")
        print("")  # retour à la ligne
    print("")  # retour à la ligne


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


def win(brd: list[list[bool | None]], is_player_round: bool) -> bool:  # running = not win(...)
    """
    Arrête le jeu si le plateau (du joueur ou de l’ordi) ne contient plus de bateau et annonce le vainqueur.
    :param brd: list[list[bool]].
    :param running: bool.
    :param is_player_round: bool.
    :return: bool.
    """
    won = True
    for row in brd:
        for cell in row:
            if cell is False:
                won = False

    if won and is_player_round:     # Glory on the leader
        print("Bravo Général! Vous avez gagné !")
    elif won:                       # Shame on the team
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu")

    return won
