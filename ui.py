from os import system
from colorama import Fore, Back
from datetime import datetime

clear_cmd = "clear"
default_colour = Fore.LIGHTGREEN_EX + Back.BLACK
red_color = Fore.LIGHTRED_EX
water_color = Fore.LIGHTBLUE_EX
intact = Fore.GREEN
pause_color = Fore.LIGHTBLACK_EX
yellow_color = Fore.YELLOW


def log(*args) -> None:
    """
    Logs the error in the log file to rebuild error(s) if needed.
    :param args: Message to log.
    """
    with open(".logs", "a", encoding="utf-8") as file:  # creates the file if it doesn't exist.
        arg_str = "".join([a.replace("\n", "\\n") for a in args])
        file.write(datetime.now().strftime("%d/%m/%y %H:%M:%S | ") + arg_str + "\n")
        file.close()


def colour(*args) -> None:
    """
    Colours the command prompt.
    :param args: Colours.
    """
    for i in args:
        print(i, end="")


def error(*args, sep: str = ' ', end: str = '\n') -> None:
    """
    Displays errors in the console.
    :param sep: String inserted between values, default a space.
    :param end: String appended after the last value, default a newline.
    """
    log("Error: ", sep.join(args))
    
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
    colour(default_colour)


def clear(will_break_line=True) -> None:
    """
    Clear the console.
    :param will_break_line: If True, it'll break the line after clearing the command prompt.
    """
    system("cls")  # asks the command prompt to execute the command
    if will_break_line:
        print("")  # break line (for the style)


def user_input(*args, clr: str = default_colour) -> str:
    """
    Print out the message with the color specified.
    :param args: Message printed out.
    :param clr: Colour of the text printed out.
    :return: User entry.
    """
    finish = False
    entry = ""
    
    # if the user raises an error and enters "N", it asks again, while allowing the user to raise an error.
    while not finish:
        error_raised = answered = will_quit = False
        colour(clr)
        for arg in args:
            print(arg, end="")
        
        try:
            entry = input()
            finish = True
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
                validation = validation.upper().replace(' ', '')
                
                if 'N' == validation:
                    print("Bonne reprise !\n")
                    answered = True
                elif 'Y' == validation:
                    will_quit = True
                    answered = True
                else:
                    print("Nous n'avons pas comprit...")
            
            if will_quit:
                print("Au revoir !")
                log("Exiting - Via error")
                quit()  # quits the program properly

    return entry


def wait_for_user() -> None:
    """
    Pause the game and wait until the user presses Enter.
    """
    # waits until the user press Enter & prays that he doesn't raise an error 🤞.
    log("wait")
    user_input('\n(pressez Entrer)', clr=pause_color)
    colour(default_colour)


def display_brd_id(boats_player: dict[str: dict[tuple[int, int]: bool]]) -> None:
    """
    Display a game board in the console, making it easy to identify the boats when you place them.
    :param boats_player: Dictionary of players' boats.
    """
    digits = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10"]
    chars = [  # different characters for colour-blind people.
        Fore.LIGHTMAGENTA_EX + '1' + default_colour,
        Fore.LIGHTYELLOW_EX + '2' + default_colour,
        Fore.LIGHTCYAN_EX + '3' + default_colour,
        Fore.LIGHTRED_EX + '4' + default_colour,
        Fore.LIGHTBLUE_EX + '5' + default_colour
    ]
    boats_names = list(boats_player.keys())
    brd_player = [["" for _ in range(10)] for _ in range(10)]
    
    for boat, char in zip(boats_player.values(), chars):  # boats_player.values() returns boat's dict
        for coord in boat.keys():  # boat.keys() returns a coord
            brd_player[coord[0]][coord[1]] = char

    print("\n\t│    │ A │ B │ C │ D │ E │ F │ G │ H │ I │ J │")  # Column headers
    
    for row in range(len(brd_player)):
        print(f"\t│ {digits[row]} │", end="")  # Line headers
        
        for cell in brd_player[row]:
            if cell:
                print(f" {cell} │", end="")
            else:
                print(f"   │", end="")
            
        if row % 2 == 0:  # one row out of two
            print(f"\t\t{chars[row//2]}: {boats_names[row//2]}", end="")  # row//2 → 0, 1, 2, 3, 4.
            
        print()  # return to line
    print()  # return to line


def display_brd(brd: list[list[int]], is_view: bool = True) -> None:
    """
    Displays a game board in the console.
    :param brd: Game board view or game board.
    :param is_view: True if it is game board view.
    """
    digits = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10"]

    print("\n\t│    │ A │ B │ C │ D │ E │ F │ G │ H │ I │ J │")  # Column headers

    for row in range(len(brd)):
        print(f"\t│ {digits[row]} │", end="")  # Line headers

        for cell in brd[row]:
            if is_view:
                if cell == 0:
                    print("  ", end="")
                elif cell == 1:
                    colour(water_color)
                    print(" ■", end="")
                elif cell == 2:
                    colour(red_color)
                    print(" ●", end="")
                elif cell == 3:
                    colour(yellow_color)
                    print(" ▲", end="")
            else:  # not is_view
                if cell == 0:
                    print("  ", end="")
                elif cell == 1:
                    colour(intact)
                    print(" ◯", end="")
                elif cell == 2:
                    colour(water_color)
                    print(" ■", end="")
                elif cell == 3:
                    colour(red_color)
                    print(" ●", end="")
                elif cell == 4:
                    colour(yellow_color)
                    print(" ▲", end="")
            colour(default_colour)
            print(" │", end="")

        if is_view:
            if row == 3:
                print(f"\t\t{yellow_color}▲{default_colour}: coulé.", end="")
            if row == 4:
                print(f"\t\t{red_color}●{default_colour}: touché", end="")
            if row == 5:
                print(f"\t\t{water_color}■{default_colour}: dans l'eau.", end="")
        else:
            if row == 3:
                print(f"\t\t{yellow_color}▲{default_colour}: coulé.", end="")
            elif row == 4:
                print(f"\t\t{red_color}●{default_colour}: touché", end="")
            elif row == 5:
                print(f"\t\t{water_color}■{default_colour}: dans l'eau.", end="")
            elif row == 6:
                print(f"\t\t{intact}◯{default_colour}: intacte.", end="")

        print()  # return to line
    print()  # return to line


def init() -> bool:
    """
    Initialise the game. Launches the welcome screen with credits, displays game recommendations and colours the screen.
    :return: True.
    """
    log("Init")
    clear(False)
    system("TITLE Bataille Navale")
    colour(default_colour)
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
    print("Pour arrêter le jeu, pressez CTRL+C.\n")
    
    wait_for_user()
    
    return True


def reset_boat_placement_player_screen(boats_player: dict[str: dict[tuple[int, int]: bool]], replacing: bool = False) \
        -> None:
    """
    Reset the command prompt for boat_placement_player().
    :param boats_player: Dictionary of players' boats.
    :param replacing: Change the message printed out.
    """
    clear()
    if replacing:
        print("Si besoin, replacez vos bateaux:\n")
    else:
        print("Commencez par placer vos bateaux:\n")
    
    print("Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement.",
          "Pour sortir, saisissez \'exit\'.", sep="\n")
    display_brd_id(boats_player)


def reset_player_turn_screen(brd_player: list[list[int]], brd_player_view: list[list[int]]):
    """
    Reset the command prompt for player_turn().
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    """
    clear()
    print("C'est votre tour, Général!")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)


def clean_to_exit() -> None:
    """
    Resets the colours of the command prompt to exit the program properly.
    """
    log("Exiting - End of the game")
    clear(False)
    colour(Fore.RESET, Back.RESET)

