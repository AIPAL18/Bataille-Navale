from os import system
from time import sleep
from colorama import Fore, Back
f_color = Fore.LIGHTGREEN_EX


def color(*args) -> None:
    """
    Colore l'invite de commande.
    """
    for i in args:
        print(i, end="")


def clear() -> None:
    """
    Efface la console.
    """
    system("cls")


def pause() -> None:
    """
    Pause le jeu.
    """
    color(Fore.LIGHTBLACK_EX)
    input('(pressez Entrer)')
    color(f_color)


def start() -> None:
    """
    Initialise le jeu : lance l'écran d'accueil avec les crédits, affiche les recommandations de jeu et colore l'écran.
    """
    clear()
    print("""\n
    \t##########################################################
    \t#                    BATAILLE NAVAL                      #
    \t#                    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾                      #
    \t#                                                        #
    \t#           Par Elie Ruggiero et Enzo Chauvet            #
    \t#                                                        #
    \t#              Décembre 2023 - Janvier 2024              #
    \t##########################################################\n\n""")
    color(Fore.YELLOW)
    print("Nous vous conseillons, pour avoir une meilleur expérience, de démarrer ce programme "
          "dans un invite de commande.\n\n")
    pause()
    clear()


def rules() -> None:
    """
    Affiche les règles du jeu.
    """
    print("\nDéroulement du jeu:\n"
          "Chacun votre tour, vous tirerez sur le plateau ennemi en essayant de toucher ses navires.\n"
          "Le premier à couler toute la flotte adverse gagne.\n"
          "Bonne chance !\n")

    pause()
    clear()


def end() -> None:
    """
    Réinitialise les couleurs de l'invite de commande.
    """
    color(Fore.RESET, Back.RESET)
