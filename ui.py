from os import system, name as os_name
from colorama import Fore, Back

clear_cmd = "cls"
default_color = Fore.LIGHTGREEN_EX + Back.BLACK
hit_color = Fore.RED
water_color = Fore.LIGHTBLUE_EX
intact = Fore.GREEN
pause_color = Fore.LIGHTBLACK_EX
infos_color = Fore.YELLOW

if os_name == 'posix' or os_name == 'Linux':
    clear_cmd = "clear"
    default_color = Fore.GREEN + Back.BLACK
    water_color = Fore.BLUE
    intact = Fore.LIGHTGREEN_EX
    infos_color = Fore.LIGHTYELLOW_EX


def colour(*args) -> None:
    """
    Colours the command prompt.
    """
    for i in args:
        print(i, end="")


def error(*args, sep=' ', end='\n') -> None:
    """
    Displays errors in the console.
    :param sep: String inserted between values, default a space.
    :param end: String appended after the last value, default a newline.
    """
    colour(hit_color)
    for i, arg in enumerate(args, 0):
        print(arg, end="")
        if i < len(args):
            print(sep, end="")
    print(end, end="")
    colour(default_color)


def clear() -> None:
    """
    Clear the console.
    """
    system(clear_cmd)


def pause() -> None:
    """
    Pause the game.
    """
    colour(pause_color)
    input('(pressez Entrer)')
    colour(default_color)


def init() -> bool:
    """
    Initialise the game. Launches the welcome screen with credits, displays game recommendations and colours the screen.
    :return: True.
    """
    clear()
    colour(default_color)
    print("""\n
    \t##########################################################
    \t#                    BATAILLE NAVAL                      #
    \t#                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾                      #
    \t#                                                        #
    \t#           Par Elie Ruggiero et Enzo Chauvet            #
    \t#                                                        #
    \t#              Décembre 2023 - Janvier 2024              #
    \t##########################################################\n\n""")
    colour(infos_color)
    print("Nous vous conseillons, pour avoir une meilleur expérience, de démarrer ce programme "
          "dans un invite de commande.\n\n")
    pause()
    
    return True


def rules() -> None:
    """
    Displays the rules of the game.
    """
    clear()
    print("\nDéroulement du jeu:\n"
          "Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.\n"
          "Le premier à couler toute la flotte adverse gagne.\n"
          "Bonne chance !\n")

    pause()


def select_level() -> int:
    """
    Returns the level of difficulty chosen by the user.
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


def clean() -> None:
    """
    Resets the colours of the command prompt.
    """
    colour(Fore.RESET, Back.RESET)
