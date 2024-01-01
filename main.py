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

start()

brd = [[False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [False, None, None, None, False, False, False, False, None, None],
       [False, None, None, None, None, None, None, None, None, None],
       [None, False, False, None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None, None, None, None],
       [None, None, None, None, None, False, None, None, None, None],
       [None, None, None, None, None, False, None, False, False, False],
       [None, None, None, None, None, False, None, None, None, None]]

brd_view = [[None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None]]

boats_dict = {
    "pa": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],   # porte-avion
    "c": [(4, 3), (5, 3), (6, 3), (7, 3)],            # croiseur
    "ct": [(5, 7), (5, 8), (5, 9)],                   # contre-torpilleur
    "sm": [(7, 8), (8, 8), (9, 8)],                   # sous-marin
    "t": [(1, 5), (2, 5)],                            # torpilleur
}

target = (1, 1)

brd, brd_view = pc_round(brd, brd_view)
display_brd(brd, False)
display_brd(brd_view, True)
print(win(brd, is_player_round=True))
color(Fore.RESET, Back.RESET)
