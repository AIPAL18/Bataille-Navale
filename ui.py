from os import system
from colorama import Fore, Back
from time import sleep

clear_cmd = "clear"
default_color = Fore.LIGHTGREEN_EX + Back.BLACK
red_color = Fore.LIGHTRED_EX
water_color = Fore.LIGHTBLUE_EX
intact = Fore.GREEN
pause_color = Fore.LIGHTBLACK_EX
yellow_color = Fore.YELLOW


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


def wait_for_user() -> None:
    """
    Pause the game.
    """
    colour(pause_color)
    user_input('(pressez Entrer)')  # waits until the user press Enter & prays that he doesn't raise an error 🤞.
    colour(default_color)


def init() -> bool:
    """
    Initialise the game. Launches the welcome screen with credits, displays game recommendations and colours the screen.
    :return: True.
    """
    clear()
    system("TITLE Bataille Navale")
    colour(default_color)
    print("""
    \t##########################################################
    \t#                    BATAILLE NAVALE                     #
    \t#                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                     #
    \t#                                                        #
    \t#           Par Elie Ruggiero et Enzo Chauvet            #
    \t#                                                        #
    \t#              Décembre 2023 - Janvier 2024              #
    \t##########################################################
    """, end="\n\n")
    print("Nous vous conseillons, pour avoir une meilleur expérience, de démarrer ce programme "
          "dans un invite de commande.\n")
    print("Pour arrêter le jeu, pressez CTRL+C.\n\n")
    
    wait_for_user()
    
    return True


def display_brd(brd: list[list[bool | None | int]], is_view: bool = True, legend: bool = True) -> None:
    """
    Displays a game board in the console.
    :param brd: Game board view or game board.
    :param is_view: True if it is game board view.
    :param legend: Displays the legend if the value is True.
    """
    digits = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10"]

    print("\n\t|    | A | B | C | D | E | F | G | H | I | J |")  # Column headers

    for row in range(len(brd)):
        print(f"\t| {digits[row]} |", end="")  # Line headers

        for cell in brd[row]:
            if is_view:
                if cell:
                    colour(red_color)
                    print(" ●", end="")
                elif cell is False:
                    colour(water_color)
                    print(" ⌗", end="")
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
                    print(" ⌗", end="")
                elif cell == 3:
                    colour(red_color)
                    print(" ●", end="")
            colour(default_color)
            print(" |", end="")

        if legend and is_view:
            if row == 3:
                print(f"\t\t{red_color}●{default_color}: touché", end="")
            if row == 5:
                print(f"\t\t{water_color}⌗{default_color}: dans l'eau.", end="")
        elif legend:
            if row == 3:
                print(f"\t\t{red_color}●{default_color}: touché", end="")
            elif row == 4:
                print(f"\t\t{water_color}⌗{default_color}: dans l'eau.", end="")
            elif row == 5:
                print(f"\t\t{intact}◯{default_color}: intacte.", end="")

        print()  # return to line
    print()  # return to line


def rules(mode) -> None:
    """
    Displays the rules of the game.
    """
    if mode == 0:  # normal
        print("Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.",
              "Le premier à couler toute la flotte adverse gagne.",
              "Il n'y a pas de restriction de temps ni de coups"
              "Bonne chance !", sep="\n", end="\n")
    elif mode == 1:  # time trial
        print("Vous avez vous tirerez sur le plateau ennemi en essayant de toucher ses navires.",
              "Le premier à couler toute la flotte adverse gagne.",
              "Bonne chance !", sep="\n", end="\n")
    elif mode == 2:  # accurate
        print("Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.",
              "Le premier à couler toute la flotte adverse gagne.",
              "Bonne chance !", sep="\n", end="\n")
    elif mode == 3:  # limited
        print("Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.",
              "Le premier à couler toute la flotte adverse gagne.",
              "Bonne chance !", sep="\n", end="\n")


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
    error_raised = answered = will_quit = False
    entry = ""
    
    for arg in args:
        print(arg, end="")
    
    try:
        entry = input()
    except KeyboardInterrupt:
        error_raised = True
    except EOFError:
        error_raised = True
    
    if error_raised:  # it may be an error
        while not answered:
            colour(yellow_color)
            # for security reasons (mainly development errors), KeyboardInterrupt and EOFError are not processed.
            validation = input("\nVoulez-vous vraiment quitté le jeu ? (Y/n): ")
            colour(Fore.RESET, Back.RESET)  # resets the colours of the command prompt.
            validation = validation.upper()
            
            # N first because if the user wrote y and n by accident, we don't want to stop the game.
            if 'N' in validation:
                print("Bonne reprise !")
                colour(default_color)
                answered = True
            elif 'Y' in validation:
                will_quit = True
                answered = True
            else:
                print("Nous n'avons pas comprit...")
        
        if will_quit:
            print("Au revoir !")
            quit()  # quits the program properly

    return entry



