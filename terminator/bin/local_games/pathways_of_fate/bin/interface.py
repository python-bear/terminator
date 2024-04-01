import os
import sys
import time
import random
import colorama

from colorama import Fore, Style, Back
from bin.utils import linearize_text, is_float


colorama.init(autoreset=True)


class DisplayMachine:
    def __init__(self, world=None):
        self.world = world
        self.pause_time = 0.5
        self.max_line_len = 70
        self.do_screen_clearing = True
        self.prompts = {
            'question': f'{Fore.MAGENTA}?> {Fore.YELLOW}',
            'command': f'{Fore.MAGENTA}>> {Fore.YELLOW}'
        }

    def pause(self, low=1.0, high=1.0):
        time.sleep(random.uniform(low * self.pause_time, high * self.pause_time))

    def exit_program(self):
        self.display(question=(f'{Back.RED}Press enter to close the Pathways Of Fate program.', str),
                     alt_prompt=self.prompts['command'])
        sys.exit()

    def clear_screen(self):
        if self.do_screen_clearing:
            # Clear the screen for Windows
            if os.name == 'nt':
                _ = os.system('cls')

            # Clear the screen for Linux and Mac
            else:
                _ = os.system('clear')

    def display(self, input_string=None, table=None, options=None, question=None, title=None, ascii_image=None,
                card=None, alt_prompt=None):

        if title is not None:  # str
            mock_title = f'=== {title.upper()} ==='
            title_len = len(mock_title)
            title = f'{Fore.WHITE}=== {Style.BRIGHT}{title.upper()}{Style.RESET_ALL}{Fore.WHITE} ==='
            padding = ' ' * ((self.max_line_len - title_len) // 2)

            print(f'\n{padding}{title}{padding}\n')

        if input_string is not None:  # str
            if isinstance(input_string, str):

                lines = linearize_text(input_string, self.max_line_len)

                for line_index in lines:
                    print(f'  {line_index.strip(" ")} ')
                    self.pause(0.8, 2.9)

            else:
                for string in input_string:

                    lines = linearize_text(string, self.max_line_len)

                    for line_index in lines:
                        print(f'  {line_index.strip(" ")} ')
                        self.pause(0.8, 2.9)

        if ascii_image is not None:
            print(f'\n{ascii_image}')

        if card is not None:
            column_widths = [0, 0, 0, 0]
            rows = [[], [], [], []]

            for model in card:
                model_stamina = f'{model.calculate_total_attribute("stamina")}❤️'
                model_skill = f'{model.calculate_total_attribute("skill")}🗡️'
                model_luck = f'{model.calculate_total_attribute("luck")}🍀'

                name_len = len(model.name)
                stamina_len = len(str(model_stamina))
                skill_len = len(str(model_skill))
                luck_len = len(str(model_luck))

                if name_len > column_widths[0]:
                    column_widths[0] = name_len

                if stamina_len > column_widths[1]:
                    column_widths[1] = stamina_len

                if skill_len > column_widths[2]:
                    column_widths[2] = skill_len

                if luck_len > column_widths[3]:
                    column_widths[3] = luck_len

                rows[0].append(model.name)
                rows[1].append(str(model_stamina))
                rows[2].append(str(model_skill))
                rows[3].append(str(model_luck))

            for index in range(len(column_widths)):
                column_widths[index] += 2

            for index in range(len(rows[0])):
                row_str = ''

                for j in range(len(rows)):
                    row = rows[j][index].strip()
                    row_len = len(row)

                    cell_width = column_widths[j]
                    cell_padding = (cell_width - row_len) // 2

                    cell = f'{" " * cell_padding}{row}{" " * (cell_width - row_len - cell_padding)}'

                    if j == 0:
                        row_str += f'    |{Fore.CYAN}{cell}{Fore.RESET}'

                    elif j == len(rows) - 1:
                        row_str += f'|{cell}|'

                    else:
                        row_str += f'|{cell}'

                row_len = len(row_str) - len(f'{Fore.CYAN}{Fore.RESET}') - 2

                if index == 0:
                    print('   ', '-' * (row_len - 1))

                print(row_str)
                print('   ', '-' * (row_len - 1))

        if table is not None:  # ((column_1_row_1, column_1_row_2), (column_2_row_1, column_2_row_2))
            longest_column_one_length = 0

            for row in table[0]:
                if len(row) > longest_column_one_length:
                    longest_column_one_length = len(row)

            longest_column_one_length += 2  # adding padding

            for row in range(len(table[0])):
                column_one_mock = f'     [ {table[0][row]} ]'
                column_one_text_len = len(table[0][row])

                column_one_mock = f'{column_one_mock}{" " * (longest_column_one_length - column_one_text_len)}:  '
                column_one_len = len(column_one_mock)

                column_one = f'     [ {Fore.CYAN}{table[0][row]}{Fore.RESET} ]'
                column_one = f'{column_one}{" " * (longest_column_one_length - column_one_text_len)}:  '

                column_two = linearize_text(table[1][row], self.max_line_len - column_one_len)

                for line_index in range(len(column_two)):
                    if line_index == 0:
                        if len(column_two) == 1:
                            print(f'{column_one}{column_two[line_index]}\n')

                        else:
                            print(f'{column_one}{column_two[line_index]}')

                    elif line_index == len(column_two) - 1:
                        print(f'{" " * column_one_len}{column_two[line_index]}\n')

                    else:
                        print(f'{" " * column_one_len}{column_two[line_index]}')

                    self.pause(0.6, 2.2)

        if options is not None:
            # ((option_one, option_two, option_etc), (description_one, description_two, description_etc))
            self.display(' ')

            for index in range(len(options[0])):
                command_mock = f'     [ {options[0][index]} ]  :   '
                command = f'     [ {Fore.BLUE}{options[0][index]}{Fore.RESET} ]  :   '
                command_len = len(command_mock)

                description = linearize_text(options[1][index], self.max_line_len - command_len)

                for line_index in range(len(description)):
                    if line_index == 0:
                        print(f'{command}{description[line_index]}')

                    else:
                        print(f'{" " * command_len}{description[line_index]}')

                    self.pause(0.6, 2.2)

            if self.world is not None:
                return self.world.get_player_action(options[0]).upper()

            else:
                while True:
                    choice = input(f'{self.prompts["question"]}{Fore.YELLOW}').upper()
                    self.display(Style.RESET_ALL)

                    if choice in options[0]:
                        return choice

                    else:
                        print(f'   {Fore.RED}Invalid input{Fore.RESET}, you must choose from {options[0]}')

        if question is not None:  # (question_str, answer_format)
            self.display(' ')

            if alt_prompt is not None:
                question_prompt = alt_prompt

            else:
                question_prompt = self.prompts["question"]

            if question[0] is not None:
                question_context = linearize_text(question[0], self.max_line_len)
                self.display(question_context)

            while True:
                choice = input(f'{question_prompt}{Fore.YELLOW}')
                self.display(Style.RESET_ALL)

                if question[1] == str:
                    return choice

                elif question[1] == int:
                    if choice.isdigit():
                        return int(choice)

                    else:
                        print(f'   {Fore.RED}Invalid input{Fore.RESET}, you must input a whole number')

                if question[1] == float:
                    if is_float(choice):
                        return float(choice)

                    else:
                        print(f'   {Fore.RED}Invalid input{Fore.RESET}, you must input a number with decimal points')

        self.pause(1.5, 5)

    def roll_dice(self, roll_range=None, number_of_rolls=None, form='dice'):
        dice_rolls = []
        form_image = None

        if roll_range is None:
            if form == 'coin':
                roll_range = ['heads', 'tails']
            else:
                roll_range = [1, 6]

        if number_of_rolls is None:
            if form == 'coin':
                number_of_rolls = [1, ['coin flip']]
            else:
                number_of_rolls = [1, ['dice roll']]

        if form == 'dice':
            form_image = '🎲'

        elif form == 'coin':
            form_image = '⛀'

        for roll_index in range(number_of_rolls[0]):  # number_of_rolls = (number_of_rolls, (reason_for_roll))
            print(f'\n   {number_of_rolls[1][roll_index]} {form_image}: \n    ', end='')

            number_of_turn_overs = random.randint(1, 10)

            for turn_over in range(number_of_turn_overs):
                if turn_over == number_of_turn_overs - 1:
                    if form == 'coin':
                        dice_roll = random.choice(roll_range)

                    else:
                        dice_roll = random.randint(int(roll_range[0]), int(roll_range[1]))

                    print(f' {Style.BRIGHT}{dice_roll}')
                    self.pause(0.2, 2.0)

                    dice_rolls.append(dice_roll)

                else:
                    if form == 'coin':
                        print(f' {random.choice(roll_range)}', end='')

                    else:
                        print(f' {random.randint(int(roll_range[0]), int(roll_range[1]))}', end='')

                    self.pause(0.2, 0.5)
                    print('.', end='', flush=True)
                    self.pause(0.2, 0.4)
                    print('.', end='', flush=True)
                    self.pause(0.2, 0.5)
                    print('. ', end='', flush=True)
                    self.pause(0.2, 2.0)

        return dice_rolls
