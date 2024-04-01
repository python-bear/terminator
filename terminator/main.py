import os
import sys
import pickle
import getpass
from word2number import w2n
import questionary as qy


if len(os.listdir(os.path.join("build"))) == 0:
    from bin import installer

else:
    import colorama
    from colorama import Fore, Back, Style
    from bin import terminator

    term = terminator.Terminal()
    term.run()

sys.exit()
