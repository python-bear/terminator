from random import *
from turtle import *
import turtle
import time

from freegame_utils import square

cells = {}
last_cells = cells.copy()
SCORE_WRITER = None

board_width = 400
board_height = 400
half_board_width = board_width // 2
half_board_height = board_height // 2
ENABLE_MUTATIONS = True
BACKGROUND_COLOR = 'grey'
TEXT_COLOR = 'white'
GAME_MODE = 'multiplayer'  # creative, zeroplayer, multiplayer
step_count = 0
compute_step_paused = False
processing_draw_cells = False
processing_compute_step = False
processing_write = False
processing_paused = False
processing_update_populations = False
processing_run_game = False
selected_brush = 'dot'
did_write = False

window_dimensions = {
    'width': board_width + board_width,
    'height': board_height + 50,
    'start x': 370,
    'start y': 50
}

PLAYER_NUMBER = 3

TEAM_COLORS = [0b100, 0b110, 0b010, 0b011, 0b001, 0b101, 0b111]
DEFAULT_TEAM = 0b100

color_codes = {
    0b100: 'red',
    0b110: 'yellow',
    0b010: 'green',
    0b011: 'cyan',
    0b001: 'blue',
    0b101: 'magenta',
    0b111: 'white',
    0b000: 'black',

    'red': 0b100,
    'yellow': 0b110,
    'green': 0b010,
    'cyan': 0b011,
    'blue': 0b001,
    'magenta': 0b101,
    'white': 0b111,
    'black': 0b000,
}

chosen_team_colors = [color_codes['red'], color_codes['blue'], color_codes['green'], color_codes['yellow']]
turn_color = color_codes[DEFAULT_TEAM]

team_scores = {
    'current': {
        'red': 0,
        'yellow': 0,
        'green': 0,
        'cyan': 0,
        'blue': 0,
        'magenta': 0,
        'white': 0
    },

    'total': {
        'red': 0,
        'yellow': 0,
        'green': 0,
        'cyan': 0,
        'blue': 0,
        'magenta': 0,
        'white': 0
    },

    'previous': {
        'red': 0,
        'yellow': 0,
        'green': 0,
        'cyan': 0,
        'blue': 0,
        'magenta': 0,
        'white': 0
    },
}

brushes = {
    'dot': 0,
    'beehive': 0,
    'blinker': 0,
    'eater 1': 0,
    'beacon': 0,
    'prepond': 0,
    'glider': 0,
    'yeast': 0,
    'hook': 0,
    'cap': 0,
    'l-ship': 0,
}


def scorer_write(string):
    global SCORE_WRITER, processing_write

    if processing_write:
        return

    processing_write = True

    SCORE_WRITER.undo()
    SCORE_WRITER.write(string, font=('Courier New', 12, 'normal'))

    processing_write = False


def initialize_world():
    """Initialize the world."""
    global half_board_height, half_board_width, cells

    for x in range(-half_board_width - 10, half_board_height + 10, 10):
        for y in range(-half_board_width - 10, half_board_height + 10, 10):
            cells[x, y] = 0b000


def initialize_teams():
    """Initialize the cells of each team."""
    global half_board_height, half_board_width, PLAYER_NUMBER, step_count, GAME_MODE, chosen_team_colors, turn_color

    if GAME_MODE in ('zeroplayer', 'creative'):
        for x in range(-half_board_width // 2, half_board_height // 2, 10):
            for y in range(-half_board_width // 2, half_board_height // 2, 10):
                cells[x, y] = choice((chosen_team_colors + chosen_team_colors + [0b000]))

    elif GAME_MODE == 'multiplayer':
        chosen_team_colors = []
        colors = input('COLORS :\nred, magenta, blue\ncyan, green, yellow\nwhite\n\n'
                       'Which teams? ').replace(',', '').strip().lower().split(' ')

        for team in TEAM_COLORS:
            if color_codes[team] in colors or "all" in colors:
                chosen_team_colors.append(team)

        for x in range(-half_board_width + 50, half_board_height - 50, 10):
            for y in range(-half_board_width + 50, half_board_height - 50, 10):
                cells[x, y] = choice((chosen_team_colors + [0b000] + [0b000]))

    turn_color = color_codes[choice(chosen_team_colors)]

    scorer_write('FOUR...')
    time.sleep(1)

    scorer_write('THREE...')
    time.sleep(1)

    scorer_write('TWO...')
    time.sleep(1)

    scorer_write('ONE...')
    time.sleep(1)

    scorer_write('GO !!')
    time.sleep(1)


def compute_step():
    """Compute one step in the Game of Life."""
    global half_board_height, half_board_width, PLAYER_NUMBER, cells, step_count, compute_step_paused, \
        processing_compute_step

    if processing_compute_step:
        return

    if compute_step_paused:
        return

    processing_compute_step = True

    neighbours = {}

    for x in range(-half_board_width, half_board_width, 10):
        for y in range(-half_board_height, half_board_height, 10):
            new_state = {
                0b100: 0,
                0b110: 0,
                0b010: 0,
                0b011: 0,
                0b001: 0,
                0b101: 0,
                0b111: 0,
                0b000: 1 if cells[x, y] == 0b000 else 0
            }

            for horizontal in [-10, 0, 10]:
                for vertical in [-10, 0, 10]:
                    if not (horizontal == 0 and vertical == 0):
                        neighbour = cells[x + horizontal, y + vertical]
                        new_state[neighbour] += 0 if neighbour == 0b000 else 1

            neighbours[(x, y)] = new_state

    for cell, new_state in neighbours.items():
        total_neighbours = 0

        for team_color, color_count in new_state.items():
            if team_color != 0b000:
                total_neighbours += color_count

        if new_state[0b000] != 1:  # If the cell is not black
            if total_neighbours < 2 or total_neighbours > 3:  # If it doesn't have two or three neighbours
                cells[cell] = 0b000  # it dies

        elif total_neighbours == 3 and cells[cell] == 0b000:  # If it is black and has three neighbours
            biggest_neighbours = []

            for team_color, color_count in new_state.items():
                if team_color != 0b000:
                    if len(biggest_neighbours) == 0:
                        biggest_neighbours.append(team_color)

                    elif color_count > new_state[biggest_neighbours[-1]]:
                        biggest_neighbours = [team_color]

                    elif color_count == new_state[biggest_neighbours[-1]]:
                        biggest_neighbours.append(team_color)

            if len(biggest_neighbours) == 1:
                cell_color = biggest_neighbours[0]

            elif not ENABLE_MUTATIONS:
                cell_color = choice(biggest_neighbours)

            else:  # If mutations are allowed and more than one big neighbour
                if len(biggest_neighbours) == 3:
                    new_color = int(biggest_neighbours[0])

                    for index in range(1, len(biggest_neighbours)):
                        new_color ^= int(biggest_neighbours[index])

                    if bin(int(format(new_color, 'b'), 2)) != '0b000':
                        cell_color = int(format(new_color, 'b'), 2)

                else:
                    cell_color = choice(TEAM_COLORS)

            cells[cell] = cell_color

    step_count += 1
    processing_compute_step = False


def update_populations():
    global cells, team_scores, processing_update_populations

    if processing_update_populations:
        return

    processing_update_populations = True

    for team in team_scores['current'].keys():
        if team_scores['current'][team] > team_scores['previous'][team]:
            team_scores['total'][team] += team_scores['current'][team] - team_scores['previous'][team]

        team_scores['previous'][team] = team_scores['current'][team]
        team_scores['current'][team] = 0

    for cell_coord, cell_color in cells.items():
        if cell_color != 0b000:
            team_scores['current'][color_codes[cell_color]] += 1

    scorer_write(f"TOTAL  POPULATION  SCORES : \n\n"
                 f"   red     :  {team_scores['total']['red']}\n"
                 f"   yellow  :  {team_scores['total']['yellow']}\n"
                 f"   green   :  {team_scores['total']['green']}\n"
                 f"   cyan    :  {team_scores['total']['cyan']}\n"
                 f"   blue    :  {team_scores['total']['blue']}\n"
                 f"   magenta :  {team_scores['total']['magenta']}\n"
                 f"   white   :  {team_scores['total']['white']}\n\n\n\n"
                 f"CURRENT  POPULATION  SCORES : \n\n"
                 f"   red     :  {team_scores['current']['red']}\n"
                 f"   yellow  :  {team_scores['current']['yellow']}\n"
                 f"   green   :  {team_scores['current']['green']}\n"
                 f"   cyan    :  {team_scores['current']['cyan']}\n"
                 f"   blue    :  {team_scores['current']['blue']}\n"
                 f"   magenta :  {team_scores['current']['magenta']}\n"
                 f"   white   :  {team_scores['current']['white']}\n\n"
                 f"TURN :  {step_count}  ({turn_color})")

    processing_update_populations = False


def toggle(variable):
    global compute_step_paused, processing_paused, processing_update_populations

    def switch(switch_variable):
        if switch_variable:
            return False

        else:
            return True

    if variable == 'paused':
        switch('processing_paused')

        compute_step_paused = switch(compute_step_paused)
        update_populations()

        switch('processing_paused')

    if variable == 'processing_pause':
        processing_paused = switch(processing_paused)

    if variable == 'processing_update_populations':
        processing_update_populations = switch(processing_update_populations)


def cursor_click(cursor_x, cursor_y):
    global turn_color

    if not compute_step_paused:
        return

    cell_x = (round((cursor_x + 165 - 5) / 10)) * 10
    cell_y = (round((cursor_y - 4 - 5) / 10)) * 10

    if cell_x in range(-half_board_width, half_board_height) and \
            cell_y in range(-half_board_width, half_board_height):
        cells[(cell_x, cell_y)] = color_codes[turn_color]

        draw_cells()


def change_turn(next_team):
    global turn_color

    turn_color = next_team

    update_populations()


def draw_cells():
    global processing_draw_cells

    if processing_draw_cells:
        return

    processing_draw_cells = True

    for (x, y), cell_color in cells.items():
        state_color = color_codes[cell_color]
        square(x - 165, y + 4, 10, state_color)

    processing_draw_cells = False


def run_game():
    global last_cells, cells, processing_run_game

    if processing_run_game:
        return

    processing_run_game = True

    try:
        compute_step()

        clear()

        draw_cells()
        update_populations()

        update()

        ontimer(run_game, 100)

    except turtle.Terminator as _error:
        end_game()

    except KeyboardInterrupt as _error:
        end_game()

    processing_run_game = False


def end_game():
    global SCORE_WRITER, cells, last_cells, GAME_MODE, step_count, compute_step_paused, processing_draw_cells, \
        processing_compute_step, processing_write, processing_paused, processing_update_populations, \
        processing_run_game, did_write
    bye()

    print('\n\nGAME OVER')
    cells = {}
    last_cells = cells.copy()
    SCORE_WRITER = None
    GAME_MODE = 'multiplayer'  # creative, zeroplayer, multiplayer
    step_count = 0
    compute_step_paused = False
    processing_draw_cells = False
    processing_compute_step = False
    processing_write = False
    processing_paused = False
    processing_update_populations = False
    processing_run_game = False
    did_write = False


def main_run():
    global SCORE_WRITER

    SCORE_WRITER = Turtle(visible=False)

    setup(window_dimensions['width'], window_dimensions['height'],
          window_dimensions['start x'], window_dimensions['start y'])
    title("Multiplayer JoeMama's Game Of Life")
    hideturtle()
    tracer(False)
    bgcolor(BACKGROUND_COLOR)

    SCORE_WRITER.penup()
    SCORE_WRITER.goto((half_board_width // 3), -half_board_height)
    SCORE_WRITER.pendown()
    SCORE_WRITER.color(TEXT_COLOR)
    SCORE_WRITER.write(f"INITIALIZING...", font=('Courier New', 12, 'normal'))

    print('GAME STARTED\n\n')

    try:
        initialize_world()
        initialize_teams()

    except KeyboardInterrupt as _error:
        end_game()

    listen()
    onkey(lambda: toggle('paused'), 'space')
    onkey(lambda: end_game(), 'Escape')
    onscreenclick(cursor_click)
    onkey(lambda: change_turn('red'), 'r')
    onkey(lambda: change_turn('yellow'), 'y')
    onkey(lambda: change_turn('green'), 'g')
    onkey(lambda: change_turn('cyan'), 'c')
    onkey(lambda: change_turn('blue'), 'b')
    onkey(lambda: change_turn('magenta'), 'm')
    onkey(lambda: change_turn('white'), 'w')

    run_game()
    done()


# 1.  block   [1x1-
# 2.  beehive [4x3- https://conwaylife.com/wiki/Beehive
# 3.  blinker [1x3- https://conwaylife.com/wiki/Blinker
# 4.  eater 1 [4x4- https://conwaylife.com/wiki/Eater_1
# 5.  beacon  [4x4- https://conwaylife.com/wiki/Beacon
# 6.  toad    [4x4- https://conwaylife.com/wiki/Toad
# 7.  prepond [3x3- https://conwaylife.com/wiki/Pond
# 8.  glider  [3x3- https://conwaylife.com/wiki/Glider
# 9.  yeast   [5x5- https://conwaylife.com/wiki/Bakery
# 10. hook    [3x4- custom
# 11. cap     [4x3- https://conwaylife.com/wiki/Cap
# 12. l-ship  [5x4- https://conwaylife.com/wiki/Lightweight_spaceship

main_run()
