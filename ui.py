import os
from os import system, name
from colorama import Fore, Back

clear_cmd = "cls"
default_color = Fore.LIGHTGREEN_EX + Back.BLACK
hit_color = Fore.RED
water_color = Fore.LIGHTBLUE_EX
intact = Fore.GREEN
pause_color = Fore.LIGHTBLACK_EX
infos_color = Fore.YELLOW

if os.name == 'posix' or os.name == 'Linux':
    clear_cmd = "clear"
    default_color = Fore.GREEN + Back.BLACK
    water_color = Fore.BLUE
    intact = Fore.LIGHTGREEN_EX
    infos_color = Fore.LIGHTYELLOW_EX


def color(*args) -> None:
    """
    Colore l'invite de commande.
    """
    for i in args:
        print(i, end="")


def error(*args, sep=' ', end='\n') -> None:
    """
    Affiche une erreur en console.
    :param args: /
    :param sep: str.
    :param end: str.
    """
    color(hit_color)
    for i, arg in enumerate(args, 0):
        print(arg, end="")
        if i < len(args):
            print(sep, end="")
    print(end, end="")
    color(default_color)


def clear() -> None:
    """
    Efface la console.
    """
    system(clear_cmd)


def pause() -> None:
    """
    Pause le jeu.
    """
    color(pause_color)
    input('(pressez Entrer)')
    color(default_color)


def start() -> None:
    """
    Initialise le jeu : lance l'écran d'accueil avec les crédits, affiche les recommandations de jeu et colore l'écran.
    """
    clear()
    print("""\n
    \t##########################################################
    \t#                    BATAILLE NAVAL                      #
    \t#                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾                      #
    \t#                                                        #
    \t#           Par Elie Ruggiero et Enzo Chauvet            #
    \t#                                                        #
    \t#              Décembre 2023 - Janvier 2024              #
    \t##########################################################\n\n""")
    color(infos_color)
    print("Nous vous conseillons, pour avoir une meilleur expérience, de démarrer ce programme "
          "dans un invite de commande.\n\n")
    pause()


def rules() -> None:
    """
    Affiche les règles du jeu.
    """
    clear()
    print("\nDéroulement du jeu:\n"
          "Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.\n"
          "Le premier à couler toute la flotte adverse gagne.\n"
          "Bonne chance !\n")

    pause()


def select_level() -> int:
    """
    Retourne le niveau de difficulté choisit par l'utilisateur.
    :return: int.
    """
    clear()
    level = 0
    not_allowed = True

    print("Choisissez le niveau de difficulté du jeu:\n"
          "\t1 - Facile\n"
          "\t2 - Moyen\n"
          "\t3 - Difficile")

    while not_allowed:
        entry = input("\n(Entrez le numéro correspondant) -> ")
        if not entry:  # empty
            error("Vous devez entrer une valeur !")
        else:
            if not entry.isnumeric():  # is int
                error("La valeur entrée doit être un nombre !")
            else:
                level = int(entry)
                if level < 1 or level > 3:
                    error("La valeur entrée doit correspondre à un niveau de difficulté !")
                else:
                    not_allowed = False

    return level


def finish() -> None:
    """
    Réinitialise les couleurs de l'invite de commande.
    """
    color(Fore.RESET, Back.RESET)
