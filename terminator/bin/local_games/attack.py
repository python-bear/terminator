import colorama
import random
import time

from bin.local_games import game_constants
from colorama import Fore


symb = {
    "[": f"{Fore.MAGENTA}[{Fore.RESET}",
    "]": f"{Fore.MAGENTA}]{Fore.RESET}"
}


def run():
    thugs = random.randint(1, 50)
    while True:
        if thugs <= 0:
            print(f"You've escaped the wild thug attack! You walk off into the night...")
            break
        else:
            print(f"\nYou've been attacked by {thugs} hostile thugs!")
            choice = input(f"What will you do {symb['[']}{Fore.YELLOW}run/talk/fight/rizz{symb[']']}? ").lower()

        if choice == "run":
            stamina = random.randint(2, 4)
            while stamina > 0 and thugs > 0:
                lost = random.randint(0, 10)

                if lost > thugs:
                    lost = thugs

                if lost == 0:
                    print("You try to run away, but they black, so you don't get very far before they gang bang you.")
                else:
                    stamina -= random.randint(1, 2)
                    if stamina < 0:
                        stamina = 0
                    print(
                        f"They're fast, but you manage to lose {lost} of them while running past KFC. But, you've only "
                        f"got {stamina} stamina left.")
                    thugs -= lost
                    action = input(f"What will you choose to do "
                                   f"{symb['[']}{Fore.YELLOW}run/talk/rizz{symb[']']}? ").lower()

                    if action == "talk":
                        words = input("What will you say? ")

                        print(f"You tell the thugs '{words}'")

                        if "thug" in words.lower():
                            print("Yo, fag you can't call us that! the thugs yell, then proceed to bash you")
                        else:
                            print("Give us yo chicken wings")
                            time.sleep(2)
                            wings = random.randint(0, 2)
                            print(f"You have {wings}! You tell the thugs.")

                            if wings == 0:
                                print("Aight, well have to kill you then.")
                                stamina = 0
                            else:
                                print("Passem here, they beg")

                                action = input("Will you give them the wings? ")

                                if action.lower() in game_constants.yesses:
                                    print("You give them the wings, and while they are pacified quickly run away.")
                                else:
                                    action = input(
                                        "You ask them what they can give you, and they offer the N-Word pass. Do you "
                                        "take it? ")

                                    if action.lower() in game_constants.yesses:
                                        print(
                                            "They hand you a slick looking business card, clearly labeled "
                                            "'N-Word-Pass', and apoligize for the problem they caused.")
                                    else:
                                        print(
                                            "They start screaming and tearing at each others' hair, until most of them "
                                            "are a pulp of black flesh and blood.")
                                        thugs -= 20
                                        if thugs < 0:
                                            thugs = 0
                    elif action == "rizz":
                        words = input("What's your pickup line? ")
                        success = random.choice([True, False])

                        if (success and not len(words) < random.randint(0, 8)) \
                                or ("chicken" in words or "kfc" in words):
                            print("Nice, line! You got rizz, can we go on a date they ask, you say yes and get married")
                        else:
                            print("They fuck you up, you got no rizz")

        elif choice == "talk":
            words = input("What will you say? ")

            print(f"You tell the thugs '{words}'")

            if "thug" in words.lower():
                print("Yo, fag you can't call us that! the thugs yell, then proceed to bash you")
            else:
                print("Give us yo chicken wings")
                time.sleep(2)
                wings = random.randint(0, 2)
                print(f"You have {wings}! You tell the thugs.")

                if wings == 0:
                    print("Aight, well have to kill you then.")
                else:
                    print("Passem here, they beg")

                    action = input("Will you give them the wings? ")

                    if action.lower() in game_constants.yesses:
                        print("You give them the wings, and while they are pacified quickly run away.")
                    else:
                        action = input(
                            "You ask them what they can give you, and they offer the N-Word pass. Do you take it? ")

                        if action.lower() in game_constants.yesses:
                            print(
                                "They hand you a slick looking business card, clearly labeled 'N-Word-Pass', and "
                                "apoligize for the problem they caused.")
                        else:
                            print(
                                "They start screaming and tearing at each others' hair, until most of them are a pulp "
                                "of black flesh and blood.")
                            thugs -= 20
                            if thugs < 0:
                                thugs = 0
        elif choice == "fight":
            health = 10
            while health > 0:
                time.sleep(1)
                damage = random.randint(0, 5)
                print(f"The thugs attack you for {damage} damage")
                health -= damage
                print(f"You have {health} left!")

                damage = random.randint(0, 2)
                thugs -= damage
                print(f"You kill {damage} thugs, there are {thugs} left!")

            print("You died! They loot your body and run away")

        elif choice == "rizz":
            words = input("What's your pickup line? ")
            success = random.choice([True, False])

            if success and not len(words) < random.randint(0, 7):
                print("Nice, line! You got rizz, can we go on a date they ask, you say yes and get married")
            else:
                print("They fuck you up, you got no rizz")
