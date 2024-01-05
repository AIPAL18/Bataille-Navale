########################################################################################################################
#                                                                                                                      #
#                                                    BATAILLE NAVAL                                                    #
#                                                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾                                                    #
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

color(f_color, Back.BLACK)
playing = True

start()
rules()

while playing:
    running = True
    is_player_round = bool(randint(0, 1))

    if is_player_round:
        print("\nVous jouerez en premier\n")
    else:
        print("\nVotre adversaire jouera en premier\n")
    pause()
    clear()

    brd_pc, brd_player, brd_player_view = build_brd(10)
    brd_player = boat_placement_player(brd_player)

    print("L'adversaire positionne ses bateaux...")

    brd_pc = boat_placement_pc(brd_pc)

    while running:
        clear()
        if is_player_round:
            print("C'est votre tour, Général!")
            brd_pc, brd_player_view = player_round(brd_pc, brd_player, brd_player_view)
            is_player_round = False
            pause()
        else:
            print("C'est au tour de l'adversaire.")
            brd_player = pc_round(brd_player, brd_player_view)
            is_player_round = True
            pause()

        running = not win(brd_player, brd_pc)

    replay = input("Voulez-vous rejouer ? (Y/N)\n>>> ").upper()
    if 'N' in replay:
        playing = False
    elif 'Y' not in replay:
        print("Nous n'avons pas comprit, mais comme le jeu est incroyable, nous allons vous faire rejouer!\n"
              "(Pour annuler presser CTRL+C)")

end()
