import colorama
import os
import pickle
import getpass
from word2number import w2n
import questionary as qy

from colorama import Fore, Back, Style

colorama.init(autoreset=True)


class Ui:
    def __init__(self, allow_coloring: bool):
        self.allow_coloring = allow_coloring
        self.ansi = {
            "blinking": "\033[5m",
            "input": f"{Style.RESET_ALL}{Fore.YELLOW}"
        }

    def choice(self, text: str, answers: tuple, secret: bool = False, password: bool = False,
               remove_space: bool = False, convert_words_to_numbers: bool = True, new_lined: bool = False):
        shortened_inputs = {str(key[:2]): key for key in answers}
        end_of_line = "\n" if new_lined else " "

        while True:
            if secret:
                answer = getpass.getpass(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}")\
                    .strip().lower()
            elif password:
                answer = qy.password(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}")\
                    .ask().strip().lower()
            else:
                answer = input(f"{text}{self.answers_printable(answers)}{end_of_line}{self.ansi['input']}")\
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
                print(f"{Style.RESET_ALL}{Back.RED}Bad input! choose from {self.answers_printable(answers)}")

    def ask(self, text: str, length: tuple = (), secret: bool = False, password: bool = False,
            remove_space: bool = False, new_lined: bool = False):
        length = (length[0] - 1, length[1] + 1)
        end_of_line = "\n" if new_lined else " "
        while True:
            if secret:
                answer = getpass.getpass(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                         f"{self.ansi['input']}").strip()
            elif password:
                answer = qy.password(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                                     f"{self.ansi['input']}").ask().strip()
            else:
                answer = input(f"{text}[length between {length[0] + 1} and {length[1] - 1}]{end_of_line}"
                               f"{self.ansi['input']}").strip()

            if remove_space:
                answer = answer.replace(" ", "").replace("\t", "")

            if length[1] > len(answer) > length[0]:
                self.clean_formatting()
                return answer
            else:
                print(f"{Style.RESET_ALL}{Back.RED}Bad input! must be between {length[0] + 1} and {length[1] - 1} "
                      f"characters long")

    def ask_color(self, text: str):
        while True:
            answer = input(f"{text}[in hexadecimal format] {self.ansi['input']}")\
                .strip().lower().replace(" ", "").replace("\t", "")

            try:
                self.clean_formatting()
                return self.hex_to_rgb(answer)

            except:
                print(f"{Style.RESET_ALL}{Back.RED}Bad input! not a valid hex color code")

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
        return tuple(int(hex_string.strip('#')[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def clean_formatting():
        print(Style.RESET_ALL, end="")


ui = Ui(True)
os.system("cls")

print(f"""
{Fore.RED} _____  ____ _____  __  __  _  __  _   ____  _____  ____ _____ 
{Fore.RED}|_   _|| ===|| () )|  \\/  || ||  \\| | / () \\|_   _|/ () \\| () )
{Fore.RED}  |_|  |____||_|\\_\\|_|\\/|_||_||_|\\__|/__/\\__\\ |_|  \\____/|_|\\_\\
{Fore.RED}  :INSTALLER:                                    {Fore.RESET}-{Fore.BLUE}Python{Fore.YELLOW}Bear{Style.RESET_ALL}


    1) Hello! I'm some RED text that is bold and flashing
    2) {Fore.CYAN}Hello!{Fore.RESET} I'm {ui.rgb_fore(49, 230, 179)}some{Fore.RESET} {Back.RED}RED{Back.RESET} text that is {Style.BRIGHT}bold{Style.RESET_ALL} and {ui.ansi['blinking']}flashing{Style.RESET_ALL}
""")

allow_coloring_text = True if ui.choice("Which of the above 2 example texts looks better?",
                                        ("1", "2")) == "2" else False
account = {"name": None, "gender": None, "color": None, "bio": None, "pic": None, "plain name": None, }

print(ui.style(f"account creation", "title"))
account["plain name"] = ui.ask("What is your name?", (4, 30))
account["gender"] = ui.choice("What is your gender?", ("male", "female"))
account["color"] = ui.ask_color("What should your accounts color be?")
account["bio"] = ui.ask("Write a short biography for yourself", (0, 300), new_lined=True)
account["pic"] = ui.ask('Choose one character for your profile pic', (1, 1))
account["name"] = f"{ui.rgb_fore(*account['color'])}{account['plain name']}{Style.RESET_ALL}"

os.makedirs("build", exist_ok=True)
with open(os.path.join("build", "account.pkl"), "wb") as file:
    pickle.dump(account, file)

with open(os.path.join("build", "settings.pkl"), "wb") as file:
    pickle.dump({
        "allow coloring": allow_coloring_text,
        "python exe": "python" if os.name == "nt" else "python3",
        "localhost": "127.0.0.1",
        "host port": 8888
    }, file)

print(ui.style(f"setup complete", "title"))
