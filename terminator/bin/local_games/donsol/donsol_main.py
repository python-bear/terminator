# Donsol game, for help go to https://wiki.xxiivv.com/site/donsol.html
import argparse
from blessed import Terminal

from bin.models import *

parser = argparse.ArgumentParser()

TERM = Terminal()


def main():
    print(TERM.enter_fullscreen)

    print(TERM.clear)

    dungeon = Dungeon()
    renderer = Renderer(dungeon, TERM)

    history = []

    with TERM.cbreak():
        keyval = ''

        while keyval.lower() != 'x':
            # HANDLE INPUT
            dungeon.handle_input(keyval)

            # RENDER
            renderer.render()

            # GET INPUT
            keyval = TERM.inkey()

    print(TERM.exit_fullscreen)


def run_game():
    main()
