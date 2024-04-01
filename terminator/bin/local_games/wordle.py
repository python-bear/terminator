import random
import sys
import os

from num2words import num2words as n2w
from colorama import Fore, Style
from bin.local_games import game_constants


def print_menu():

    print("Type a 5 letter word and hit enter!\n")


def read_words_db():
    with open(os.path.join("lib", "wordle_words.txt"), "r") as file:
        db_words = file.read().splitlines()
        return db_words


def process_words_db():
    with open(os.path.join("lib", "words.txt")) as file:
        db_words = file.read().splitlines()

    with open(os.path.join("lib", "wordle_words.txt"), "w") as file:
        for word in db_words:
            if len(word) == 5 and word.islower() and len(strip_letters(word)) == 0:
                file.write(f"{word}\n")


def strip_letters(text: str) -> str:
    for letter in "abcdefghijklmnopqrstuvwxyz":
        text = text.replace(letter, "")
    return text


def run():
    word_list = read_words_db()
    print(f"{Style.BRIGHT}=== Wordle  ==={Style.RESET_ALL}")

    while True:
        print("Type a 5 letter word and hit enter to start!\n")
        word = random.choice(word_list).lower()

        for attempt in range(1, 7):
            while True:
                guess = game_constants.ask("", (5, 5), silent=True)

                if guess in word_list:
                    break
                else:
                    print(game_constants.input_error("that word is not recognized."))

            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')

            for i in range(min(len(guess), 5)):
                if guess[i] == word[i]:
                    print(f"{Fore.GREEN}{guess[i]}{Fore.RESET}", end="")
                elif guess[i] in word:
                    print(f"{Fore.YELLOW}{guess[i]}{Fore.RESET}", end="")
                else:
                    print(guess[i], end="")
            print()

            if guess == word:
                print(f"{Fore.YELLOW}Congrats! You got the word in {n2w(attempt)} attempts.{Fore.RESET}")
                break
            elif attempt == 6:
                print(f"{Fore.RED}Failure! The wordle was.. {word}{Fore.RESET}")

        if input("Want to play again? ") not in game_constants.yesses:
            break
