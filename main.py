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
    mode = select_mode()
    print('\n-------------------------------------------------------'
          '-------------------------------------------------------', end="")
    level = select_level()
    
    if mode == -1:
        cheat_mode(level)
    elif mode == 0:
        normal_mode(level)
    elif mode == 1:
        against_clock_mode(level)
    elif mode == 2:
        accuracy_mode(level)
    elif mode == 3:
        limited_mode(level)

    # Asks the user if he wants to play again.
    playing = will_replay()

# Resets the colours of the command prompt.
clean()
