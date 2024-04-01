import random
import sys
from word2number import w2n
from num2words import num2words as n2w

from blessed import Terminal
from bin.local_games import game_constants
from colorama import Fore, Back, Style


class Dungeon:
    def __init__(self):
        self.term = Terminal()
        self.run = True

        # Tiles
        self.gold_t = f'{Style.RESET_ALL}{Fore.YELLOW}{Style.BRIGHT}G'
        self.floor_t = f'{Style.RESET_ALL}{Style.DIM}.'

        # Map dimensions
        self.map_width = 44
        self.map_height = 22

        # Params
        self.history = []
        self.players_colors = ((Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE),
                               (Back.GREEN, Back.CYAN, Back.MAGENTA, Back.BLUE))
        self.player_t = "@"
        self.wall_color = None
        self.scores = None
        self.lives = None
        self.number_of_players = None
        self.players_x = None
        self.players_y = None
        self.treasures_pos = None
        self.map_style = None
        self.skeleton_name = None
        self.zombie_name = None
        self.wall_name = None
        self.skeleton_t = None
        self.zombie_t = None
        self.wall_t = None
        self.legend = None
        self.num_zombies = None
        self.num_skeletons = None
        self.map_data = None
        self.zombies = None
        self.skeletons = None

    def player_glyph(self, index: int, fore: bool = True):
        return f"{Style.RESET_ALL}{self.players_colors[not fore][index]}{Style.BRIGHT}{self.player_t}{Style.RESET_ALL}"

    def update_player_scores(self):
        for i in range(self.number_of_players):
            del self.legend[-1]

        for i in range(self.number_of_players):
            self.legend.append(f"{self.player_glyph(i)} : Player {n2w(i + 1)}'s score is {self.scores[i]}")

    def play(self):
        game_constants.clean_formatting()
        game_constants.clear_screen()

        self.number_of_players = game_constants.question("How many players? ",
                                                         ["one", "two", "three", "four", "quit"],
                                                         convert_words_to_numbers=False)
        if self.number_of_players.startswith("q"):
            self.run = False

        self.number_of_players = w2n.word_to_num(self.number_of_players)
        self.scores = [0 for __ in range(self.number_of_players)]

        while self.run:
            self.generate_dungeon()

            # Game loop
            while self.run:
                if self.run_frame():
                    break

            if self.run:
                again = input(f"{Fore.MAGENTA}Do you want to play again?{Fore.BLUE} ")

                if again.lower() not in game_constants.yesses:
                    break

    def generate_dungeon(self):
        self.history = []
        self.lives = [1 for __ in range(self.number_of_players)]

        # Map choice
        self.map_style = random.choice(("dungeon", "forest", "cave"))
        self.skeleton_name = "skeleton" if self.map_style == "dungeon" \
            else "spider" if self.map_style == "forest" else "kobold"
        self.zombie_name = "zombie" if self.map_style == "dungeon" \
            else "werewolf" if self.map_style == "forest" else "rat"
        self.wall_name = "wall" if self.map_style == "dungeon" else "tree" if self.map_style == "forest" else "dirt"
        self.wall_t = "#" if self.wall_name == "wall" else "%" if self.wall_name == "tree" else "#"
        self.wall_color = f"{Style.RESET_ALL}{Back.WHITE}{Style.DIM}" if self.wall_name == "wall" \
            else f"{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}" if self.wall_name == "tree" \
            else f"{Style.RESET_ALL}{Back.BLACK}{Style.DIM}"
        self.skeleton_t = f"{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{self.skeleton_name[0].upper()}{self.wall_color}"
        self.zombie_t = f"{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{self.zombie_name[0].upper()}{self.wall_color}"

        # Legend
        self.legend = [
            f"{Style.BRIGHT}      ===  RULES  === {Style.RESET_ALL}",
            f"{self.zombie_t}{Style.RESET_ALL} : {self.zombie_name.capitalize()}, they move up to",
            f"      one space orthogonally",
            f"{self.skeleton_t}{Style.RESET_ALL} : {self.skeleton_name.capitalize()}s move one",
            f"      space orthogonally or diagonally",
            f"{self.gold_t}{Style.RESET_ALL} : The golden treasure that",
            f"      you need to reach",
            f"{self.wall_color}{self.wall_t}{Style.RESET_ALL} : {self.wall_name.capitalize()}, cannot be moved",
            f"      through",
        ]

        for i in range(self.number_of_players):
            self.legend.append(f"{Style.RESET_ALL}{self.player_glyph(i)} : Player {n2w(i + 1)}'s score is 0")

        self.map_width = random.randint(22, 33)
        self.map_height = len(self.legend)

        # Player starting position
        self.players_x = [
            1, self.map_width - 2, 1, self.map_width - 2
        ]
        self.players_y = [
            1, self.map_height - 2, self.map_height - 2, 1
        ]
        self.players_x = self.players_x[:self.number_of_players]
        self.players_y = self.players_y[:self.number_of_players]

        # Make map
        # Treasure position
        self.treasures_pos = [(random.randint(1, self.map_width - 2), random.randint(1, self.map_height - 2))
                              for __ in range(int(self.number_of_players * 3.5))]

        # Number of self.zombies
        self.num_zombies = max(random.randint(-2, 2) + int((self.map_height * self.map_width) / 45), 1)
        self.num_skeletons = max(random.randint(-2, 2) + int((self.map_height * self.map_width) / 65), 1)

        # Generate random map
        self.map_data = []
        for __ in range(self.map_height):
            self.map_data.append([self.floor_t] * self.map_width)

        # Add walls to the map
        for x in range(0, self.map_width):
            for y in range(0, self.map_height):
                if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
                    self.map_data[y][x] = self.wall_t
                elif random.randint(0, 3) == 0 \
                        and (x, y) != (1, 1) \
                        and (x, y) != (1, self.map_height - 2) \
                        and (x, y) != (self.map_width - 2, 1) \
                        and (x, y) != (self.map_width - 2, self.map_height - 2) \
                        and (x, y) not in self.treasures_pos:
                    self.map_data[y][x] = self.wall_t

        # Add self.zombies to the map
        self.zombies = []
        for __ in range(self.num_zombies):
            x = random.randint(1, self.map_width - 2)
            y = random.randint(1, self.map_height - 2)
            if (x, y) != (1, 1) and (x, y) != (1, self.map_height - 2) and (x, y) != (self.map_width - 2, 1) \
                    and (x, y) != (self.map_width - 2, self.map_height - 2) and (x, y) not in self.treasures_pos:
                self.zombies.append((x, y))
                self.map_data[y][x] = self.zombie_t
            else:
                self.num_zombies -= 1

        # Add self.skeletons to the map
        self.skeletons = []
        for _ in range(self.num_skeletons):
            x = random.randint(1, self.map_width - 2)
            y = random.randint(1, self.map_height - 2)
            if (x, y) != (1, 1) and (x, y) != (1, self.map_height - 2) and (x, y) != (self.map_width - 2, 1) \
                    and (x, y) != (self.map_width - 2, self.map_height - 2) and (x, y) not in self.treasures_pos:
                self.skeletons.append((x, y))
                self.map_data[y][x] = self.skeleton_t
            else:
                self.num_skeletons -= 1

    def run_frame(self):
        # Clear the console screen
        self.draw_game()

        # Check for treasure
        for i in range(self.number_of_players):
            for j in range(len(self.treasures_pos)):
                if (self.players_x[i], self.players_y[i]) == self.treasures_pos[j]:
                    self.history.append(f"{Style.RESET_ALL}{Fore.YELLOW}Congratulations! Player {n2w(j + 1)} found a "
                                        f"treasure hoard!")
                    self.scores[i] += 1
                    self.treasures_pos[j] = None

        self.treasures_pos = [pos for pos in self.treasures_pos if pos is not None]

        # Check for self.zombies
        for i in range(self.num_zombies):
            zombie_x, zombie_y = self.zombies[i]
            for j in range(self.number_of_players):
                if self.players_x[j] == zombie_x and self.players_y[j] == zombie_y:
                    self.history.append(f"{Style.RESET_ALL}{Fore.RED}Player {n2w(j + 1)} has been captured by a "
                                        f"{self.zombie_name}!")
                    self.scores[j] = 0
                    self.lives[j] = 0

        # Check for self.skeletons
        for i in range(self.num_skeletons):
            skeleton_x, skeleton_y = self.skeletons[i]
            for j in range(self.number_of_players):
                if self.players_x[j] == skeleton_x and self.players_y[j] == skeleton_y:
                    self.history.append(f"{Style.RESET_ALL}{Fore.RED}Player {n2w(j + 1)} has been captured by a "
                                        f"{self.skeleton_name}!")
                    self.scores[j] = 0
                    self.lives[j] = 0

        # Get player input
        generated_new_dungeon = False
        for i in range(self.number_of_players):
            if generated_new_dungeon:
                break

            if self.lives[i]:
                self.draw_game(turn=i)
                while self.run:
                    with self.term.cbreak():
                        move = self.term.inkey()
                        moved = False

                        # Update player position
                        if move == "w" and self.players_y[i] > 0 \
                                and self.map_data[self.players_y[i] - 1][self.players_x[i]] \
                                not in (self.zombie_t, self.skeletons, self.player_t, self.wall_t):
                            self.players_y[i] -= 1
                            moved = True
                        elif move == "a" and self.players_x[i] > 0 \
                                and self.map_data[self.players_y[i]][self.players_x[i] - 1] \
                                not in (self.zombie_t, self.skeletons, self.player_t, self.wall_t):
                            self.players_x[i] -= 1
                            moved = True
                        elif move == "s" and self.players_y[i] < self.map_height - 1 \
                                and self.map_data[self.players_y[i] + 1][self.players_x[i]] \
                                not in (self.zombie_t, self.skeletons, self.player_t, self.wall_t):
                            self.players_y[i] += 1
                            moved = True
                        elif move == "d" and self.players_x[i] < self.map_width - 1 \
                                and self.map_data[self.players_y[i]][self.players_x[i] + 1] \
                                not in (self.zombie_t, self.skeletons, self.player_t, self.wall_t):
                            self.players_x[i] += 1
                            moved = True
                        elif move == "q":
                            self.run = False
                        elif move == "r":
                            if self.scores[i] != 0:
                                self.scores[i] -= 1
                            self.generate_dungeon()
                            self.history.append(f"{Style.RESET_ALL}{Fore.MAGENTA}Player {n2w(i + 1)} rerolled the "
                                                f"dungeon.")
                            generated_new_dungeon = True
                            self.draw_game()

                        if moved:
                            break

        # Move self.zombies randomly
        for i in range(self.num_zombies):
            zombie_x, zombie_y = self.zombies[i]
            if random.randint(0, 1):
                dx = random.randint(-1, 1)
                dy = random.randint(0, 0)
            else:
                dx = random.randint(0, 0)
                dy = random.randint(-1, 1)
            if (
                    0 <= zombie_x + dx < self.map_width
                    and 0 <= zombie_y + dy < self.map_height
                    and self.map_data[zombie_y + dy][zombie_x + dx] != self.wall_t
            ):
                self.map_data[zombie_y][zombie_x] = self.floor_t
                self.zombies[i] = (zombie_x + dx, zombie_y + dy)
                self.map_data[zombie_y + dy][zombie_x + dx] = self.zombie_t

        # Move self.skeletons randomly
        for i in range(self.num_skeletons):
            skeleton_x, skeleton_y = self.skeletons[i]
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            if (
                    0 <= skeleton_x + dx < self.map_width
                    and 0 <= skeleton_y + dy < self.map_height
                    and self.map_data[skeleton_y + dy][skeleton_x + dx] != self.wall_t
            ):
                self.map_data[skeleton_y][skeleton_x] = self.floor_t
                self.skeletons[i] = (skeleton_x + dx, skeleton_y + dy)
                self.map_data[skeleton_y + dy][skeleton_x + dx] = self.skeleton_t

        if len(self.treasures_pos) == 0:
            print(f"{Style.RESET_ALL}{Fore.YELLOW}Congratulations! All of the treasure has been collected.")
            return True

        found_alive = 1 in self.lives
        if not found_alive:
            print(f"{Style.RESET_ALL}{Fore.RED}All players have been killed... failure")
            return True

        return False

    def draw_game(self, turn=None):
        game_constants.clean_formatting()
        game_constants.clear_screen()
        self.update_player_scores()

        # Draw the map
        print("\n")
        legend_index = 0
        buffer = []
        for y in range(self.map_height):
            row = f"  {self.wall_color}"
            for x in range(self.map_width):
                if (x, y) in self.zombies:
                    row += self.zombie_t
                elif (x, y) in self.skeletons:
                    row += self.skeleton_t
                elif (x, y) in list(zip(self.players_x, self.players_y)):
                    for i in range(self.number_of_players):
                        if x == self.players_x[i] and y == self.players_y[i]:
                            if turn is not None and i == turn:
                                row += f"{self.player_glyph(i, False)}{self.wall_color}"
                            else:
                                row += f"{self.player_glyph(i)}{self.wall_color}"
                elif (x, y) in self.treasures_pos:
                    row += f"{self.gold_t}{self.wall_color}"
                elif self.map_data[y][x] == self.wall_t:
                    try:
                        if self.map_data[y][x - 1] != self.wall_t or x == 0:
                            row += f"{self.wall_color}{self.wall_t}"
                        else:
                            row += self.wall_t
                    except:
                        row += f"{self.wall_color}{self.wall_t}"
                else:
                    row += self.floor_t
            if legend_index < len(self.legend):
                row += f"{Style.RESET_ALL}  {self.legend[legend_index] if legend_index < len(self.legend) else ''}"
            legend_index += 1
            buffer.append(row)
        print("\n".join(buffer))
        print()

        print(f"{Style.RESET_ALL}{Fore.YELLOW}WASD{Fore.RESET} to move, {Fore.YELLOW}R{Fore.RESET} to shuffle dungeon "
              f"& lose a coin, {Fore.YELLOW}Q{Fore.RESET} to quit.")

        for i in range(min(3, len(self.history))):
            try:
                print(self.history[-i])
            except IndexError:
                pass


def run():
    dungeon = Dungeon()
    dungeon.play()
