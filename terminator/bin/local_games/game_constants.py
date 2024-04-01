import getpass
import os
import questionary as qy
from word2number import w2n
from num2words import num2words as n2w

from colorama import Fore, Back, Style


yesses = (
    "ye", "y", "yea", "yeah", "yes", "ya", "yah", "ys",
    "ok", "okay", "oky", "k", "kay",
    "sure", "suree", "for sure",
    "yep", "yp", "yippie",
    "aight", "alright",
    "def", "definitely"
)


def clean_formatting():
    print(Style.RESET_ALL, end="")


def clear_screen():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')


def answers_printable(answers: list):
    return f"[{'|'.join(answers)}]"


def input_error(message: str) -> str:
    return f"{Style.RESET_ALL}{Back.RED}Bad input! {message}{Style.RESET_ALL}"


def question(text: str, answers: list, shortenable: int = 2, secret: bool = False, remove_space: bool = False,
             keyword: str = "", convert_words_to_numbers: bool = True, convert_numbers_to_words: bool = True) -> str:
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

        try:
            if convert_words_to_numbers and str(w2n.word_to_num(answer)) in answers:
                return str(w2n.word_to_num(answer))
        except:
            pass

        try:
            if convert_numbers_to_words and str(n2w(answer)) in answers:
                return str(n2w(answer))
        except:
            pass

        if answer in answers or (answer == keyword and keyword != ""):
            return answer
        elif shortened_inputs.get(answer) is not None:
            return shortened_inputs.get(answer)
        else:
            print(f"{Back.RED}Bad input! choose from {answers_printable(answers)}")


def ask(text: str, length: tuple = (), secret: bool = False, password: bool = False,
        remove_space: bool = False, new_lined: bool = False, silent: bool = False):
    length = (length[0] - 1, length[1] + 1)
    end_of_line = "\n" if new_lined else " "
    while True:
        if silent:
            answer = input(f"{Style.RESET_ALL}").strip().lower()
        elif secret:
            answer = getpass.getpass(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                     f"{Style.RESET_ALL}{Fore.YELLOW}").strip().lower()
        elif password:
            answer = qy.password(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                 f"{Style.RESET_ALL}{Fore.YELLOW}").ask().strip().lower()
        else:
            answer = input(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                           f"{Style.RESET_ALL}{Fore.YELLOW}").strip().lower()

        if remove_space:
            answer = answer.replace(" ", "").replace("\t", "")

        if length[1] > len(answer) > length[0]:
            clean_formatting()
            return answer
        else:
            print(input_error(f"must be between {length[0] + 1} and {length[1] - 1} characters long"))
