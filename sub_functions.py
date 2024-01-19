from ui import *
from random import choice, choices
import re


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
    :return: is_space_free, list of boat's name already placed on these coordinates.
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


def determine_orientation(first_coord, second_coord) -> int | None:
    """
    Determines orientation from two set of coordinates.
    1 means horizontal, 0 means vertical and None means diagonal.
    :param first_coord: First set of coordinates.
    :param second_coord: Second set of coordinates.
    :return: orientation.
    """
    if first_coord[0] == second_coord[0]:  # horizontal
        return 1
    elif first_coord[1] == second_coord[1]:  # vertical
        return 0
    else:  # neither
        return None


def str_to_coordinate(coordinate_str: str) -> tuple[int, int] | int:
    """
    Transforms a string into a set of coordinates if possible, otherwise it returns the error_code.
    :param coordinate_str: Coordinates written with a letter and a number.
    :return: coordinates or error_code.
    """
    letters_place = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}

    # Intelligent recognition: (it will not extract a string if it already knows that it is not on the game board)
    if re.search(r"[A-J][0-9]{1,2}", coordinate_str):  #
        coordinate_str = re.search(r"[A-J][0-9]{1,2}", coordinate_str).group()

    if re.search(r"^[A-Z][0-9]+$", coordinate_str):  # if the input format is valid.
        """
        index = number - 1
        It is already calculated for the letters in the dictionary above.
        We calculate the index from the number above.
        """
        letter = coordinate_str[0]
        number = int(coordinate_str[1:]) - 1
        if letter in letters_place.keys() and 0 <= number <= 9:
            return number, letters_place[letter]
        else:
            # out of the board
            return 1
    else:
        # invalid input format
        return 0


def boat_limits_size(first_coord: tuple[int, int], second_coord: tuple[int, int], orientation: int)\
        -> tuple[tuple[int, int], tuple[int, int], int]:
    """
    Calculates the start, the end and the size of the boat with two set of coordinates and the orientation.
    :return: start, end, size.
    """
    # we use letters_place because we checked, with the regex above, that the input format is valid.
    letter_a = first_coord[0]  # letter of the first set of coordinates.
    letter_b = second_coord[0]  # letter of the second set of coordinates.

    # we use int() because we checked, with the regex above, that the input format is respected.
    number_a = first_coord[1]  # number in the first set of coordinates.
    number_b = second_coord[1]  # number in the second set of coordinates.
    size = 0
    start = end = ()

    if orientation == 0:  # letters are the same → vertical.
        # Enables the start and end of the boat to be interchanged.
        if letter_a > letter_b:
            start = (number_b, letter_b)  # reel number = index+1 so index = number_b-1
            end = (number_a, letter_a + 1)  # reel number = index+1 so index = number_a-1
        else:
            start = (number_a, letter_a)
            end = (number_b, letter_b + 1)

        size = end[1] - start[1]  # calculates the size of the boat

    elif orientation == 1:  # numbers are the same → horizontal.
        # Enables the start and end of the boat to be interchanged.
        if number_a > number_b:
            start = (number_b, letter_b)
            end = (number_a + 1, letter_a)
        else:
            start = (number_a, letter_a)
            end = (number_b + 1, letter_b)

        size = end[0] - start[0]  # calculates the size of the boat

    return start, end, size


def place_boat(brd_player: list[list[int]], boat_name: str, boats_player: dict[str: dict[tuple[int, int]: bool]],
               delete_before: bool = False) -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]], bool]:
    """
    Places one boat on the game board. It returns True if the boat has been placed successfully.
    :param brd_player: Player's game board.
    :param boat_name: Boat's name.
    :param boats_player: Dictionary storing the player's boats.
    :param delete_before: If True, it deletes the boat before placing it (used when a boat is replaced).
    :return: brd_player, boats_player, placed.
    """
    boats_size_dict = {"porte-avion": 5, "croiseur": 4, "contre-torpilleur": 3, "sous-marin": 3, "torpilleur": 2}
    exiting = placed = False
    boat_size = boats_size_dict[boat_name]

    reset_boat_placement_player_screen(boats_player, replacing=delete_before)

    while not (exiting or placed):
        print(f"Inscrivez la première et la dernière coordonnée du {boat_name} ({boat_size} cases).",
              # Adapt the example to the boat selected:
              f"Par exemple: -> A1 A{boat_size}.", sep="\n")
        coord_entry = user_input(f"-> ")
        coord_entry = coord_entry.upper()

        # Intelligent recognition: (it will not extract a string if it already knows that it is not on the game board)
        if re.search(r"[A-J][0-9]{1,2} [A-J][0-9]{1,2}", coord_entry):
            coord_entry = re.search(r"[A-J][0-9]{1,2} [A-J][0-9]{1,2}", coord_entry).group()

        if coord_entry:
            if coord_entry != "EXIT":
                if re.search(r"^[A-Z][0-9]+ [A-Z][0-9]+$", coord_entry):  # if the input format is valid.
                    coord_a_str, coord_b_str = coord_entry.split(' ')  # split the string into two set of coordinates.
                    coord_a = str_to_coordinate(coord_a_str)  # we won't process the error 0, the input format is valid.
                    coord_b = str_to_coordinate(coord_b_str)

                    if type(coord_a) is tuple and type(coord_b) is tuple:
                        orientation = determine_orientation(coord_a, coord_b)

                        if orientation == 0 or orientation == 1:
                            start, end, size = boat_limits_size(coord_a, coord_b, orientation)

                            if size == boat_size:
                                space_free, boats_obstructing = is_space_free(brd_player, start, end,
                                                                              orientation, boats_player)

                                if space_free:
                                    if delete_before:  # only used when we replace a boat
                                        brd_player, boats_player = delete_boat(brd_player, boats_player, boat_name)

                                    if orientation:  # 1 = True → Horizontal
                                        row = start[1]  # clearer
                                        for cell in range(start[0], end[0]):  # from start's letter to end's letter
                                            brd_player[row][cell] = 1
                                            # update coordinates of the boat
                                            boats_player[boat_name][(row, cell)] = False

                                        placed = True
                                    else:  # 0 = False → Vertical
                                        cell = start[0]  # clearer
                                        for row in range(start[1], end[1]):  # from start's number to end's number
                                            brd_player[row][cell] = 1
                                            # update coordinates of the boat
                                            boats_player[boat_name][(row, cell)] = False

                                        placed = True
                                elif len(boats_obstructing) == 1 and boats_obstructing[0] == boat_name:
                                    reset_boat_placement_player_screen(boats_player, replacing=delete_before)
                                    placed = True  # the boat was already placed onto these coordinates
                                else:
                                    reset_boat_placement_player_screen(boats_player, replacing=delete_before)

                                    print(list(boats_player[boat_name].keys())[0], start,
                                          list(boats_player[boat_name].keys())[-1], end, sep="\n")

                                    boat_names_format = f"Le {boats_obstructing[0]}"
                                    for i, boat in enumerate(boats_obstructing[1:], 0):
                                        if i < len(boats_obstructing) - 2:
                                            boat_names_format += f", le {boat}"
                                        else:
                                            boat_names_format += f" et le {boat}"
                                    error(f"{boat_names_format} navigue{'nt' if len(boats_obstructing) > 1 else ''} "
                                          "déjà sur ces eaux... L'espace est pris !")
                            else:
                                reset_boat_placement_player_screen(boats_player, replacing=delete_before)
                                error("La taille du bateau ne correspond pas aux coordonnées saisies: ",
                                      f"\'{coord_entry}\'\n"
                                      f"({size} cases, alors que le {boat_name} en mesure {boat_size}) !", sep=" ")

                        else:  # letters and numbers are different.
                            reset_boat_placement_player_screen(boats_player, replacing=delete_before)
                            error(f"Général, le bateau ne peut pas être placé en diagonale: \'{coord_entry}\' !")
                    elif coord_a == 1 or coord_b == 1:  # boat isn't on the game board.
                        reset_boat_placement_player_screen(boats_player, replacing=delete_before)
                        error(f"Le bateau doit être placé sur la mer (de A1 à J10): \'{coord_entry}\' !")
                else:
                    reset_boat_placement_player_screen(boats_player, replacing=delete_before)
                    error("Le format n'est pas bon: inscrivez la première et la dernière coordonnée séparées d'un "
                          f"espace: \'{coord_entry}\'\nPar exemple: Porte-avion (5 cases) -> A1 A5.")
            else:
                exiting = True
        else:
            reset_boat_placement_player_screen(boats_player, replacing=delete_before)
            error("Vous devez entrez une valeur !")

    return brd_player, boats_player, placed


def delete_boat(brd_player: list[list[int]], boats_player: dict[str: dict[tuple[int, int]: bool]], boat_name: str)\
        -> tuple[list[list[int]], dict[str: dict[tuple[int, int]: bool]]]:
    """
    Deletes one boat on the game board.
    :param brd_player: Player's game board.
    :param boats_player: Dictionary storing the player's boats.
    :param boat_name: Boat's name.
    :return: brd_player, boats_player.
    """
    for coordinate in boats_player[boat_name].keys():
        brd_player[coordinate[0]][coordinate[1]] = 0

    boats_player[boat_name] = {}
    return brd_player, boats_player


def is_hit(brd: list[list[int]], boat_dict: dict[str: dict[tuple[int, int]: bool]], target: tuple[int, int])\
        -> tuple[dict[str: dict[tuple[int, int]: bool]], bool]:
    """
    Returns True if the target hits a cell on a boat and the boat's dictionary has been modified accordingly.
    :param brd: Game board.
    :param boat_dict: Dictionary storing the boats.
    :param target: Couple of coordinates.
    :return: boat_dict, If the target touches a square on a boat.
    """
    # intact or hit or sunk
    hit = brd[target[0]][target[1]] == 1 or brd[target[0]][target[1]] == 3 or brd[target[0]][target[1]] == 4
    if hit:
        for boat_name, boat in zip(boat_dict, boat_dict.values()):
            for coord in boat.keys():
                if target == coord:
                    boat_dict[boat_name][coord] = True
                    
    return boat_dict, hit


def is_new_sunk(brd: list[list[int]], boat_coordinates: list[tuple[int, int]], is_view: bool) -> bool:
    """
    Check if the boat has been already sunk.
    :param brd: Game board.
    :param boat_coordinates: List of every coordinate of the boat.
    :param is_view: True if the game board is a view.
    :return: is_new_sunk.
    """
    is_new = True
    
    for coord in boat_coordinates:
        if is_view:
            if brd[coord[0]][coord[1]] != 2:  # hit
                is_new = False
        else:
            if brd[coord[0]][coord[1]] != 3:  # hit
                is_new = False
        
    return is_new


def boats_sunk(brd: list[list[int]], boats_dict: dict[str: dict[tuple[int, int]: bool]], is_view: bool = False)\
        -> tuple[list[list[int]], str]:
    """
    Sunk the boat if all their cells are hit.
    :param brd: Game board.
    :param boats_dict: Dictionary storing the boats.
    :param is_view: True if the game board is a view.
    :return: brd, name_sunk of the new boat sunk, if any.
    """
    name_sunk = ""
    
    for boat_name, boat in boats_dict.items():
        # if the boat is sunk for the first time
        # the second therm is only processed if the first is True, so we won't check is_new_sunk() for every boat.
        if all(boat.values()) and is_new_sunk(brd, list(boat.keys()), is_view):
            name_sunk = boat_name
            for coord, hit in boats_dict[boat_name].items():
                if is_view:
                    brd[coord[0]][coord[1]] = 3  # sunk the boat on the brd
                else:
                    brd[coord[0]][coord[1]] = 4  # sunk the boat on the brd
    
    return brd, name_sunk


def easy_level(brd_pc_view: list[list[int]]) -> tuple[int, int]:
    """
    Compute (Well, not really, but pretend) coordinates of the target.
    :return: target.
    """
    free = value_in_matrix(brd_pc_view, 0)
    return choice(free)


def value_in_matrix(matrix: list[list], value) -> list[tuple[int, int]]:
    """
    Returns the indexes of each value in the matrix.
    :param matrix: Matrix, in which the function will search.
    :param value: Value sought by the function.
    :return: value_places.
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
    :param hit_coord: all the coordinate that the function can shoot.
    :param brd_view: True if the game board is a view.
    :return: targets.
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

    return too_shoot


def intermediate_level(brd_pc_view: list[list[int]]) -> tuple[int, int]:
    """
    Computes the coordinates that the computer must shoot.
    :param brd_pc_view: Computer's game board view.
    :return: target.
    """
    hit_coord = value_in_matrix(brd_pc_view, 2)  # hit cells
    if hit_coord:  # hit_coord isn't empty == True
        """
        regarder quelles cases ne sont pas possible en fonction des tailles de bateaux qu'il reste !
        """
        print("we know...")
        return choice(should_shoot(hit_coord, brd_pc_view))
    else:  # hit_coord is empty == False
        print("au pif")
        return easy_level(brd_pc_view)


def difficult_level(boat_player_dict: dict[str: dict[tuple[int, int]: bool]]) -> tuple[int, int]:
    """
    Pareil que "intermediate_level". Sauf quand il faut tirer au pif, la fonction utilise "compute_odds3".
    :return:
    """
    # The values are saved in variables for reasons of clarity and ease of access to readjust parameters if necessary.
    empty_value = 1
    second_tier = 30
    full_tier = 100
    boats_coordinates = []
    brd_coord = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                 (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                 (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                 (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                 (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                 (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
                 (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9),
                 (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
                 (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
    
    for boat_dict in boat_player_dict.values():
        for coord, hit in boat_dict.items():
            if not hit:
                boats_coordinates.append(coord)  # fills boats_coordinates with the coordinates of the player's boats.
    
    odds = [empty_value for _ in range(100)]
    for x, y in boats_coordinates:
        for i in range(10):
            for j in range(10):
                """
                We have decided to represent a two-dimensional matrix by a one-dimensional matrix instead of using a
                flatten function. This is the reason why we calculate x * 10 + j.
                """
                if odds[i * 10 + j] == empty_value:
                    if x - 1 <= i <= x + 1 and y - 1 <= j <= y + 1:
                        odds[i * 10 + j] = second_tier

                if odds[i * 10 + j] == second_tier:
                    if i == x and j == y:
                        odds[i * 10 + j] = full_tier
     
    return choices(brd_coord, odds, k=1)[0]  # choices returns a list


def impossible_level(boats_dict: dict[str: dict[tuple[int, int]: bool]])\
        -> tuple[int, int]:
    """
    Makes computer shot on the coordinates of player bot.
    :param boats_dict: dict[str: dict[tuple[int, int]: bool]]
    :return: tuple[int, int]
    """
    target = ()
    
    for boat_name in boats_dict:
        for boats_coordinates, shot in boats_dict[boat_name].items():
            if not (shot or target):
                target = boats_coordinates

    return target
