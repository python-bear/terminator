import colorama
import random
import sys

from colorama import Fore, Style
from bin.local_games import game_constants


chosen_number = 0
low = 0
high = 101


def choose_number(low_range, high_range):
    global chosen_number

    chosen_number = random.randint(low, high)
    print(f"{Style.RESET_ALL}My number is between {low_range} and {high_range - 1}.")


def guess_number():
    global chosen_number, low, high

    count = 1

    while True:
        while True:
            guess_choice = input("Guess my number: ").lower()

            if guess_choice.isdigit():
                guess = int(guess_choice)
                break
            
            elif guess_choice in ("is even", "is even?", "even?", "even", "if even") or \
                guess_choice in ("quit", "end", "die", "give up", "concede", "suicide", "no", "i don't think so", "n",
                                 "na"):
                guess = 0
                break

            else:
                print(f"{Style.RESET_ALL}It needs to be a number.")

        if guess_choice in ("is even", "even?", "even", "if even"):
            print((chosen_number % 2) == 0)
            count += 1
        
        elif guess_choice in ("quit", "end", "die", "give up", "concede", "suicide", "no", "i don't think so", "n",
                              "na"):
            break

        elif guess == chosen_number:
            print(f"{Style.RESET_ALL}That's my number! ({chosen_number}), good job, it took you {count} guesses.")
            break

        elif guess > chosen_number + (high // 2):
            print(f"{Fore.MAGENTA}Way way too high!!!")

        elif guess < chosen_number - (high // 2):
            print(f"{Fore.MAGENTA}Way way too low!!!")

        elif guess > chosen_number + (high // 4):
            print(f"{Fore.RED}Way too high!")

        elif guess < chosen_number - (high // 4):
            print(f"{Fore.RED}Way too low!")

        elif guess > chosen_number + (high // 8):
            print(f"{Fore.YELLOW}A bit too high.")

        elif guess < chosen_number - (high // 8):
            print(f"{Fore.YELLOW}A bit too low.")

        elif guess > chosen_number + (high // 16):
            print(f"{Fore.GREEN}A little bit too high.")

        elif guess < chosen_number - (high // 16):
            print(f"{Fore.GREEN}A little bit too low.")

        elif guess > chosen_number:
            print(f"{Fore.CYAN}Go a tiny little bit lower.")

        elif guess < chosen_number:
            print(f"{Fore.CYAN}Go a tiny little bit higher.")

        count += 1


def run():
    global low, high, chosen_number
    chosen_number = 0

    while True:
        choose_number(low, high)
        guess_number()

        if input(f"{Style.RESET_ALL}Do you want to play again? ").lower() not in game_constants.yesses:
            break

        else:
            print("\n")
            while True:
                low_choice = input(f"{Style.RESET_ALL}What do you want the lowest number in the range to be? ")

                if low_choice.isdigit():
                    low = int(low_choice)
                    break

                else:
                    print(f"{Style.RESET_ALL}It needs to be a number.")

                print("\n")

            while True:
                high_choice = input(f"{Style.RESET_ALL}What do you want the highest number in the range to be? ")

                if high_choice.isdigit():
                    high = int(high_choice) + 1
                    break

                else:
                    print(f"{Style.RESET_ALL}It needs to be a number.")

                print("\n")
