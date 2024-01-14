from ui import *
from random import randint, choice
import re
from time import sleep


def select_mode() -> int:
    """
    Returns the level of difficulty chosen by the user.
    """
    clear()
    mode = 0
    is_cheat_code_activated = False
    allowed = False

    print("Choisissez le mode de jeu en inscrivant le numéro correspondant:",
          "\t1 - Le Nord Mâle",  # normal
          "\t2 - Le Comte Rellam-Honttre",  # contre-la-montre, 10 min pour gagner.
          "\t3 - L'habile lité",  # habilité/doigt de fée, précision, tu dois toucher 50 % du temps.
          "\t4 - Il reste un rein", sep="\n")  # restreint → nombre de coups limité
    
    while not allowed:
        entry = user_input("-> ")
        if entry:
            if entry.isnumeric():
                mode = int(entry) - 1
                if 0 <= mode <= 3:
                    allowed = True
                else:
                    error("La valeur entrée doit correspondre à un niveau de difficulté !")
            else:  # is not int
                error("La valeur entrée doit être un nombre !")
        else:  # empty
            error("Vous devez entrer une valeur !")
    
    return mode


def select_level() -> int:
    """
    Returns the level of difficulty chosen by the user.
    """
    level = 0
    allowed = False
    
    print("\n\nChoisissez le niveau de difficulté du jeu en inscrivant le numéro correspondant:",
          "\t1 - Facile",
          "\t2 - Moyen",
          "\t3 - Difficile",
          "\t4 - Impossible", sep="\n")
    
    while not allowed:
        entry = user_input("-> ")
        if entry:
            if entry.isnumeric():
                level = int(entry) - 1
                if 0 <= level <= 3:
                    allowed = True
                else:
                    error("La valeur entrée doit correspondre à un mode de jeu !")
            else:  # is not int
                error("La valeur entrée doit être un nombre !")
        else:  # empty
            error("Vous devez entrer une valeur !")

    return level


def first_player() -> bool:
    """
    Randomly defines whether the player starts playing.
    :return: is_player_round.
    """
    is_player_round = bool(randint(0, 1))
    
    if is_player_round:
        print("\n\nVous jouerez en premier\n")
    else:
        print("\n\nVotre adversaire jouera en premier\n")
    wait_for_user()
    
    return is_player_round


def build_brd() -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    """
    Build the game boards.
    :return: brd_pc, brd_player, brd_pc_view, brd_player_view.
    """
    brd_pc = [[0 for _ in range(10)] for _ in range(10)]
    brd_player = [[0 for _ in range(10)] for _ in range(10)]
    brd_pc_view = [[0 for _ in range(10)] for _ in range(10)]
    brd_player_view = [[0 for _ in range(10)] for _ in range(10)]
    
    return brd_pc, brd_player, brd_pc_view, brd_player_view


def reset_boat_placement_player_screen(boats_player: dict[str: dict[tuple[int, int]: bool]]) -> None:
    """
    Reset the command prompt for boat_placement_player().
    :param boats_player: pass
    """
    clear()
    print("Commencez par placer vos bateaux:\n",
          "Les bateaux peuvent être orienté verticalement ou horizontalement exclusivement.",
          "Pour sortir, saisissez \'exit\'.", sep="\n")
    display_brd_id(boats_player)


def str_to_coordinates(coordinates_str: str) -> tuple[int, int] | int:
    """
    Transform a string into a set of coordinates if possible, otherwise it returns the error_code.
    :param coordinates_str:  Pass.
    :return: coordinates or error_code.
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    
    # Intelligent recognition: (it will not extract a string if it already knows that it is not on the game board)
    if re.search(r"[A-J][0-9]{1,2}", coordinates_str):  #
        coordinates_str = re.search(r"[A-J][0-9]{1,2}", coordinates_str).group()
    
    if re.search(r"^[A-Z][0-9]+$", coordinates_str):  # if the input format is valid.
        """
        index = number - 1
        It is already calculated for the letters in the dictionary above.
        We calculate the index from the number above.
        """
        letter = coordinates_str[0]
        number = int(coordinates_str[1:]) - 1
        if letter in letters_place.keys() and 0 <= number <= 9:
            return number, letters_place[letter]
        else:
            return 1
    else:
        return 0
    

def determine_orientation(first_coord, second_coord) -> int | None:
    """
    
    :param first_coord:
    :param second_coord:
    :return:
    """
    if first_coord[0] == second_coord[0]:  # horizontal
        return 1
    elif first_coord[1] == second_coord[1]:  # vertical
        return 0
    else:  # neither
        return None
    

def str_to_boat_coordinates(coordinates_str: str, brd_player: list[list[int]],
                            boats_player: dict[str: dict[tuple[int, int]: bool]])\
        -> tuple[tuple[int, int], tuple[int, int], int, int] | bool:
    """
    Transform a string into two set of coordinates if possible, otherwise it returns False.
    :param coordinates_str: Pass.
    :param brd_player: Pass.
    :param boats_player: pass
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
                reset_boat_placement_player_screen(boats_player)
                error(f"Général, le bateau ne peut pas être placé en diagonale: {coordinates_str} !")
                return False
        else:  # boat isn't on the game board.
            reset_boat_placement_player_screen(boats_player)
            error(f"Le bateau doit être placé sur la mer (de A1 à J10): {coordinates_str} !")
            return False
    else:  # The input format is not respected.
        reset_boat_placement_player_screen(boats_player)
        error("Le format n'est pas bon: inscrivez la première et la dernière coordonnée séparées d'un espace: "
              f"{coordinates_str}\nPar exemple: Porte-avion (5 cases) -> A1 A5.")
        return False


def is_space_free(brd, start: tuple[int, int], end: tuple[int, int], orientation: int,
                  boats_player: dict[str: dict[tuple[int, int]: bool]]) -> tuple[bool, list[str]]:
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
    boats_obstructing_list = []
    
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
        
        for boat_name in boats_player:
            for coord in boats_player[boat_name].keys():
                if coord in virtual_coord and boat_name not in boats_obstructing_list:
                    boats_obstructing_list.append(boat_name)
    
    return allowed, boats_obstructing_list
    

def place_boat(brd_player: list[list[int]], boat_name: str, boats_player: dict[str: dict[tuple[int, int]: bool]])\
        -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]], bool]:
    """
    Place one boat on the game board. It returns True if the boat has been placed successfully.
    :param brd_player: Player's game board.
    :param boat_name: Name of the boat.
    :param boats_player: Dictionary storing the player's boats.
    :return: brd_player, boats_player, placed.
    """
    boats_size_list = {"porte-avion": 5, "croiseur": 4, "contre-torpilleur": 3, "sous-marin": 3, "torpilleur": 2}
    exiting = placed = False
    boat_size = boats_size_list[boat_name]
    
    reset_boat_placement_player_screen(boats_player)
    
    while not (exiting or placed):
        print(f"Inscrivez la première et la dernière coordonnée du {boat_name} ({boat_size} cases).",
              # Adapt the example to the boat selected:
              f"Par exemple: -> A1 A{boat_size}.", sep="\n")
        entry = user_input(f"-> ")
        entry = entry.upper()
        
        if entry and entry != "EXIT":
            boat_infos = str_to_boat_coordinates(entry, brd_player, boats_player)
            if boat_infos:  # if the input format is valid
                start, end, orientation, size = boat_infos
                if size == boat_size:
                    space_free, boats_obstructing = is_space_free(brd_player, start, end, orientation, boats_player)
                    if space_free:
                        if orientation:  # 1 = True → Vertical
                            cell = start[0]  # clearer
                            for row in range(start[1], end[1]):  # from start's number to end's number
                                brd_player[row][cell] = 1
                                boats_player[boat_name][(row, cell)] = False  # update coordinates of the boat
                            
                            placed = True
                        else:  # 0 = False → Horizontal
                            row = start[1]
                            for cell in range(start[0], end[0]):  # from start's letter to end's letter
                                brd_player[row][cell] = 1
                                boats_player[boat_name][(row, cell)] = False  # update coordinates of the boat
                            
                            placed = True
                    else:
                        reset_boat_placement_player_screen(boats_player)
                        boat_names_format = f"Le {boats_obstructing[0]}"
                        for i, boat in enumerate(boats_obstructing[1:], 0):
                            if i < len(boats_obstructing) - 2:
                                boat_names_format += f", le {boat}"
                            else:
                                boat_names_format += f" et le {boat}"
                        error(f"{boat_names_format} navigue{"nt" if len(boats_obstructing) > 1 else ""} déjà sur ces "
                              "eaux... L'espace est pris !")
                else:
                    reset_boat_placement_player_screen(boats_player)
                    error(f"La taille du bateau ne correspond pas aux coordonnées saisies: \"{entry}\"",
                          f"({size} cases, alors que le {boat_name} en mesure {boat_size}) !", sep=" ")
        elif entry == "EXIT":
            exiting = True
        else:
            reset_boat_placement_player_screen(boats_player)
            error("Vous devez entrez une valeur !")
    
    return brd_player, boats_player, placed


def delete_boat(brd_player: list[list[int]], boats_player: dict[str: dict[tuple[int, int]: bool]], boat_name: str)\
        -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]]]:
    """
    Replace one boat on the game board.
    :param brd_player: Player's game board.
    :param boats_player: Dictionary storing the player's boats.
    :param boat_name: Name of the boat.
    :return: brd_player, boats_player.
    """
    for row, cell in boats_player[boat_name].keys():
        brd_player[row][cell] = 0
    
    boats_player[boat_name] = {}
    
    return brd_player, boats_player


def replace_boat():
    pass


def boat_placement_player(brd_player: list[list[int]])\
        -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]]]:
    """
    Makes the user place his/her boats.
    :param brd_player: Player's game board.
    :return: brd_player, boats_player.
    """
    boats_size_list = {"porte-avion": 5, "croiseur": 4, "contre-torpilleur": 3, "sous-marin": 3, "torpilleur": 2}
    boats_player = {
        "porte-avion": {},
        "croiseur": {},
        "contre-torpilleur": {},
        "sous-marin": {},
        "torpilleur": {}
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
    
    reset_boat_placement_player_screen(boats_player)

    while not all(boats_status.values()):  # loops until all the boats are positioned
        print("Saisissez le numéro du bateau que vous voulez placer:")
        for i, name in enumerate(boats_status, 1):
            if boats_status[name]:
                colour(Fore.GREEN)
                print(f"\t● {i} -> {name}{" " * (22 - len(name))}({boats_size_list[name]} cases)")
                colour(default_color)
            else:
                print(f"\t◯ {i} -> {name}{" " * (22 - len(name))}({boats_size_list[name]} cases)")
        boat_number_entry = user_input("-> ")
        boat_number_entry = boat_number_entry.upper().replace(' ', '')
        if boat_number_entry.isnumeric():
            boat_number = int(boat_number_entry)
            if 1 <= boat_number <= 5:
                boat = number_to_boat[boat_number]
                if not boats_status[boat]:  # if the boat is not already placed
                    brd_player, boats_player, placed = place_boat(brd_player, boat, boats_player)
                    boats_status[boat] = placed  # updates the boat's status
                    reset_boat_placement_player_screen(boats_player)
                else:
                    reset_boat_placement_player_screen(boats_player)
                    error(f"Le {boat} est déjà placé. Quand j'aurais du temps, je vous proposerais de le replacer...")
                    # replace_entry = user_input("Souhaitez-vous replacer le bateau ? (Y/N)")
            else:
                reset_boat_placement_player_screen(boats_player)
                error(f"Le numéro {boat_number} ne correspond pas à un bateau !")
        elif boat_number_entry == "EXIT":
            reset_boat_placement_player_screen(boats_player)
            error("Vous ne pouvez pas continuer avant d'avoir placé tous vos bateaux !")
        else:
            reset_boat_placement_player_screen(boats_player)
            error("Vous devez saisir un numéro !")
    
    wait_for_user()
    # new page
    clear()
    
    # Ask the user if he/she want to replace a boat (While)
    keep_modifying = True
    while keep_modifying:
        replaced = False
        display_brd_id(boats_player)
        want_replace = user_input("Voulez-vous replacer l'un de vos navires ? (Y/n): ")
        want_replace = want_replace.upper().replace(' ', '')
        if 'Y' == want_replace:
            while not replaced:
                print("Saisissez le numéro du bateau que vous voulez replacer (pour sortir, saisissez \'exit\'):")
                for i, name in enumerate(boats_status, 1):
                    print(f"\t{i} -> {name}{" " * (22 - len(name))}({boats_size_list[name]} cases)")
                replace_entry = user_input("-> ")
                if replace_entry:  # not empty
                    replaced = True
                else:
                    error("")
                clear()
        elif 'N' == want_replace:
            keep_modifying = False
        else:
            clear()
            error(f"Répondez à la question par \'Y\' (Oui) ou \'N\' (Non) uniquement: {want_replace} !")
    
    return brd_player, boats_player


def boat_placement_pc(brd_pc: list[list[int]]) -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]]]:
    """
    Place the computer's boats.
    :param brd_pc: computer's game board.
    :return: brd_pc, boats_pc.
    """
    clear()
    boats_list = [5, 4, 3, 3, 2]
    boats_name = ["porte-avion", "croiseur", "contre-torpilleur", "sous-marin", "torpilleur"]
    boats_pc = {
        "porte-avion": {},
        "croiseur": {},
        "contre-torpilleur": {},
        "sous-marin": {},
        "torpilleur": {}
    }
    i = 0

    print("L'adversaire positionne ses bateaux...")
    
    while i < len(boats_list):
        size = boats_list[i]
        name = boats_name[i]
        orientation = randint(0, 1)
        
        if orientation:  # vertical
            letter = randint(0, 9)
            first_number = randint(0, 9 - size)
            allowed = True
            for number in range(first_number, first_number + size):
                if not brd_pc[letter][number] == 0:
                    allowed = False
            if allowed:
                for number in range(first_number, first_number + size):
                    brd_pc[letter][number] = 1
                    boats_pc[name][(letter, number)] = False
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
                    boats_pc[name][(letter, number)] = False
                i += 1

    sleep(3)  # simulation of the pc placing its boats

    return brd_pc, boats_pc


def normal_mode(level: int):
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)
    
    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view)
            is_player_turn = False
        
        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, level)
            is_player_turn = True
        
        # Check to see if anyone has won and if so, stop the game.
        running = not win(brd_player, brd_pc)
    
    # Tell the user, which one was the most precise.
    display_accuracy(brd_player, brd_pc)


def against_clock_mode(level: int):
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)
    
    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view)
            is_player_turn = False
        
        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, level)
            is_player_turn = True
        
        # Check to see if anyone has won and if so, stop the game.
        running = not win(brd_player, brd_pc)
    
    # Tell the user, which one was the most precise.
    display_accuracy(brd_player, brd_pc)


def accuracy_mode(level: int):
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)
    
    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view)
            is_player_turn = False
        
        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, level)
            is_player_turn = True
        
        # Check to see if anyone has won and if so, stop the game.
        running = not win(brd_player, brd_pc)
    
    # Tell the user, which one was the most precise.
    display_accuracy(brd_player, brd_pc)


def limited_mode(level: int):
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)
    
    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view)
            is_player_turn = False
        
        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, level)
            is_player_turn = True
        
        # Check to see if anyone has won and if so, stop the game.
        running = not win(brd_player, brd_pc)
    
    # Tell the user, which one was the most precise.
    display_accuracy(brd_player, brd_pc)


def is_hit(brd: list[list[int]], target: tuple[int, int]) -> bool:
    """
    Returns True if the target touches a square on a boat.
    :param brd: Game board.
    :param target: Couple of coordinates.
    :return: If the target touches a square on a boat.
    """
    return brd[target[0]][target[1]] == 1 or brd[target[0]][target[1]] == 3


def is_boat_sunk(boat_dict: dict[tuple[int, int]: bool]) -> bool:
    """
    
    :param boat_dict:
    :return:
    """
    return all(boat_dict.values())


def reset_player_round_screen(brd_player: list[list[int]], brd_player_view: list[list[int]]):
    """
    
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    :return:
    """
    clear()
    print("C'est votre tour, Général!")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)


def player_turn(brd_pc: list[list[int]], brd_player: list[list[int]], brd_player_view: list[list[int]])\
        -> tuple[list[list[int]], list[list[int]]]:
    """
    Makes the user play.
    :param brd_pc: Computer's game board.
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    :return: brd_pc, brd_player_view.
    """
    reset_player_round_screen(brd_player, brd_player_view)
    entry = ""
    allowed = False
    target = ()
    
    while not allowed:
        print("Où voulez-vous tirez ? (Inscrivez les coordonnées de la case ciblée)")
        entry = user_input("-> ")
        result = str_to_coordinates(entry)
        if type(result) is tuple:
            target = result
            allowed = True
        elif result == 0:
            reset_player_round_screen(brd_player, brd_player_view)
            error("Le format n'est pas bon: inscrivez les coordonnées de la cible avec la lettre de la colonne et le "
                  "numéro de la ligne. Par exemple: -> A1.")
        elif result == 1:
            reset_player_round_screen(brd_player, brd_player_view)
            error("Vous devez tirer sur le plateau (de A1 à J10) !")

    if is_hit(brd_pc, target):
        brd_pc[target[0]][target[1]] = 3
        brd_player_view[target[0]][target[1]] = 2
    else:
        brd_pc[target[0]][target[1]] = 2
        brd_player_view[target[0]][target[1]] = 1

    clear()
    print(f"Tire en {entry}")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    if is_hit(brd_pc, target):
        colour(red_color)
        print("Touché !")
    else:
        colour(water_color)
        print("Dans l'eau...")
    colour(default_color)
    
    wait_for_user()
    return brd_pc, brd_player_view


def easy_level(brd_pc_view: list[list[int]]) -> tuple[int, int]:
    """
    Compute (Well, not really, but pretend) coordinates of the target.
    :return: target.
    """
    free = value_in_matrix(brd_pc_view, 0)
    return choice(free)


def value_in_matrix(matrix: list[list], value) -> list[tuple[int, int]]:
    """
    
    :param matrix:
    :param value:
    :return:
    """
    value_places = []
    for i, row in enumerate(matrix, 0):
        for j, cell in enumerate(row, 0):
            if cell == value:
                value_places.append((i, j))
    
    return value_places


def should_shoot(hit_coord: list[tuple[int, int]], brd_view: list[list[int]]) -> list[tuple[int, int]]:
    """
    Shoot the cell from below, above, right or left if it has not been hit.
    :param hit_coord:
    :param brd_view:
    :return:
    """
    too_shoot = []
    if len(hit_coord) == 1:
        coord = hit_coord[0]
        # all the possibilities:
        virtual_shoot = [(coord[0] - 1, coord[1]),
                         (coord[0] + 1, coord[1]),
                         (coord[0], coord[1] - 1),
                         (coord[0], coord[1] + 1)]
        
        for coord_shoot in virtual_shoot:
            if 0 <= coord_shoot[0] <= 9 and 0 <= coord_shoot[1] <= 9:
                if brd_view[coord_shoot[0]][coord_shoot[1]] == 0:  # not already shot
                    too_shoot.append(coord_shoot)
    else:
        orientation = determine_orientation(hit_coord[0], hit_coord[-1])
        ic(orientation)
        virtual_shoot = []
        for coord in hit_coord:
            if orientation:  # True → 1 → Horizontal.
                virtual_shoot.append((coord[0], coord[1] - 1))
                virtual_shoot.append((coord[0], coord[1] + 1))
            elif orientation == 0:  # 0 → Vertical.
                virtual_shoot.append((coord[0] - 1, coord[1]))
                virtual_shoot.append((coord[0] + 1, coord[1]))
        
        for coord_shoot in virtual_shoot:
            if 0 <= coord_shoot[0] <= 9 and 0 <= coord_shoot[1] <= 9:
                if brd_view[coord_shoot[0]][coord_shoot[1]] == 0:  # not already shot
                    too_shoot.append(coord_shoot)
    
    return ic(too_shoot)


def intermediate_level(brd_pc_view: list[list[int]]) -> tuple[int, int]:
    """
    
    :param brd_pc_view:
    :return:
    """
    hit_coord = value_in_matrix(brd_pc_view, 2)  # hit cells
    if hit_coord:  # hit_coord isn't empty == True
        """
        regarder quelles cases ne sont pas possible en fonction des tailles de bateaux qu'il reste !
        """
        return choice(should_shoot(hit_coord, brd_pc_view))
    else:  # hit_coord is empty == False
        return easy_level(brd_pc_view)


def difficult_level() -> tuple[int, int]:
    """
    Pareil que "intermediate_level". Sauf quand il faut tirer au pif, la fonction utilise "compute_odds3".
    :return:
    """
    pass


def impossible_level() -> tuple[int, int]:
    """
    Ne vise que sur les bateaux de l'adversaire.
    :return:
    """
    pass


def pc_turn(brd_player: list[list[int]], brd_pc_view: list[list[int]],
            brd_player_view: list[list[int]], level: int) -> list[list[int]]:
    """
    Makes the computer play.
    :param brd_player: Player's game board.
    :param brd_pc_view: Computer's game board view.
    :param brd_player_view: Player's game board view.
    :param level: int.
    :return: brd_player.
    """
    clear()
    letters_place = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
    target = (randint(0, 9), randint(0, 9))

    if level == 0:
        target = (randint(0, 9), randint(0, 9))
    elif level == 1:
        pass
    elif level == 2:
        pass
    elif level == 3:
        pass

    if is_hit(brd_player, target):
        brd_player[target[0]][target[1]] = 3
        brd_pc_view[target[0]][target[1]] = 2
    else:
        brd_player[target[0]][target[1]] = 2
        brd_pc_view[target[0]][target[1]] = 1

    print("C'est au tour de l'adversaire.")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)
    print(f"L'adversaire tire en {letters_place[target[1]]}{target[0]+1}")
    
    if is_hit(brd_player, target):
        colour(red_color)
        print("Touché...")
    else:
        colour(water_color)
        print("Dans l'eau!")
    colour(default_color)
    
    wait_for_user()
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

    if pc_won:  # Shame on the team (WE lost)
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu...")
    elif player_won:  # Glory on the leader (YOU won)
        print("Bravo Général! Vous avez gagné !")

    return pc_won or player_won


def accuracy(brd) -> int:
    """
    Calculates the accuracy of the player and the computer.
    :param brd:
    :return:
    """
    # En fin de compte, accuracy retourne la précision (entre 0 et 1, car c'est un pourcentage).
    # C'est dans le fichier les fonctions de mode de jeu qu'on affichera lequel des deux a été le meilleur.
    pass


def display_accuracy(brd_player, brd_pc) -> None:
    """
    
    :param brd_player:
    :param brd_pc:
    :return:
    """
    player_accuracy = accuracy(brd_player)
    pc_accuracy = accuracy(brd_pc)
    if player_accuracy < pc_accuracy:
        pass
    elif player_accuracy > pc_accuracy:
        pass
    else:
        pass


def will_replay() -> bool:
    """
    
    :return:
    """
    replay = user_input("Voulez-vous rejouer ? (Y/n): ")
    replay = replay.upper()
    if 'N' in replay:
        return False
    elif 'Y' in replay:
        return True
    else:  # if neither N nor Y are contained in "replay".
        print("Nous n'avons pas comprit, mais comme le jeu est incroyable, nous allons vous faire rejouer!\n"
              "(Pour annuler presser les touches CTRL et C simultanément)")
        wait_for_user()
        return True
