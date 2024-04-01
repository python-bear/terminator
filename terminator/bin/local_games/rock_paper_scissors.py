import colorama
import random
import getpass

from colorama import Fore, Back


possible_actions = [
    ["rock", "scissors", "paper"],
    ["rock", "lizard", "spock", "clippers", "paper"],
    ["rock", "fire", "clippers", "sponge", "paper", "air", "water"],
    ["rock", "fire", "clippers", "snake", "human", "tree", "wolf", "sponge", "paper", "air", "water", "dragon", "devil",
     "lightning", "gun"]
]
emojis = {
    "scissors": "✂ ",
    "clippers": "✂ ",
    "rock": "🌑",
    "lightning": "⚡",
    "paper": "📃",
    "bomb": "💣",
    "fire": "🔥",
    "tree": "🌳",
    "water": "💧",
    "air": "💨",
    "devil": "😈",
    "snake": "🐍",
    "human": "😀",
    "wolf": "🐺",
    "dragon": "🐉",
    "gun": "🔫",
    "sponge": "🧽",
    "lizard": "🦎",
    "spock": "🖖",
    "scry": "🔮",
    "blackhole": "🕳 ",
}
player_colors = {
    "player one": f"{Fore.BLUE}player one{Fore.RESET}",
    "player two": f"{Fore.RED}player two{Fore.RESET}",
    "player three": f"{Fore.GREEN}player three{Fore.RESET}",
}
custom_win_logics = {
    1: {
        ("rock", "lizard"): 0,
        ("rock", "spock"): 1,
        ("rock", "clippers"): 0,
        ("rock", "paper"): 1,

        ("lizard", "rock"): 1,
        ("lizard", "spock"): 0,
        ("lizard", "clippers"): 1,
        ("lizard", "paper"): 0,

        ("spock", "lizard"): 1,
        ("spock", "rock"): 0,
        ("spock", "clippers"): 0,
        ("spock", "paper"): 1,

        ("clippers", "lizard"): 0,
        ("clippers", "spock"): 1,
        ("clippers", "rock"): 1,
        ("clippers", "paper"): 0,

        ("paper", "lizard"): 0,
        ("paper", "spock"): 1,
        ("paper", "clippers"): 0,
        ("paper", "rock"): 1,
    }
}
win_word = "scry"


def answers_printable(answers: list):
    return f"[{'|'.join(answers)}]"


def decide_winner(player_one: str, player_two: str, game_mode: int, player_three: str = None):
    if player_three is not None:
        return [
            decide_winner(player_one, player_two, game_mode) != 1 and
            decide_winner(player_one, player_three, game_mode) != 1,
            decide_winner(player_two, player_one, game_mode) != 1 and
            decide_winner(player_two, player_three, game_mode) != 1,
            decide_winner(player_three, player_one, game_mode) != 1 and
            decide_winner(player_three, player_two, game_mode) != 1
        ]

    if game_mode in custom_win_logics.keys():
        return custom_win_logics[game_mode][(player_one, player_two)]

    else:
        actions_count = len(possible_actions[game_mode])
        player_one_idx = possible_actions[game_mode].index(player_one)
        player_two_idx = possible_actions[game_mode].index(player_two)
        difference = (player_one_idx - player_two_idx) % actions_count

        if difference == 0:
            return 0
        elif difference <= actions_count // 2:
            return 1
        else:
            return 0


def question(text: str, answers: list, shortenable: int = 1, secret: bool = False, remove_space: bool = False,
             keyword: str = "") -> str:
    if shortenable == 1:
        shortened_inputs = {str(key[0]): key for key in answers}
    elif shortenable == 2:
        shortened_inputs = {str(key[:2]): key for key in answers}
    else:
        shortened_inputs = {}

    while True:
        if secret:
            answer = getpass.getpass(f"{text}{answers_printable(answers)} ").strip().lower()
        else:
            answer = input(f"{text}{answers_printable(answers)} ").strip().lower()

        if remove_space:
            answer = answer.replace(" ", "").replace("\t", "")

        if answer in answers or (answer == keyword and keyword != ""):
            return answer
        elif shortened_inputs.get(answer) is not None:
            return shortened_inputs.get(answer)
        else:
            print(f"{Back.RED}Bad input! choose from {answers_printable(answers)}")


def run():
    print("""


!   __            _     @   ___                       # __      _                        
!  /__\\ ___   ___| | __ @  / _ \\__ _ _ __   ___ _ __  #/ _\\ ___(_)___ ___  ___  _ __ ___ 
! / \\/// _ \\ / __| |/ / @ / /_)/ _` | '_ \\ / _ \\ '__| #\\ \\ / __| / __/ __|/ _ \\| '__/ __|
!/ _  \\ (_) | (__|   <  @/ ___/ (_| | |_) |  __/ |    #_\\ \\ (__| \\__ \\__ \\ (_) | |  \\__ \\
!\\/ \\_/\\___/ \\___|_|\\_\\ @\\/    \\__,_| .__/ \\___|_|    #\\__/\\___|_|___/___/\\___/|_|  |___/
!                       @           |_|               #                    $- PythonBear


""".replace("!", Fore.RED).replace("@", Fore.YELLOW).replace("#", Fore.BLUE).replace("$", Fore.WHITE) +
          f"""{Fore.BLUE}When prompted for input if multiple options start with the same letter then you can just type 
the first two letters, otherwise, if they don't, then you can just write the first letter.""")

    while True:
        print("")
        number_of_players = question("How many players? ", ["one", "two", "three", "quit"], 2)

        if number_of_players == "quit":
            break

        gamemode = question("What gamemode? ", ["normal", "star trek", "mega", "ultra"], 1)
        gamemode = 0 if gamemode == "normal" else 1 if gamemode == "star trek" else 2 if gamemode == "mega" else 3
        run_minigame = True
        turn = 1
        scores = [0, 0, 0]

        while run_minigame:
            if number_of_players == "three":
                print(f"{Back.YELLOW}PLAYER ONE: {scores[0]}, PLAYER TWO: {scores[1]}, PLAYER THREE: {scores[2]}")

                if turn % 3 == 0:
                    action_three = question(f"What is {player_colors['player three']}'s action? ",
                                            possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_two = question(f"What is {player_colors['player two']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_one = question(f"What is {player_colors['player one']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                elif turn % 3 == 1:
                    action_two = question(f"What is {player_colors['player two']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_one = question(f"What is {player_colors['player one']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_three = question(f"What is {player_colors['player three']}'s action? ",
                                            possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                else:
                    action_one = question(f"What is {player_colors['player one']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_three = question(f"What is {player_colors['player three']}'s action? ",
                                            possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                    action_two = question(f"What is {player_colors['player two']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, True, True, win_word)
                turn += 1

                if action_one == win_word and action_two != win_word and action_three != win_word:
                    action_one = possible_actions[gamemode][possible_actions[gamemode].index(action_two) - 1]

                elif action_two == win_word and action_one != win_word and action_three != win_word:
                    action_two = possible_actions[gamemode][possible_actions[gamemode].index(action_three) - 1]

                elif action_three == win_word and action_one != win_word and action_two != win_word:
                    action_three = possible_actions[gamemode][possible_actions[gamemode].index(action_one) - 1]

                print(f"{Fore.YELLOW}PLAYER ONE CHOSE {action_one.upper()} {emojis[action_one]} and PLAYER TWO CHOSE "
                      f"{action_two.upper()} {emojis[action_two]} and PLAYER THREE CHOSE {action_three.upper()} "
                      f"{emojis[action_three]}")

                if action_one == action_two == action_three:
                    print(f"{Fore.MAGENTA}THIS ROUND WAS A DRAW")
                elif [action_one, action_two, action_three].count("scry") > 1:
                    print(f"{Fore.MAGENTA}THIS ROUND WAS A DRAW")
                else:
                    winner = decide_winner(action_one, action_two, gamemode, action_three)
                    if 1 not in winner:
                        print(f"{Fore.MAGENTA}ALL PLAYERS LOST THIS ROUND")
                    else:
                        if winner[0]:
                            print(f"{Fore.BLUE}PLAYER ONE WINS THIS ROUND")
                            scores[0] += 1
                        if winner[1]:
                            print(f"{Fore.RED}PLAYER TWO WINS THIS ROUND")
                            scores[1] += 1
                        if winner[2]:
                            print(f"{Fore.GREEN}PLAYER THREE WINS THIS ROUND")
                            scores[2] += 1

                if scores[0] >= 3 and scores[1] >= 3 and scores[2] >= 3:
                    print(f"{Back.MAGENTA}THIS GAME WAS A THREE-WAY DRAW!")
                    run_minigame = False
                elif scores[0] >= 3 and scores[1] >= 3:
                    print(f"{Back.MAGENTA}THIS GAME WAS A DRAW BETWEEN PLAYER ONE AND TWO!")
                    run_minigame = False
                elif scores[0] >= 3 and scores[2] >= 3:
                    print(f"{Back.MAGENTA}THIS GAME WAS A DRAW BETWEEN PLAYER ONE AND THREE!")
                    run_minigame = False
                elif scores[1] >= 3 and scores[2] >= 3:
                    print(f"{Back.MAGENTA}THIS GAME WAS A DRAW BETWEEN PLAYER TWO AND THREE!")
                    run_minigame = False
                elif scores[0] >= 3:
                    print(f"{Back.BLUE}PLAYER ONE WINS THIS GAME!")
                    run_minigame = False
                elif scores[1] >= 3:
                    print(f"{Back.RED}PLAYER TWO WINS THIS GAME!")
                    run_minigame = False
                elif scores[2] >= 3:
                    print(f"{Back.GREEN}PLAYER THREE WINS THIS GAME!")
                    run_minigame = False
            else:
                print(f"{Back.YELLOW}PLAYER ONE: {scores[0]}, PLAYER TWO: {scores[1]}")

                if number_of_players == "one":
                    action_one = question(f"What is {player_colors['player one']}'s action? ",
                                          possible_actions[gamemode], 2 if gamemode == 3 else 1, keyword=win_word)
                    action_two = random.choice(possible_actions[gamemode])
                elif number_of_players == "two":
                    if turn % 2 == 0:
                        action_two = question(f"What is {player_colors['player two']}'s action? ",
                                              possible_actions[gamemode],
                                              2 if gamemode == 3 else 1, True, True, win_word)
                        action_one = question(f"What is {player_colors['player one']}'s action? ",
                                              possible_actions[gamemode],
                                              2 if gamemode == 3 else 1, True, True, win_word)
                    else:
                        action_one = question(f"What is {player_colors['player one']}'s action? ",
                                              possible_actions[gamemode],
                                              2 if gamemode == 3 else 1, True, True, win_word)
                        action_two = question(f"What is {player_colors['player two']}'s action? ",
                                              possible_actions[gamemode],
                                              2 if gamemode == 3 else 1, True, True, win_word)
                    turn += 1

                if action_one == win_word and action_two != win_word:
                    action_one = possible_actions[gamemode][possible_actions[gamemode].index(action_two) - 1]

                elif action_two == win_word and action_one != win_word:
                    action_two = possible_actions[gamemode][possible_actions[gamemode].index(action_one) - 1]

                print(f"{Fore.YELLOW}PLAYER ONE CHOSE {action_one.upper()} {emojis[action_one]} and PLAYER TWO CHOSE "
                      f"{action_two.upper()} {emojis[action_two]}")

                if action_one == action_two:
                    print(f"{Fore.MAGENTA}THIS ROUND WAS A DRAW")
                else:
                    winner = decide_winner(action_one, action_two, gamemode)
                    if winner == 0:
                        print(f"{Fore.BLUE}PLAYER ONE WINS THIS ROUND")
                        scores[0] += 1
                    elif winner == 1:
                        print(f"{Fore.RED}PLAYER TWO WINS THIS ROUND")
                        scores[1] += 1

                if scores[0] >= 3 and scores[1] >= 3:
                    print(f"{Back.MAGENTA}THIS GAME WAS A DRAW!")
                    run_minigame = False
                elif scores[0] >= 3:
                    print(f"{Back.BLUE}PLAYER ONE WINS THIS GAME!")
                    run_minigame = False
                elif scores[1] >= 3:
                    print(f"{Back.RED}PLAYER TWO WINS THIS GAME!")
                    run_minigame = False
