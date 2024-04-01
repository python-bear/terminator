from random import choice
from turtle import *
import time

from freegame_utils import floor, vector


print('\n1')
time.sleep(1)
print('\n2')
time.sleep(1)
print('\n3')
time.sleep(1)
print('\nGO!!')

arrows = 'ghostman'
game_paused = False
game_over = False
state = {'pacman score': 0, 'ghostman score': 0}
t = Turtle(visible=False)
score_writer = Turtle(visible=False)
pacaim = vector(5, 0)
pacman = vector(-40, -80)
ghostmanaim = vector(0, 5)
ghostman = vector(40, 40)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
    [vector(-20, 0), vector(5, 0)],
]
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


# fmt: on


def square(x, y):
    """Draw square using t at (x, y)."""
    t.up()
    t.goto(x, y)
    t.down()
    t.begin_fill()

    for count in range(4):
        t.forward(20)
        t.left(90)

    t.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using t."""
    bgcolor('black')
    t.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                t.up()
                t.goto(x + 10, y + 10)
                t.dot(4, 'white')


def move():
    global game_paused, pacman, game_over
    """Move pacman, ghostman, and all ghosts."""

    if not game_over:
        score_writer.undo()

        if state['ghostman score'] > 2:
            score_writer.write(f"PACMAN: LOSES ({state['pacman score']})\nGHOSTMAN: WINS")
            game_over = True

        elif state['pacman score'] >= 85:
            score_writer.write(f"PACMAN: WINS\nGHOSTMAN: LOSES")
            game_over = True

        else:
            score_writer.write(f"PACMAN: {state['pacman score']}\nGHOSTMAN: {state['ghostman score']}")

    clear()

    # Pacman
    if valid(pacman + pacaim):
        pacman.move(pacaim)

    pacman_index = offset(pacman)

    if tiles[pacman_index] == 1:
        tiles[pacman_index] = 2
        state['pacman score'] += 1
        x = (pacman_index % 20) * 20 - 200
        y = 180 - (pacman_index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Ghostman
    if valid(ghostman + ghostmanaim):
        ghostman.move(ghostmanaim)

    up()
    goto(ghostman.x + 10, ghostman.y + 10)
    dot(20, 'red')

    # Ghosts
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20 or abs(pacman - ghostman) < 20:
            if not game_over:
                score_writer.undo()

                if state['ghostman score'] > 2:
                    score_writer.write(f"PACMAN: LOSES ({state['pacman score']})\nGHOSTMAN: WINS")
                    game_over = True

                elif state['ghostman score'] <= 2:
                    score_writer.write(f"PACMAN: {state['pacman score']}\nGHOSTMAN: {state['ghostman score']}")
                    state['ghostman score'] += 1
                    pacman = vector(-40, -80)

                elif state['pacman score'] >= 85:
                    score_writer.write(f"PACMAN: WINS\nGHOSTMAN: LOSES")
                    game_over = True

                else:
                    score_writer.write(f"PACMAN: {state['pacman score']}\nGHOSTMAN: {state['ghostman score']}")

            if game_over:
                return

    ontimer(move, 100)


def change_pacman(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        pacaim.x = x
        pacaim.y = y


def change_ghostman(x, y):
    """Change ghostman aim if valid."""
    if valid(ghostman + vector(x, y)):
        ghostmanaim.x = x
        ghostmanaim.y = y


setup(600, 440, 370, 0)
hideturtle()
tracer(False)
score_writer.goto(160, 160)
score_writer.color('white')
score_writer.write(f"PACMAN: {state['pacman score']}\nGHOSTMAN: {state['ghostman score']}")
listen()

if arrows == 'ghostman':
    onkey(lambda: change_pacman(5, 0), 'd')
    onkey(lambda: change_pacman(-5, 0), 'a')
    onkey(lambda: change_pacman(0, 5), 'w')
    onkey(lambda: change_pacman(0, -5), 's')
    onkey(lambda: change_ghostman(5, 0), 'Right')
    onkey(lambda: change_ghostman(-5, 0), 'Left')
    onkey(lambda: change_ghostman(0, 5), 'Up')
    onkey(lambda: change_ghostman(0, -5), 'Down')

elif arrows == 'pacman':
    onkey(lambda: change_ghostman(5, 0), 'd')
    onkey(lambda: change_ghostman(-5, 0), 'a')
    onkey(lambda: change_ghostman(0, 5), 'w')
    onkey(lambda: change_ghostman(0, -5), 's')
    onkey(lambda: change_pacman(5, 0), 'Right')
    onkey(lambda: change_pacman(-5, 0), 'Left')
    onkey(lambda: change_pacman(0, 5), 'Up')
    onkey(lambda: change_pacman(0, -5), 'Down')

world()
move()
done()
