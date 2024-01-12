from ui import *
from random import randint, choice
import re
from time import sleep


def select_level() -> tuple[int, bool | None]:
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
        entry = user_input("\n(Entrez le numéro correspondant) -> ")
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


def first_player() -> bool:
    """
    Randomly defines whether the player starts playing.
    :return: is_player_round.
    """
    clear()
    is_player_round = bool(randint(0, 1))
    
    if is_player_round:
        print("Vous jouerez en premier\n")
    else:
        print("Votre adversaire jouera en premier\n")
    pause()
    
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


def reset_boat_placement_player_screen(brd_player: list[list[int]]):
    """
    Reset the command prompt for boat_placement_player().
    :param brd_player: Player's game board.
    """
    colour(default_color)
    clear()
    print("\nCommencez par placer vos bateaux:\n\n"
          "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement")
    display_brd(brd_player, False, False)


def str_to_coordinates(coordinates_str) -> tuple[tuple[int, int], tuple[int, int], int, int] | bool:
    """
    Transform a string into two set of coordinates if possible, otherwise it returns False.
    :param coordinates_str:
    :return: (start, end, orientation, size) or False.
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    # intelligent recogniser:
    if re.search(r"[A-Z][0-9]+ [A-Z][0-9]+", coordinates_str):
        coordinates_str = re.search(r"[A-Z][0-9]+ [A-Z][0-9]+", coordinates_str).group()
    
    if re.search(r"^[A-Z][0-9]+ [A-Z][0-9]+$", coordinates_str):  # if the input format is valid.
        limits = tuple(coordinates_str.split(" "))
        
        if (limits[0][0] in letters_place.keys() and limits[1][0] in letters_place.keys() and
                0 < int(limits[0][1:]) < 11 and 0 < int(limits[1][1:]) < 11):  # True if the boat is on the board.
            # we use letters_place because we checked, with the regex above, that the input format is respected.
            letter_a = letters_place[limits[0][0]]  # letter of the first set of coordinates.
            letter_b = letters_place[limits[1][0]]  # letter of the second set of coordinates.
            
            # we use int() because we checked, with the regex above, that the input format is respected.
            number_a = int(limits[0][1:])  # number in the first set of coordinates.
            number_b = int(limits[1][1:])  # number in the second set of coordinates.
            
            if letter_a == letter_b:  # letters are the same → vertical.
                # Enables the start and end of the boat to be interchanged and readjustment due to the range() function.
                """
                We will iterate in between number_b and number_a with the range() function.
                1 - reel number = index + 1
                So index = number_b - 1
                II - range(a, b-1) gives index + 1 - 1 = reel number
                So index = number_a
                
                Whereas index for letters is already calculated in the dict above.
                """
                print(letter_a)
                if number_a > number_b:
                    start = (letter_b, number_b - 1)
                    end = (letter_a, number_a)
                else:
                    start = (letter_a, number_a - 1)
                    end = (letter_b, number_b)
                
                size = end[1] - start[1]  # calculates the size of the boat
                
                return start, end, 1, size
            
            elif number_a == number_b:  # numbers are the same → horizontal.
                # Enables the start and end of the boat to be interchanged.
                """
                We will iterate in between letter_b and letter_a with the range() function.
                I - value of letter = place of letter - 1 (in the dict above)
                And place of letter = index + 1
                So index = place of letter - 1 = value of letter
                II - range(a, b-1) gives index + 1 - 1 = place of letter
                And index = place of letter
                But place of letter = value of letter + 1
                So index = value of letter + 1
                
                Whereas index for number = index + 1
                So index = number - 1
                """
                if letter_a > letter_b:
                    start = (letter_b, number_b - 1)  # reel number = index+1 so index = number_b-1
                    end = (letter_a + 1, number_a - 1)  # reel number = index+1 so index = number_a-1
                else:
                    start = (letter_a, number_a - 1)
                    end = (letter_b + 1, number_b - 1)
                
                size = end[0] - start[0]  # calculates the size of the boat
                print(start, end)
                return start, end, 0, size
            
            else:  # letters and numbers are different.
                error("Général, le bateau ne peut pas être placé en diagonale !")
                return False
        else:  # boat isn't on the game board.
            error("Le bateau doit être placé sur la mer (de A1 à J10) !")
            return False
    else:  # The input format is not respected.
        error("Le format n'est pas bon: inscrivez la première coordonnée, puis la dernière séparées d'un espace.\n"
              "Par exemple: Porte-avion (5 cases) -> A1 A5.\n"
              f"Entrée obtenue: \"{coordinates_str}\"")
        return False


def is_space_free(brd, start: tuple[int, int], end: tuple[int, int], orientation: int, boats_player: dict)\
        -> tuple[bool, list[str]]:
    """
    Returns True if the location of the new boat is free.
    Otherwise, it returns False, and the name of the boat(s) that is placed on at least one of the coordinates.
    :param brd: Game board.
    :param start: Small coordinates.
    :param end: Big coordinates.
    :param orientation: Orientation.
    :param boats_player: Dictionary storing the player's boats.
    :return: is_space_free, if False, it returns a list of boat's name already placed on these coordinates otherwise
     it returns an empty list.
    """
    allowed = True
    boat_list = []
    
    if orientation:  # 1 = True → Vertical
        for row in range(start[1], end[1]):
            if not brd[row][start[0]] == 0:
                allowed = False
    else:  # 0 = False → Horizontal
        for cell in range(start[0], end[0]):
            if not brd[start[1]][cell] == 0:
                allowed = False
    
    if not allowed:
        if orientation:
            virtual_coord = [(row, start[0]) for row in range(start[1], end[1])]
        else:
            virtual_coord = [(start[1], cell) for cell in range(start[0], end[0])]
        
        for boat, coord in zip(boats_player, list(boats_player.values())):
            for c in virtual_coord:
                if c in coord:
                    boat_list.append(boat)
    
    return allowed, boat_list
    

def place_boat(brd_player: list[list[int]], boat_name: str, boats_player: dict)\
        -> tuple[list[list[int]], dict, bool]:
    """
    Place one boat on the game board. It returns True if the boat has been placed successfully.
    :param brd_player: Player's game board.
    :param boat_name: Name of the boat.
    :param boats_player: Dictionary storing the player's boats.
    :return: brd_player, boats_player, placed.
    """
    boats_size_list = {"porte-avion": 5, "croiseur": 4, "contre-torpilleur": 3, "sous-marin": 3, "torpilleur": 2}
    placed = False
    boat_size = boats_size_list[boat_name]
    
    print(f"\nInscrivez la première coordonnée du {boat_name}, puis la dernière séparées d'un espace. "
          "Par exemple: Porte-avion (5 cases) -> A1 A5.")
    entry = user_input(f"{boat_name} ({boat_size} cases) -> ")
    entry = entry.upper()
    boat_infos = str_to_coordinates(entry)
    
    if boat_infos:  # if the input format is valid
        start, end, orientation, size = boat_infos
        if size == boat_size:
            space_free, boats_taking_space = is_space_free(brd_player, start, end, orientation, boats_player)
            if space_free:
                if orientation:  # 1 = True → Vertical
                    coord = []
                    for row in range(start[1], end[1]):
                        brd_player[row][start[0]] = 1
                        coord.append((row, start[0]))
                    
                    boats_player[boat_name] = coord  # update coordinates of the boat
                    placed = True
                else:  # 0 = False → Horizontal
                    coord = []
                    for cell in range(start[0], end[0]):
                        brd_player[start[1]][cell] = 1
                        coord.append((start[1], cell))
                    
                    boats_player[boat_name] = coord  # update coordinates of the boat
                    placed = True
            else:
                boat_names_format = f"Le {boats_taking_space}"
                for i, boat in enumerate(boats_taking_space[1:], 0):
                    if i < len(boats_taking_space) - 2:
                        boat_names_format += f", le {boat}"
                    else:
                        boat_names_format += f" et le {boat}"
                error(f"{boat_names_format} navigue{"nt" if len(boats_taking_space) > 1 else ""} déjà sur ces eaux... "
                      "L'espace est pris !")
        else:
            error("La taille du bateau ne correspond pas !\n\t"
                  f"taille attendu: {boat_size}\n\t"
                  f"taille obtenue: {size}")
    
    return brd_player, boats_player, placed


def delete_boat(brd_player: list[list[int]], boats_player, boat_name):
    """
    Replace one boat on the game board.
    :param brd_player: Player's game board.
    :param boats_player: Dictionary storing the player's boats.
    :param boat_name: Name of the boat.
    :return: brd_player, boats_player.
    """
    pass


def boat_placement_player(brd_player: list[list[int]]) -> tuple[list[list[int]], dict]:
    """
    Makes the user place his/her boats.
    :param brd_player: Player's game board.
    :return: brd_player, boats_player.
    """
    boats_size_list = {"porte-avion": 5, "croiseur": 4, "contre-torpilleur": 3, "sous-marin": 3, "torpilleur": 2}
    boats_player = {
        "porte-avion": [],
        "croiseur": [],
        "contre-torpilleur": [],
        "sous-marin": [],
        "torpilleur": []
    }
    boats_status = {  # status is False if the boat is not placed.
        "porte-avion": False,
        "croiseur": False,
        "contre-torpilleur": False,
        "sous-marin": False,
        "torpilleur": False
    }
    number_to_boat = {
        1: "porte-avion",
        2: "croiseur",
        3: "contre-torpilleur",
        4: "sous-marin",
        5: "torpilleur"
    }
    
    reset_boat_placement_player_screen(brd_player)

    while not all(boats_status.values()):  # loops until all the boats are positioned
        print("Saisissez le numéro du bateau que vous voulez placer:")
        for i, name in enumerate(boats_status, 1):
            if boats_status[name]:
                colour(red_color)
                print(f"{i} -> {name} ({boats_size_list[name]} cases)")
                colour(default_color)
            else:
                print(f"{i} -> {name} ({boats_size_list[name]} cases)")
        boat_number_entry = user_input(">>> ")
        if boat_number_entry.isnumeric():
            boat_number = int(boat_number_entry)
            if 1 <= boat_number <= 5:
                boat = number_to_boat[boat_number]
                if not boats_status[boat]:  # if the boat is not already placed
                    brd_player, boats_player, placed = place_boat(brd_player, boat, boats_player)
                    boats_status[boat] = placed  # updates the boat's status
                    if placed:
                        reset_boat_placement_player_screen(brd_player)
                        pass
                else:
                    error(f"Le {boat} est déjà placé. Quand j'aurais du temps, je vous proposerais de le replacer...")
                    # replace_entry = user_input("Souhaitez-vous replacer le bateau ? (Y/N)")
                    
            else:
                error(f"Le numéro {boat_number} ne correspond pas à un bateau !")
        else:
            error("Vous devez saisir un numéro !")
    
    # Ask the user if he/she want to replace a boat (While)
    """keep_modifying = True
    while keep_modifying:
        replace_entry = user_input()
        # si vide
        # si Y/N
        # delete
        # place
    """
    
    pause()
    return brd_player, boats_player


def boat_placement_pc(brd_pc: list[list[int]]) -> tuple[list[list[int]], dict]:
    """
    Place the computer's boats.
    :param brd_pc: computer's game board.
    :return: brd_pc, boats_pc.
    """
    clear()
    boats_list = [5, 4, 3, 3, 2]
    boats_pc = {
        "porte-avion": [],
        "croiseur": [],
        "contre-torpilleur": [],
        "sous-marin": [],
        "torpilleur": []
    }
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

    sleep(3)  # simulation of the pc placing its boats
    clear()

    return brd_pc, boats_pc


def is_hit(brd: list[list[int]], target: tuple[int, int]) -> bool:
    """
    Returns True if the target touches a square on a boat.
    :param brd: Game board.
    :param target: Couple of coordinates.
    :return: If the target touches a square on a boat.
    """
    return brd[target[0]][target[1]] == 1 or brd[target[0]][target[1]] == 3


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
                    colour(red_color)
                    print(" ●", end="")
            colour(default_color)
            print(" |", end="")

        if legend and is_view:
            if row == 3:
                print(f"\t\t{red_color}●{default_color}: touché", end="")
            if row == 5:
                print(f"\t\t{water_color}✕{default_color}: dans l'eau.", end="")
        elif legend:
            if row == 3:
                print(f"\t\t{red_color}●{default_color}: touché", end="")
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
    clear()
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    entry = ""

    print("C'est votre tour, Général!")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    while not (re.search(r"^[A-Z][0-9]+$", entry) and entry[0] in letters_place.keys() and
               0 < int(entry[1:]) < 11):
        print("Où voulez-vous tirez ? "
              "(Saisissez la coordonnée avec la lettre de la colonne suivit du chiffre de la ligne)")
        entry = user_input(">>> ")
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
    clear()
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
        colour(red_color)
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
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu...")
    elif player_won:  # Glory on the leader
        print("Bravo Général! Vous avez gagné !")

    return pc_won or player_won


def accuracy(brd_player, brd_pc) -> None:
    """
    Calculates the accuracy of the player and the computer. Tells the user which one was more precise.
    Args:
        brd_player:
        brd_pc:
    """
    pass

