from sub_functions import *


def select_mode() -> int:
    """
    Returns the level of difficulty chosen by the user.
    """
    clear()
    mode = 0
    is_cheat_code_activated = False
    allowed = False
    print("Choisissez le mode de jeu en inscrivant le numéro correspondant: (Tapez \'rules\' pour avoir les règles)",
          "\t1 - Normal",
          "\t2 - Contre-la-montre",
          "\t3 - Précis",
          "\t4 - Restreint", sep="\n")

    while not allowed:
        entry = user_input("-> ")
        if entry:
            if entry.isnumeric():
                mode = int(entry) - 1
                if 0 <= mode <= 3:
                    allowed = True
                else:
                    error("La valeur entrée doit correspondre à un niveau de difficulté !")
            elif entry.upper().replace(' ', '') == "RULES":
                print("""\t* Mode Normal
                Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.
                Le premier à couler toute la flotte adverse gagne.
                Sinon, vous perdez.
                """)
                print("""\t* Mode Contre-la-montre
                Vous disposez de 20 minutes pour tirer sur le plateau ennemi en essayant de toucher ses navires.
                Votre temps vous sera afficher régulièrement.
                Le premier à couler toute la flotte adverse avant le temps impartie ne soit écoulé gagne.
                Si avant d'avoir commencé votre tour, votre temps s'est écoulé, vous perdez.
                """)
                print("""\t* Mode Précis
                Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.
                Pour gagner, vous devez être le premier à couler la flotte adverse en touchant 35% du temps.
                Dans le cas inverse, vous perdez.
                """)
                print("""\t* Mode Restreint
                Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.
                Vous ne disposez que de 35 tours pour couler la flotte adverse et gagner.
                Dans le case échant, vous perdez.
                """)
            elif entry == "les carottes sont cuites":
                mode = -1
                allowed = True
                clear()
                print("Choisissez le mode de jeu en inscrivant le numéro correspondant: "
                      "(Tapez \'rules\' pour avoir les règles)",
                      "\t1 - Normal",
                      "\t2 - Contre-la-montre",
                      "\t3 - Précis",
                      "\t4 - Restreint", sep="\n")
                print("-> 1")
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


def normal_mode(level: int):
    """
    Elie -> accuracy to tell !!
    :param level:
    :return:
    """
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)

    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view, boats_pc_dict)
            is_player_turn = False

        else:  # computer's round
            brd_player, brd_pc_view = pc_turn(brd_player, brd_pc_view, brd_player_view, boats_player_dict, level)
            is_player_turn = True

        # Check to see if anyone has won and if so, stop the game.
        if win(brd_player, brd_pc):
            running = False


def against_clock_mode(level: int):
    """
    
    Elie.
    :param level:
    :return:
    """
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)

    clear()
    user_input("Le jeu commence dès que vous presserez Entrer:")

    end_time = time() + 120  # 1200 seconds = 20 minutes
    # unfortunately, we cannot display the remaining time

    # Game loop
    running = True
    while running:
        if time() < end_time:  # if the player still has time to play
            if is_player_turn:  # player's round
                brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view, boats_pc_dict)
                is_player_turn = False

            else:  # computer's round
                brd_player, brd_pc_view = pc_turn(brd_player, brd_pc_view, brd_player_view, boats_player_dict, level)
                is_player_turn = True
        else:
            clear()
            colour(red_color)
            print("Vous avez épuisé votre temps... ")
            colour(default_color)
            running = False
        
        # Check to see if anyone has won and if so, stop the game.
        if win(brd_player, brd_pc):
            running = False


def accuracy_mode(level: int):
    """
    
    Elie.
    :param level:
    :return:
    """
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)

    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view, boats_pc_dict)
            is_player_turn = False

        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, boats_player_dict, level)
            is_player_turn = True

        # Check to see if anyone has won and if so, stop the game.
        won = win(brd_player, brd_pc, display=False)
        player_accuracy = accuracy(brd_player_view)
        if player_accuracy >= .35 and won:
            win(brd_player, brd_pc)
        elif won:
            clear()
            colour(red_color)
            print(f"Vous avez perdu car votre précision est de {accuracy(brd_player_view) * 10}% ! (> 35%)")
            colour(default_color)
        
        running = not won


def limited_mode(level: int):
    """
    
    Elie.
    :param level:
    :return:
    """
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)

    # Game loop
    won = False
    for _ in range(35):
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view, boats_pc_dict)
            is_player_turn = False

        else:  # computer's round
            brd_player = pc_turn(brd_player, brd_pc_view, brd_player_view, boats_player_dict, level)
            is_player_turn = True

        # Check to see if anyone has won and if so, stop the game.
        if win(brd_player, brd_pc):
            won = True
    
    if not won:
        clear()
        colour(red_color)
        print("Vous avez perdu ! 35 tours sont passés sans que vous ne gagniez.")
        colour(default_color)


def cheat_mode(level: int):
    """

    :param level:
    :return:
    """
    is_player_turn = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)

    # Game loop
    running = True
    while running:
        if is_player_turn:  # player's round
            brd_pc, brd_player_view = player_turn(brd_pc, brd_player, brd_player_view, boats_pc_dict, True)
            is_player_turn = False

        else:  # computer's round
            brd_player, brd_pc_view = pc_turn(brd_player, brd_pc_view, brd_player_view, boats_player_dict, level)
            is_player_turn = True

        # Check to see if anyone has won and if so, stop the game.
        if win(brd_player, brd_pc):
            running = False


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
            if boats_status[name]:  # already placed
                colour(Fore.GREEN)
                print(f"\t● {i} -> {name}{' ' * (22 - len(name))}({boats_size_list[name]} cases)")
                colour(default_color)
            else:  # not placed yet
                print(f"\t◯ {i} -> {name}{' ' * (22 - len(name))}({boats_size_list[name]} cases)")
        boat_number_entry = user_input("-> ")
        boat_number_entry = boat_number_entry.upper().replace(' ', '')
        
        if boat_number_entry:  # not empty
            if boat_number_entry.isnumeric():
                boat_number = int(boat_number_entry)
                if 1 <= boat_number <= 5:
                    boat_name = number_to_boat[boat_number]
                    if not boats_status[boat_name]:  # if the boat is not already placed
                        brd_player, boats_player, placed = place_boat(brd_player, boat_name, boats_player)
                        boats_status[boat_name] = placed  # updates the boat's status (we can exit the place_boat loop).
                        reset_boat_placement_player_screen(boats_player)
                    else:
                        answered = False
                        reset_boat_placement_player_screen(boats_player)
                        while not answered:
                            want_replace = user_input(f"Le {boat_name} est déjà placé. "
                                                      f"Voulez-vous le replacer ? (Y/n): ")
                            want_replace = want_replace.upper().replace(' ', '')
                            if 'Y' == want_replace:
                                brd_player, boats_player, replaced = place_boat(brd_player, boat_name, boats_player,
                                                                                True)
                                answered = True
                            elif 'N' == want_replace:
                                answered = True
                            else:
                                reset_boat_placement_player_screen(boats_player)
                                error(f"Répondez à la question par \'Y\' (Oui) ou \'N\' (Non) uniquement: "
                                      f"{want_replace} !")
                        reset_boat_placement_player_screen(boats_player)
                else:
                    reset_boat_placement_player_screen(boats_player)
                    error(f"Le numéro {boat_number} ne correspond pas à un bateau !")
            elif boat_number_entry == "EXIT":
                reset_boat_placement_player_screen(boats_player)
                error("Vous ne pouvez pas continuer avant d'avoir placé tous vos bateaux !")
            else:
                reset_boat_placement_player_screen(boats_player)
                error("Vous devez saisir un numéro !")
        else:
            reset_boat_placement_player_screen(boats_player)
            error("Vous devez saisir une valeur !")
    
    reset_boat_placement_player_screen(boats_player)

    # Ask the user if he/she want to replace a boat (While)
    keep_modifying = True
    while keep_modifying:
        replaced = exiting = False
        want_replace = user_input("Voulez-vous replacer l'un de vos navires ? (Y/n): ")
        want_replace = want_replace.upper().replace(' ', '')
        if 'Y' == want_replace:
            while not (exiting or replaced):
                print("Saisissez le numéro du bateau que vous voulez replacer:")
                for i, name in enumerate(boats_status, 1):
                    print(f"\t{i} -> {name}{' ' * (22 - len(name))}({boats_size_list[name]} cases)")
                boat_number_entry = user_input("-> ").upper().replace(' ', '')
                if boat_number_entry:  # not empty
                    if boat_number_entry.isnumeric():
                        boat_number = int(boat_number_entry)
                        if 1 <= boat_number <= 5:
                            boat_name = number_to_boat[boat_number]
                            brd_player, boats_player, replaced = place_boat(brd_player, boat_name, boats_player, True)
                            reset_boat_placement_player_screen(boats_player)
                        else:
                            reset_boat_placement_player_screen(boats_player)
                            error(f"Le numéro {boat_number} ne correspond pas à un bateau !")
                    else:
                        reset_boat_placement_player_screen(boats_player)
                        error("Vous devez saisir un numéro !")
                elif boat_number_entry == "EXIT":
                    exiting = True
                else:
                    reset_boat_placement_player_screen(boats_player)
                    error("Empty")
        elif 'N' == want_replace:
            keep_modifying = False
        else:
            reset_boat_placement_player_screen(boats_player)
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


def player_turn(brd_pc: list[list[int]], brd_player: list[list[int]], brd_player_view: list[list[int]],
                boats_pc_dict: dict[str: dict[tuple[int, int]: bool]], cheat: bool = False)\
        -> tuple[list[list[int]], list[list[int]]]:
    """
    Makes the user play.
    :param brd_pc: Computer's game board.
    :param brd_player: Player's game board.
    :param brd_player_view: Player's game board view.
    :param boats_pc_dict:
    :param cheat:
    :return: brd_pc, brd_player_view.
    """
    reset_player_round_screen(brd_player, brd_player_view)
    letter_place = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
    entry = ""
    allowed = False
    target = ()
    
    if cheat:
        target = impossible_level(boats_pc_dict)
        entry = letter_place[target[1]] + str(target[0] + 1)
    else:
        while not allowed:
            print("Où voulez-vous tirez ? (Inscrivez les coordonnées de la case ciblée)")
            entry = user_input("-> ")
            result = str_to_coordinate(entry)
            if type(result) is tuple:
                target = result
                allowed = True
            elif result == 0:
                reset_player_round_screen(brd_player, brd_player_view)
                error("Le format n'est pas bon: inscrivez les coordonnées de la cible avec la lettre de la colonne et "
                      "le numéro de la ligne. Par exemple: -> A1.")
            elif result == 1:
                reset_player_round_screen(brd_player, brd_player_view)
                error("Vous devez tirer sur le plateau (de A1 à J10) !")
    
    boats_pc_dict, hit = is_hit(brd_pc, boats_pc_dict, target)
    
    if hit:
        brd_pc[target[0]][target[1]] = 3
        brd_player_view[target[0]][target[1]] = 2
    else:
        brd_pc[target[0]][target[1]] = 2
        brd_player_view[target[0]][target[1]] = 1
    
    brd_player_view, sunk_name = boats_sunk(brd_player_view, boats_pc_dict, is_view=True)
    brd_pc, sunk_name = boats_sunk(brd_pc, boats_pc_dict)
    
    clear()
    print(f"Tire en {entry}")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)

    if hit:
        colour(red_color)
        print("Touché !")
        if sunk_name:
            colour(yellow_color)
            print(f"Le {sunk_name} est coulé !")
    else:
        colour(water_color)
        print("Dans l'eau...")
    colour(default_color)

    wait_for_user()
    return brd_pc, brd_player_view


def pc_turn(brd_player: list[list[int]], brd_pc_view: list[list[int]],
            brd_player_view: list[list[int]], boat_player_dict: dict[str: dict[tuple[int, int]: bool]], level: int)\
        -> tuple[list[list[int]], list[list[int]]]:
    """
    Makes the computer play.
    :param brd_player: Player's game board.
    :param brd_pc_view: Computer's game board view.
    :param brd_player_view: Player's game board view.
    :param boat_player_dict: pass.
    :param level: int.
    :return: brd_player, brd_pc_view.
    """
    clear()
    letters_place = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
    target = ()

    if level == 0:
        target = easy_level(brd_pc_view)
    elif level == 1:
        target = intermediate_level(brd_pc_view)
    elif level == 2:
        target = difficult_level(boat_player_dict)
    elif level == 3:
        target = impossible_level(boat_player_dict)
    
    boat_player_dict, hit = is_hit(brd_player, boat_player_dict, target)

    if hit:
        brd_player[target[0]][target[1]] = 3
        brd_pc_view[target[0]][target[1]] = 2
    else:
        brd_player[target[0]][target[1]] = 2
        brd_pc_view[target[0]][target[1]] = 1
    
    brd_pc_view, sunk_name = boats_sunk(brd_pc_view, boat_player_dict, is_view=True)
    brd_player, sunk_name = boats_sunk(brd_player, boat_player_dict)
    
    print("C'est au tour de l'adversaire.")
    display_brd(brd_player_view)
    display_brd(brd_player, is_view=False)
    print(f"L'adversaire tire en {letters_place[target[1]]}{target[0]+1}")

    if hit:
        colour(red_color)
        print("Touché...")
        if sunk_name:
            colour(yellow_color)
            print(f"Prenez les bouées ! Le {sunk_name} coule !!")
    else:
        colour(water_color)
        print("Dans l'eau!")
    colour(default_color)

    wait_for_user()
    return brd_player, brd_pc_view


def win(brd_player: list[list[int]], brd_pc: list[list[int]], display: bool = True) -> bool:
    """
    Returns True and announce the winner if there's a winner, which will stop the game.
    :param brd_player: Player's game board.
    :param brd_pc: Computer's game board.
    :param display: print ?
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

    if display and pc_won:  # Shame on the team (WE lost)
        clear()
        print("MAYDAY, MAYDAY, MAYDAY! Tous nos navires sont en train de couler Général! Nous avons perdu...")
    elif display and player_won:  # Glory on the leader (YOU won)
        clear()
        print("Bravo Général! Vous avez gagné !")

    return pc_won or player_won


def accuracy(brd_view: list[list[int]]) -> float:
    """
    Calculates the accuracy of the player and the computer.
    :param brd_view: list[list[int]]
    :return: float
    """
    water_shots = success_shots = result = 0

    for row in range(len(brd_view)):
        print(brd_view[row])
        for cell in brd_view[row]:
            if cell == 1:
                water_shots += 1
            elif cell > 1:  # 2 = hit, 3 = sunk
                success_shots += 1

    total_shots = water_shots + success_shots
    if total_shots > 0:
        result = success_shots / total_shots
    
    return round(result, 2)


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
