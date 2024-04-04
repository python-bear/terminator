import os
import getpass

import num2words
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

    def print_definition(self, data: dict):
        self.clean_formatting()
        print(self.style(data["word"], "title"))
        if len(data['phonetic']) != 0:
            print(
                f"{self.answers_printable([data['phonetic']] if isinstance(data['phonetic'], str) else data['phonetic'], Fore.BLUE)}")

        for i in range(len(data["meanings"])):
            print(self.style(data["meanings"][i]["partOfSpeech"].lower(), "subtitle"))

            for j in range(len(data["meanings"][i]["definitions"])):
                print(f"  {j + 1}. {data['meanings'][i]['definitions'][j]['definition']}")

                if data["meanings"][i]["definitions"][j].get("example", None) is not None:
                    print("    " + self.style(f"{data['meanings'][i]['definitions'][j]['example']}\n", "example"))
                print()

            for j in range(len(data["meanings"][i]["synonyms"])):
                if j == 0:
                    print("  " + self.style("synonyms", "subtitle"))
                print(f"    {j + 1}. {data['meanings'][i]['synonyms'][j]}")

            for j in range(len(data["meanings"][i]["antonyms"])):
                if j == 0:
                    print("  " + self.style("antonyms", "subtitle"))
                print(f"    {j + 1}. {data['meanings'][i]['antonyms'][j]}")
            print()

    def print_thesaurus(self, data: dict):
        self.clean_formatting()
        print(self.style(data["word"], "title"))

        for j in range(len(data["synonyms"])):
            if j == 0:
                print(self.style("synonyms", "subtitle"))
            if len(data['synonyms'][j]) != 0:
                print(f"  · {data['synonyms'][j]}")

        for j in range(len(data["antonyms"])):
            if j == 0:
                print(self.style("antonyms", "subtitle"))
            if len(data['antonyms'][j]) != 0:
                print(f"  · {data['antonyms'][j]}")
        print()

    def trivia(self, data) -> float:
        self.clean_formatting()
        question = data["question"].strip().split(" (")[0]
        ending = "" if question.endswith("?") or question.endswith(";") or question.endswith(":") \
                       or question.endswith(".") else "?"
        true_answer = self.strip_trivia_answer(data["answer"])
        answer = self.strip_trivia_answer(self.input(f"  {question}{ending} "))
        if answer == true_answer:
            print("    Yes!")
            return 1
        elif (answer in true_answer or true_answer in answer) and len(answer) > 3:
            print(f"    Sort of, {data['answer']}")
            return 0.5
        else:
            print(f"    No, {data['answer']}")
            return 0

    def strip_trivia_answer(self, text: str) -> str:
        return self.full_lstrip(self.full_lstrip(self.full_lstrip(
            self.replace_words_with_numbers(
                text.lower().replace("'", "").replace('"', "").strip().replace("  ", " ").replace("\t", " ")
            ).replace("one ", " ").replace("-", " ").replace(",", "").replace(".", "").replace(":", "").replace(":", "")
            .replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")
            .replace("!", "").replace("?", "").replace("~", "").replace("_", "").replace("#", "").replace(" an ", " ")
            .replace(" the ", " ").replace(" & ", " and ").rstrip("s").replace(" ", ""), "and"), "an"), "the")

    @staticmethod
    def replace_words_with_numbers(text: str) -> str:
        final_text = ""
        text = text.split(" ")

        for word in text:
            try:
                final_text += num2words.num2words(float(word))
            except:
                final_text += f"{word} "

        return final_text.strip()

    @staticmethod
    def full_lstrip(s: str, substring: str) -> str:
        if s.startswith(substring):
            return s[len(substring):]
        return s

    @staticmethod
    def str_to_float(text: str) -> float:
        try:
            return float(text)
        except:
            try:
                return float(w2n.word_to_num(text))
            except:
                return None

    @staticmethod
    def str_to_int(text: str) -> int:
        try:
            return int(text)
        except:
            try:
                return w2n.word_to_num(text)
            except:
                return None

    @staticmethod
    def print_quote(data):
        print(f"  \"{data['quote']}\"")
        print(f"{Style.DIM}    - {data['author']}")

    @staticmethod
    def input_error(message: str) -> str:
        return f"{Style.RESET_ALL}{Back.RED}Bad input! {message}{Style.RESET_ALL}"

    @staticmethod
    def answers_printable(answers: tuple, fore_color: str = None) -> str:
        join_link = f"{Fore.RESET}|{fore_color if fore_color is not None else ''}"
        return f"[{fore_color if fore_color is not None else ''}{join_link.join(answers)}{Fore.RESET}]"

    @staticmethod
    def rgb_fore(r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def rgb_back(r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"

    @staticmethod
    def style(text: str, form: str):
        if form == "title":
            return f"\n{Style.BRIGHT} ===  {text.strip().upper()}  === {Style.RESET_ALL}"
        elif form == "subtitle":
            return f"{Style.BRIGHT}:: {text.strip()} :: {Style.RESET_ALL}"
        elif form == "example":
            return f'{Style.DIM}"{text.strip()}"{Style.RESET_ALL}'

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
