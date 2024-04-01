import random
import time

from num2words import num2words as n2w
from colorama import Fore
from bin.local_games import game_constants


def run():
    choices = "RGBYCM"
    simon = ""
    score = 1

    colors = {
        "R": f"{Fore.RED}R{Fore.RESET}",
        "G": f"{Fore.GREEN}G{Fore.RESET}",
        "B": f"{Fore.BLUE}B{Fore.RESET}",
        "Y": f"{Fore.YELLOW}Y{Fore.RESET}",
        "C": f"{Fore.CYAN}C{Fore.RESET}",
        "M": f"{Fore.MAGENTA}M{Fore.RESET}"
    }

    while True:
        print(f"\nRound {n2w(score)}:\nSimon says: ", end="")
        simon += random.choice(choices)

        for i, color in enumerate(simon):
            if i != len(simon) - 1:
                print(f"{colors[color]}... ", end="")
                time.sleep(1)
            else:
                print(f"{colors[color]}")
                time.sleep(1.5)

        game_constants.clear_screen()

        guess = input("What did Simon say? ").upper().strip()

        if guess != simon:
            break
        else:
            score += 1

    print(f"Game over! Your score was: {n2w(score)}")
