from os import system, name as os_name
from colorama import Fore, Back

clear_cmd = "cls"
default_color = Fore.LIGHTGREEN_EX + Back.BLACK
red_color = Fore.RED
water_color = Fore.LIGHTBLUE_EX
intact = Fore.GREEN
pause_color = Fore.LIGHTBLACK_EX
infos_color = Fore.YELLOW

if os_name == 'posix' or os_name == 'Linux':  # sys.platform ?
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
    colour(red_color)
    for i, arg in enumerate(args, 0):
        if type(arg) is str and arg[-1] == "\n":
            i = 0
            while arg[-1] == "\n":
                arg = arg[:-1]
                i += 1
            
        else:
            print(arg, end="")
            if i < len(args) - 1:
                print(sep, end="")
    print(end, end="")
    colour(default_color)


def clear() -> None:
    """
    Clear the console.
    """
    system("cls")  # asks the command prompt to execute the command


def pause() -> None:
    """
    Pause the game.
    """
    colour(pause_color)
    user_input('(pressez Entrer)')  # wait until the user press Enter & pray that he doesn't press CTRL+Z + Enter (EOFError).
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


def clean() -> None:
    """
    Resets the colours of the command prompt.
    """
    colour(Fore.RESET, Back.RESET)


def user_input(*args) -> str:
    """
    Catch CTRL+C and CTRL+Z+Enter, which end the program,
    Args:
        *args:

    Returns:

    """
    for arg in args:
        print(arg, end="")
    try:
        entry = input()
    except KeyboardInterrupt:
        colour(Fore.RESET, Back.RESET)
        quit()
    except EOFError:
        colour(Fore.RESET, Back.RESET)
        quit()

    return entry



