import os
import getpass
from word2number import w2n
import questionary as qy

from colorama import Fore, Back, Style


class Ui:
    def __init__(self):
        self.ansi = {
            "blinking": "\033[5m",
            "input": f"{Style.RESET_ALL}{Fore.YELLOW}"
        }
        self.max_line_length, __ = os.get_terminal_size()

    def choice(self, text: str, answers: tuple, secret: bool = False, password: bool = False,
               remove_space: bool = False, convert_words_to_numbers: bool = True, new_lined: bool = False):
        shortened_inputs = {str(key[:2]): key for key in answers}
        end_of_line = "\n" if new_lined else " "

        while True:
            if secret:
                answer = getpass.getpass(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}") \
                    .strip().lower()
            elif password:
                answer = qy.password(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}") \
                    .ask().strip().lower()
            else:
                answer = input(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}") \
                    .strip().lower()

            if remove_space:
                answer = answer.replace(" ", "").replace("\t", "")

            try:
                if convert_words_to_numbers and str(w2n.word_to_num(answer)) in answers:
                    self.clean_formatting()
                    return str(w2n.word_to_num(answer))
            except:
                pass

            if answer in answers:
                self.clean_formatting()
                return answer
            elif shortened_inputs.get(answer) is not None:
                self.clean_formatting()
                return shortened_inputs.get(answer)
            else:
                print(self.input_error(f"choose from {self.answers_printable(answers)}"))

    def ask(self, text: str, length: tuple = (), secret: bool = False, password: bool = False,
            remove_space: bool = False, new_lined: bool = False):
        length = (length[0] - 1, length[1] + 1)
        end_of_line = "\n" if new_lined else " "
        while True:
            if secret:
                answer = getpass.getpass(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                         f"{self.ansi['input']}").strip().lower()
            elif password:
                answer = qy.password(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                     f"{self.ansi['input']}").ask().strip().lower()
            else:
                answer = input(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                               f"{self.ansi['input']}").strip().lower()

            if remove_space:
                answer = answer.replace(" ", "").replace("\t", "")

            if length[1] > len(answer) > length[0]:
                self.clean_formatting()
                return answer
            else:
                print(self.input_error(f"must be between {length[0] + 1} and {length[1] - 1} characters long"))

    def ask_color(self, text: str):
        while True:
            answer = input(f"{text}[in hexadecimal format] {self.ansi['input']}") \
                .strip().lower().replace(" ", "").replace("\t", "")

            try:
                self.clean_formatting()
                return self.hex_to_rgb(answer)
            except:
                print(self.input_error(f"not a valid hex color code"))

    def input(self, text: str, secret: bool = False, password: bool = False,
              remove_space: bool = False, new_lined: bool = False):
        end_of_line = "\n" if new_lined else " "

        if secret:
            answer = getpass.getpass(f"{text}{end_of_line}{self.ansi['input']}").strip().lower()
        elif password:
            answer = qy.password(f"{text}{end_of_line}{self.ansi['input']}").ask().strip().lower()
        else:
            answer = input(f"{text}{end_of_line}{self.ansi['input']}").strip().lower()

        if remove_space:
            answer = answer.replace(" ", "").replace("\t", "")

        self.clean_formatting()
        return answer

    def command(self, text: str, commands: tuple):
        while True:
            print(text)
            answer = qy.autocomplete(
                "",
                choices=list(commands),
            ).ask().strip()

            found_command = False
            for command in commands:
                if answer.startswith(command):
                    found_command = True

            if found_command or answer == "":
                self.clean_formatting()
                return answer
            else:
                print(self.input_error(f"that is not a recognized command, run {Fore.CYAN}/help{Fore.RESET} for help"))

    @staticmethod
    def input_error(message: str) -> str:
        return f"{Style.RESET_ALL}{Back.RED}Bad input! {message}{Style.RESET_ALL}"

    @staticmethod
    def answers_printable(answers: tuple) -> str:
        return f"[{'|'.join(answers)}]"

    @staticmethod
    def rgb_fore(r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def rgb_back(r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"

    @staticmethod
    def style(text: str, form: str):
        if form == "title":
            return f"\n{Style.BRIGHT} ===  {text.upper()}  === {Style.RESET_ALL}\n"

    @staticmethod
    def hex_to_rgb(hex_string):
        return tuple(int(hex_string.strip('#')[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def clean_formatting():
        print(Style.RESET_ALL, end="")

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')

        else:
            os.system('clear')


ui = Ui()
