import sys
import subprocess
import colorama
import os
import pickle
import getpass
import threading
import requests
import random
from word2number import w2n
from datetime import datetime
import questionary as qy

from bin.local_games import attack
from bin.local_games import connect_four
from bin.local_games import rock_paper_scissors
from bin.local_games import rogue
from bin.local_games import snake
from bin.local_games import simon_says
from bin.local_games import number_guesser
from bin.local_games import wordle
from bin.user_utils import *
from bin.server import Server
from bin.client import Client
from colorama import Fore, Back, Style


class Terminal:
    def __init__(self):
        self.state = "local"  # can be local, server, client
        self.server_thread = None

        with open(os.path.join("build", "account.pkl"), "rb") as file:
            self.account = pickle.load(file)

        with open(os.path.join("build", "settings.pkl"), "rb") as file:
            self.settings = pickle.load(file)

        self.commands = {
            "local": (
                "/help", "/?", "/party", "/join", "/exit", "/settings", "/clear", "/format", "/badjoke", "/joke",
                "/play", "/games", "/update"
            ),
            "client": (
                "/help", "/?", "/post", "/image", "/view", "/audio", "/listen", "/challenge", "/leave", "/download",
                "/games", "/exit"
            ),
            "server": (
                "/help", "/?", "/kick", "/ban", "/pardon", "/close"
            )
        }

        self.commands_help = {
            "local": {
                f"{self.command('/help')}": "Displays this help page, which explains the use of each command.",
                f"{self.command('/?')}": f"Same as {self.command('/help')}.",
                f"{self.command('/party')} -{self.parameter('[name]')}":
                    f"Creates a party server, which others can then join. {self.parameter('[name]')} is what you want "
                    f"to name it.",
                f"{self.command('/join')} -{self.parameter('[code]')}":
                    f"Join the corresponding party server for the {self.parameter('[code]')}.",
                f"{self.command('/exit')} -{self.parameter('[g/f]')}":
                    f"Ends the execution of Terminator, closing the program. If {self.parameter('[g]')} is specified "
                    f"it will save before exiting gracefully. If {self.parameter('[f]')} is specified it will force "
                    f"shutdown the program, without saving.",
                f"{self.command('/settings')}": "Opens the app and account settings page.",
                f"{self.command('/clear')}": "Clears the terminal and moves cursor back to the top.",
                f"{self.command('/format')}":
                    "Resets the formatting at the position of the cursor. Can be helpful if things have started "
                    "looking funny.",
                f"{self.command('/badjoke')} -{self.parameter('[chuck/yo]')}":
                    f"Tells you a joke on the topic you chose in the parameter: {self.parameter('[chuck/yo]')}. If you "
                    f"choose chuck it will be a joke about Chuck Norris (requires an internet connection). If you "
                    f"choose yo it will be a joke about Yo Mama (doesn't use internet, because yo mama's living the "
                    f"1600's).",
                f"{self.command('/joke')} -{self.parameter('[category]')} -{self.parameter('[blacklist]')} "
                f"-{self.parameter('[find]')}":
                    f"Fetches a joke from the internet. {self.parameter('[category]')} can be any, programming, misc, "
                    f"dark, pun, spooky, or christmas. {self.parameter('[blacklist]')} can be none, nsfw, religious, "
                    f"political, racist, sexist, or explicit and will stop jokes of that type appearing, none is "
                    f"default. {self.parameter('[find]')} is a word, or sentence that you want to appear in the joke, "
                    f"if you choose something too specific you might not get a joke at all though.",
                f"{self.command('/play')} -{self.parameter('[game]')}":
                    f"Starts a game on the local computer. Run {self.command('/games')} to view the choices.",
                f"{self.command('/games')}":
                    "Lists the names of the games that you can play locally, as well as gives a summary of them.",
                f"{self.command('/update')}": "Updates the app, you need an internet connection for it to work."
            },
            "client": {
                f"{self.command('/help')}": "Displays this help page, which explains the use of each command.",
                f"{self.command('/?')}": f"Same as {self.command('/help')}.",
                f"{self.command('/post')} -{self.parameter('[message]')}":
                    f"Sends your {self.parameter('[message]')} to everyone in the party.",
                f"{self.command('/image')}":
                    f"Opens up your file-explorer and lets you choose an image to post to the chat.",
                f"{self.command('/view')} -{self.parameter('[name]')}":
                    f"Opens up the image with the name {self.parameter('[name]')} from the chat in your default image "
                    f"app.",
                f"{self.command('/audio')}":
                    f"Opens up your file-explorer and lets you choose an audio file to post to the chat.",
                f"{self.command('/listen')} -{self.parameter('[name]')}":
                    f"Plays the audio file with the name {self.parameter('[name]')}.",
                f"{self.command('/challenge')} -{self.parameter('[game]')} -{self.parameter('[usernames]')}":
                    f"Plays the {self.parameter('[game]')} after asking every player in the list of "
                    f"{self.parameter('[usernames]')} if they accept the request.",
                f"{self.command('/leave')} -{self.parameter('[s/n]')}":
                    f"Disconnects from the party, if {self.parameter('s')} is chosen it will not notify the other "
                    f"party members, otherwise it will.",
                f"{self.command('/download')} -{self.parameter('[name]')}":
                    f"Downloads the file with {self.parameter('[name]')} from the chat, opens file-explorer for you to "
                    f"choose where to save it.",
                f"{self.command('/games')}":
                    "Lists the names of the games that you can play online, as well as gives a summary of them.",
                f"{self.command('/exit')} -{self.parameter('[g/f]')}":
                    f"Ends the execution of Terminator, closing the program. If {self.parameter('[g]')} is specified "
                    f"it will save before exiting gracefully. If {self.parameter('[f]')} is specified it will force "
                    f"shutdown the program, without saving.",
            },
            "server": {
                f"{self.command('/help')}": "Displays this help page, which explains the use of each command.",
                f"{self.command('/?')}": f"Same as {self.command('/help')}.",
                f"{self.command('/kick')} -{self.parameter('[reason]')}":
                    f"Opens up a list of currently connected users and lets you select which ones to kick, telling "
                    f"each one the {self.parameter('[reason]')}. They can immediately rejoin afterwards.",
                f"{self.command('/ban')} -{self.parameter('[reason]')}":
                    f"Opens up a list of currently connected users and lets you select which ones to ban, telling "
                    f"each one the {self.parameter('[reason]')}. Banning a user stops them from ever connecting again.",
                f"{self.command('/pardon')}":
                    f"Opens up a list of currently banned users and lets you choose which ones to un-ban.",
                f"{self.command('/close')}": f"Ends the party, notifying all connected members.",
            }
        }
        self.games = {
            "local": {
                f"{self.command('donsol')}": "A strategy card game about beating a dungeon.",
                f"{self.command('pof')}": "Pathways Of Fater, a choose your own adventure game in the terminal.",
                f"{self.command('ng')}": "Guess the number between 1 and 100.",
                f"{self.command('rps')}":
                    "Rock-Paper-Scissors, with local multiplayer up to three players, and vs. computer mode. Includes "
                    "normal, Star Trek, mega, and ultra versions.",
                f"{self.command('attack')}": "A poorly made choose your own adventure game, proceed with caution.",
                f"{self.command('4')}": "Simple, text-based connect four game.",
                f"{self.command('dd')}":
                    "Dig-Dug, an obscure arcade game by G.G.Otto about mining in zombie-infested caves.",
                f"{self.command('pacman')}":
                    "Two-player pacman. Ghostman uses arrows, Pacman uses WASD. If Pacman gets 85 or more points he "
                    "wins, but if he dies thrice, then Ghostman wins instead.",
                f"{self.command('pong')}": "Classic pong game.",
                f"{self.command('rogue')}":
                    "A simplistic dungeon-crawler where you have to get to the treasure while weaving through enemies.",
                f"{self.command('snake')}": "Terminal-based snake game, you won't win.",
                f"{self.command('life')}": "A multiplayer Conway's Game Of Life, press space to pause.",
                f"{self.command('simon')}": "Like Bop-It, color memory game.",
                f"{self.command('wordle')}": "Wordle, guess the five-letter word, like Master Mind but easier."
            }
        }
        self.server = Server(self)
        self.client = Client(self)

    def run(self):
        colorama.init(autoreset=True, strip=not self.settings["allow coloring"])
        ui.clear_screen()

        print(f"\n{Fore.RED} _____  ____ _____  __  __  _  __  _   ____  _____  ____ _____ \n{Fore.RED}|_   _|| ===|| ("
              f") )|  \\/  || ||  \\| | / () \\|_   _|/ () \\| () )\n{Fore.RED}  |_|  |____||_|\\_\\|_|\\/|_||_||_|\\__"
              f"|/__/\\__\\ |_|  \\____/|_|\\_\\\n{Fore.RED}                                                 "
              f"{Fore.RESET}-{Fore.BLUE}Python{Fore.YELLOW}Bear{Style.RESET_ALL}\n\n")

        while True:
            command = ui.command(
                self.command_prompt(),
                self.commands["client"] if self.state == "client"
                else self.commands["server"] if self.state == "server"
                else self.commands["local"]
            )

            if command.startswith("/exit"):
                command = command.split("-")
                if command[-1] == "f":
                    sys.exit()
                elif command[-1] == "g":
                    break
            elif self.state == "local":
                if self.handle_local_command(command):
                    break
            elif self.state == "client":
                if self.handle_client_command(command):
                    break

        with open(os.path.join("build", "account.pkl"), "wb") as file:
            pickle.dump(self.account, file)

        with open(os.path.join("build", "settings.pkl"), "wb") as file:
            pickle.dump(self.settings, file)

    def handle_server_command(self, command: str) -> bool:
        if command.startswith("/help") or command.startswith("/?"):
            for key, val in self.commands_help["client"].items():
                print(f"{key}\t: {val}")
        elif command.startswith("/close"):
            self.state = "local"
            self.server.run = False
            self.server_thread.join()
        return False

    def handle_client_command(self, command: str) -> bool:
        if command.startswith("/help") or command.startswith("/?"):
            for key, val in self.commands_help["client"].items():
                print(f"{key}\t: {val}")
        elif command.startswith("/post"):
            self.client.write(f"{self.account['name']} : {command.split('-')[-1].strip()}")
        elif command.startswith("/leave"):
            self.state = "local"
            self.client.run = False

        base_command = command.split("-")[0].strip()
        if base_command in self.commands["local"] and base_command not in ("/help", "/?", "/join", "/party"):
            return self.handle_local_command(command)

        return False

    def handle_local_command(self, command: str) -> bool:
        if command.startswith("/help") or command.startswith("/?"):
            for key, val in self.commands_help["local"].items():
                print(f"{key}\t: {val}")
        elif command.startswith("/cl"):
            ui.clear_screen()
        elif command.startswith("/format"):
            print(Style.RESET_ALL, end="")
        elif command.startswith("/party"):
            self.state = "server"
            self.server.run = True
            self.server_thread = threading.Thread(target=self.server.start_server)
            self.server_thread.start()
        elif command.startswith("/join"):
            self.state = "client"
            self.client.run = True
            self.client.start_client()
        elif command.startswith("/exit"):
            command = [arg.strip() for arg in command.lower().split("-")]
            if command[-1] == "f":
                sys.exit()
            elif command[-1] == "g":
                return True
        elif command.startswith("/joke"):
            bad_command = False
            categories = ("any", "programming", "misc", "dark", "pun", "spooky", "christmas")
            blacklist_categories = ("none", "nsfw", "religious", "political", "racist", "sexist", "explicit")
            command = [arg.strip() for arg in command.lower().split("-")]
            if len(command) > 1:
                if command[1] not in categories:
                    print(ui.input_error(f"the category {self.command(command[1])} is not recognized as a joke "
                                         f"category name. It must be: {ui.answers_printable(categories)}"))
                    bad_command = True
                if len(command) > 2:
                    if command[2] not in blacklist_categories:
                        print(ui.input_error(f"the blacklist category {self.command(command[1])} is not recognized as "
                                             f"a blacklist category name. It must be: "
                                             f"{ui.answers_printable(blacklist_categories)}"))
                        bad_command = True
                else:
                    command.append("none")
            else:
                command.append("any")
                command.append("none")

            if len(command) < 4:
                command.append("")

            if not bad_command:
                args_question_mark = ""
                blacklist_flag = ""
                search_input = ""
                if command[2] != "none":
                    blacklist_flag = f"blacklistFlags={command[2]}"
                    args_question_mark = "?"
                if len(command[3]) != 0:
                    search_input = f"{'&' if args_question_mark == '?' else ''}contains={command[3]}"
                    args_question_mark = "?"
                url = f"https://v2.jokeapi.dev/joke/{command[1].capitalize()}{args_question_mark}{blacklist_flag}" \
                      f"{search_input}"

                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if not data["error"]:
                        if data["type"] == "twopart":
                            setup = data["setup".strip()]
                            ending = " " if setup.endswith("?") or setup.endswith(":") or setup.endswith("...") \
                                else ".. " if setup.endswith(".") \
                                else "..."
                            __ = input(f"    {data['setup']}{ending}")
                            print(f"    {data['delivery']}")
                        else:
                            print(f"    {data['joke']}")
                    else:
                        print(ui.input_error(f"failed to fetch a joke, error code {self.command(data['code'])}: "
                                             f"{self.command(data['additionalInfo'])}"))
                else:
                    print(ui.input_error(f"failed to fetch a joke from {self.command(url)}, error code "
                                         f"{self.command(str(response.status_code))}, check your internet connection, "
                                         f"otherwise the website might be down."))
        elif command.startswith("/badjoke"):
            command = [arg.strip() for arg in command.lower().split("-")]
            if command[-1] == "chuck":
                response = requests.get("https://api.chucknorris.io/jokes/random")

                if response.status_code == 200:
                    data = response.json()
                    joke = data["value"]
                    print(f"    {joke}")
                else:
                    print(ui.input_error(f"failed to fetch a Chuck Norris joke, error code "
                                         f"{self.command(str(response.status_code))}, check your internet connection, "
                                         f"otherwise the website might be down."))
            elif command[-1] == "yo":
                with open(os.path.join("lib", "yo_mama_jokes.txt"), "r", encoding="utf-8") as file:
                    joke = random.choice(file.read().splitlines())
                print(f"    {joke}")

            else:
                print(ui.input_error(f"the name {self.command(command[-1])} is not recognized as a joke category "
                                     f"name."))
        elif command.startswith("/settings"):
            choices = [
                f"{key} : {val}" for key, val in [*self.settings.items(), *self.account.items()]
            ]
            choices.remove(f"name : {self.account['name']}")
            choices[choices.index(f"plain name : {self.account['plain name']}")] = \
                f"name : {self.account['plain name']}"
            answers = qy.checkbox(
                "What settings do you want to change?",
                choices=choices
            ).ask()
            answers = [val.split(" : ")[0] for val in answers]
            if "name" in answers:
                self.account["plain name"] = ui.ask("What is your name?", (4, 30))
                self.account["name"] = f"{ui.rgb_fore(*self.account['color'])}{self.account['plain name']}" \
                                       f"{Style.RESET_ALL}"
            if "gender" in answers:
                self.account["gender"] = ui.choice("What is your gender?", ("male", "female"))
            if "color" in answers:
                self.account["color"] = ui.ask_color("What should your accounts color be?")
                self.account["name"] = f"{ui.rgb_fore(*self.account['color'])}{self.account['plain name']}" \
                                       f"{Style.RESET_ALL}"
            if "bio" in answers:
                self.account["bio"] = ui.ask("Write a short biography for yourself", (0, 300), new_lined=True)
            if "pic" in answers:
                self.account["pic"] = ui.ask('Choose one character for your profile pic', (1, 1))
            if "python exe" in answers:
                self.settings["python exe"] = ui.ask('What is the command for python.exe?', ("python", "python3"))
            if "allow coloring" in answers:
                self.settings["allow coloring"] = True if \
                    ui.choice("Do you want to allow terminal coloring (will require app restart)?",
                              ("yes", "no")) == "yes" else False
                return True

        elif command.startswith("/games"):
            for key, val in self.games["local"].items():
                print(f"{key}\t: {val}")
        elif command.startswith("/play"):
            command = [arg.strip() for arg in command.lower().split("-")]
            # try:
            if command[-1] == "donsol":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'donsol', 'main.py')}"]
                )
            elif command[-1] == "pof":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'pathways_of_fate', 'main.py')}"]
                )
            elif command[-1] == "rps":
                rock_paper_scissors.run()
            elif command[-1] == "simon":
                simon_says.run()
            elif command[-1] == "wordle":
                wordle.run()
            elif command[-1] == "ng":
                number_guesser.run()
            elif command[-1] == "attack":
                attack.run()
            elif command[-1] == "4":
                connect_four.ConnectFour().run()
            elif command[-1] == "dd":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'dig_dug.py')}"]
                )
            elif command[-1] == "pacman":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'pacman.py')}"]
                )
            elif command[-1] == "pong":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'pong.py')}"]
                )
            elif command[-1] == "rogue":
                rogue.run()
            elif command[-1] == "snake":
                snake.run()
            elif command[-1] == "life":
                subprocess.call(
                    [self.settings['python exe'],
                     f"{os.path.join(os.path.abspath(os.getcwd()), 'bin', 'local_games', 'team_life.py')}"]
                )
            else:
                print(ui.input_error(f"the name {self.command(command[-1])} is not recognized as a game "
                                     f"name."))
            # except:
            #     pass

            print("\n")
            ui.clean_formatting()
        return False

    def command_prompt(self) -> str:
        return f"{self.account['pic']}{Style.RESET_ALL} | {self.account['name']}{Style.RESET_ALL} | " \
               f"{Fore.YELLOW}{datetime.now().strftime('%H:%M')}{Style.RESET_ALL} >"

    @staticmethod
    def command(text: str):
        return f"{Fore.CYAN}{text}{Fore.RESET}"

    @staticmethod
    def parameter(text: str):
        return f"{Fore.LIGHTGREEN_EX}{text}{Fore.RESET}"
