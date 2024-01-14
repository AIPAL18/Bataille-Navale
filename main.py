########################################################################################################################
#                                                                                                                      #
#                                                   BATAILLE NAVALE                                                    #
#                                                   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                                                    #
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
from functions import *

# Initialise the game.
playing = init()  # why does it return true ?

# Replay loop
while playing:
    # Sets the variables
    running = True
    mode = select_mode()
    level = select_level()
    is_player_round = first_player()  # True if the player start playing
    brd_pc, brd_player, brd_pc_view, brd_player_view = build_brd()
    brd_player, boats_player_dict = boat_placement_player(brd_player)
    brd_pc, boats_pc_dict = boat_placement_pc(brd_pc)
    
    # Game loop
    while running:
        if is_player_round:  # player's round
            brd_pc, brd_player_view = player_round(brd_pc, brd_player, brd_player_view)
            is_player_round = False
        
        else:  # computer's round
            brd_player = pc_round(brd_player, brd_pc_view, brd_player_view, level)
            is_player_round = True
        
        # Check to see if anyone has won and if so, stop the game.
        running = not win(brd_player, brd_pc)
    
    # Tell the user, which one was the most precise.
    display_accuracy(brd_player, brd_pc)

    # Asks the user if he wants to play again.
    playing = will_replay()

# Resets the colours of the command prompt.
clean()
