# Dig Dug - An Obscure Arcade Game
# Author: G.G.Otto

import turtle
import random
import time


class DigDug(turtle.Turtle):
    """manipulates the player on the screen"""

    def __init__(self, game):
        """DigDug() -> DigDug
        constructs player at (0,0)
        game: Game object"""
        # get game info
        self.game = game
        self.blockSize = game.get_block_size()
        self.width = game.get_width()

        # set up turtle
        turtle.Turtle.__init__(self)  # make DigDug a turtle
        self.shapesize(self.blockSize / 20)
        self.shape("turtle")
        self.pensize(self.blockSize * 18 / 20)
        self.color("black", "blue")

        self.moving = False
        self.moveCount = 0
        self.moveSpeed = self.blockSize / 2
        # check if valid speed
        if (self.blockSize / self.moveSpeed) % 1 != 0:
            raise ValueError("DigDug speed does not divide evenly into blockSize")

    def get_block_in_direction(self, pos, direction):
        """DigDug.get_block_in_direction(pos,direction) -> int
        returns the block number of the block in direction
        pos: tuple representing (x,y)
        direction: 0, Up; 1, Right; 2, Down; 3, Left"""
        x, y = pos  # unpack coords

        # list of directions
        up = x, y + self.blockSize
        right = x + self.blockSize, y
        down = x, y - self.blockSize
        left = x - self.blockSize, y
        directList = [up, right, down, left]

        return self.game.coord_to_block(directList[direction])

    def move(self):
        """DigDug.move()
        moves the player"""
        if self.moving:
            self.fd(self.moveSpeed)
            self.moveCount += 1

            # if move is done
            if self.moveCount == 2:
                self.moving = False
                self.moveCount = 0

    def go_up(self):
        """DigDug.go_up()
        moves the player up"""
        if not self.moving and self.get_block_in_direction(self.pos(), 0) is not None:
            self.moving = True
            self.seth(90)
            self.pu()
            self.fd(self.blockSize)
            self.game.add_score(
                self.game.add_block(self.game.coord_to_block(self.pos()), self.heading()))
            self.bk(self.blockSize)
            self.pd()

    def go_right(self):
        """DigDug.go_right()
        moves the player right"""
        if not self.moving and self.get_block_in_direction(self.pos(), 1) is not None:
            self.moving = True
            self.seth(0)
            self.pu()
            self.fd(self.blockSize)
            self.game.add_score(
                self.game.add_block(self.game.coord_to_block(self.pos()), self.heading()))
            self.bk(self.blockSize)
            self.pd()

    def go_down(self):
        """DigDug.go_down()
        moves the player down"""
        if not self.moving and self.get_block_in_direction(self.pos(), 2) is not None:
            self.moving = True
            self.seth(270)
            self.pu()
            self.fd(self.blockSize)
            self.game.add_score(
                self.game.add_block(self.game.coord_to_block(self.pos()), self.heading()))
            self.bk(self.blockSize)
            self.pd()

    def go_left(self):
        """DigDug.go_left()
        moves the player left"""
        if not self.moving and self.get_block_in_direction(self.pos(), 3) is not None:
            self.moving = True
            self.seth(180)
            self.pu()
            self.fd(self.blockSize)
            self.game.add_score(
                self.game.add_block(self.game.coord_to_block(self.pos()), self.heading()))
            self.bk(self.blockSize)
            self.pd()

    def set_moving(self, boolean):
        """DigDug.set_moving(boolean)
        sets the moving to disable key bindings"""
        self.moving = boolean


class Harpoon(turtle.Turtle):
    """manipulates the player's harpoon"""

    def __init__(self, player, game):
        """Harpoon(player,game) -> Harpoon
        constructs the harpoon for the player in game
        player: DigDug
        game: Game"""
        # get game info
        self.game = game
        self.blockSize = game.get_block_size()
        self.width = game.get_width()
        self.player = player

        # set up turtle
        turtle.Turtle.__init__(self)  # make DigDug a turtle
        self.shapesize(1)
        self.pu()
        self.ht()
        self.color("red")
        self.recordTime = 0  # recorded time

        # set up timer
        self.timer = turtle.Turtle()
        self.timer.ht()
        self.timer.pu()
        self.timer.color("red", "black")
        self.timer.shape("square")
        self.timer.shapesize(self.blockSize / 40, self.blockSize / 80)
        self.meterPosDic = {}  # positions for each meter

        # get position
        self.meterX = 220
        self.meterY = 295
        self.timer.goto(self.meterX - self.blockSize * 9 / 4, self.meterY)

        # draw meter
        for meterNum in range(10):
            self.timer.stamp()
            self.meterPosDic[meterNum] = self.timer.pos()
            self.timer.setx(self.timer.xcor() + self.blockSize / 2)
        self.timer.color("red", "red")

        # draw meter full
        self.timer.goto(self.meterX - self.blockSize * 9 / 4, self.meterY)
        self.stampList = []
        for i in range(10):
            self.stampList.append(self.timer.stamp())
            self.timer.setx(self.timer.xcor() + self.blockSize / 2)
        self.howFull = 10  # how full the meter is

        self.moving = False
        self.moveSpeed = 1.5

    def move(self):
        """Harpoon.move()
        moves the harpoon"""
        if self.isvisible():
            self.fd(self.moveSpeed)

            # if out of bounds
            if self.is_done():
                self.ht()
        self.check_time()

    def launch(self):
        """Harpoon.launch()
        launches the harpoon"""
        # if game is done
        if self.game.is_ended():
            return

        if not self.moving and self.howFull == 10:
            self.recordTime = time.time()
            self.howFull = 0
            self.seth(self.player.heading())
            self.goto(self.player.pos())
            self.st()

            # empty meter
            for stamp in self.stampList:
                self.timer.clearstamp(stamp)

    def check_time(self):
        """Harpoon.check_time()
        checks when the harpoon can launch"""
        if self.howFull < 10 and time.time() - self.recordTime > 1:  # not yet full and time is ready
            self.timer.goto(self.meterPosDic[self.howFull])
            self.stampList.append(self.timer.stamp())
            self.recordTime = time.time()  # reset recorded time
            self.howFull += 1  # add one two meter

    def fill_meter(self):
        """Harpoon.fill_meter()
        refills the meter"""
        for meter in range(self.howFull, 10):
            self.timer.goto(self.meterPosDic[meter])
            self.stampList.append(self.timer.stamp())
        self.recordTime = time.time()  # reset recorded time
        self.howFull = 10  # reset meter

    def is_done(self):
        """Harpoon.is_done()
        checks the harpoon is done moving"""
        currentBlock = self.game.coord_to_block(self.pos())  # get current block

        # get block behind
        self.bk(self.blockSize)
        blockBehind = self.game.coord_to_block(self.pos())
        self.fd(self.blockSize)

        playerBlock = self.game.coord_to_block(self.player.pos())  # get block with player

        # check if out of bounds
        blockDic = self.game.get_blocks()
        if currentBlock not in blockDic or (currentBlock != playerBlock and blockBehind in blockDic
                                            and blockBehind not in blockDic[currentBlock]):
            return True
        return False

    def add_speed(self, speed):
        """Monster.add_speed(speed)
        adds speed to monster"""
        self.moveSpeed += speed


class Monster(turtle.Turtle):
    """manipulates the monster on the screen"""

    def __init__(self, player, game, harpoon):
        """Monster(player,game,harpoon) -> Monster
        constructs a monster that hunts for player.
        player: DigDug
        game: Game
        harpoon: Harpoon"""
        # get game info
        self.blockSize = game.get_block_size()
        self.width = game.get_width()
        self.game = game

        # get player info
        self.player = player
        self.harpoon = harpoon

        # set up turtle
        turtle.Turtle.__init__(self)
        self.pu()
        self.shape("circle")
        self.color(0, random.randint(100, 255), 0)
        self.shapesize(self.blockSize / 25)
        # goto random corner
        self.goto(random.choice([
            ((self.width / 2 - 0.5) * self.blockSize, (self.width / 2 - 0.5) * self.blockSize),
            (-(self.width / 2 - 0.5) * self.blockSize, (self.width / 2 - 0.5) * self.blockSize),
            (-(self.width / 2 - 0.5) * self.blockSize, -(self.width / 2 - 0.5) * self.blockSize),
            ((self.width / 2 - 0.5) * self.blockSize, -(self.width / 2 - 0.5) * self.blockSize)]))
        self.moveSpeed = 0.26 + random.randint(0, 15) / 100
        self.canMove = self.can_move_forward()
        self.blockToMoveFrom = 0  # tells if monster can move from a block
        self.errorMargin = random.randint(0, 20)

    def can_move_forward(self):
        """Monster.can_move_forward() -> boolean
        returns True if monster can move forward. Else returns False"""
        self.fd(self.blockSize / 2 + 1.5 * self.moveSpeed)
        block = self.game.coord_to_block(self.pos())  # get current block
        self.bk(self.blockSize / 2 + self.moveSpeed)
        currentBlock = self.game.coord_to_block(self.pos())

        if currentBlock == block or (currentBlock in self.game.get_blocks()
                                     and block in self.game.get_blocks()[currentBlock]):
            return True
        return False

    def can_see(self):
        """Monster.can_see() -> boolean
        checks if monster can 'see' player"""
        monsterBlock = self.game.coord_to_block(self.pos())
        playerBlock = self.game.coord_to_block(self.player.pos())

        # look up
        lastBlock = monsterBlock
        currentBlock = self.game.coord_to_block((self.xcor(), self.ycor() + self.blockSize))
        if currentBlock in self.game.get_blocks():
            x, y = self.game.block_to_coord(currentBlock)
        while currentBlock in self.game.get_blocks()[lastBlock]:
            y += self.blockSize
            lastBlock = currentBlock
            currentBlock = self.game.coord_to_block((x, y))
            if currentBlock == playerBlock:
                return True

        # look right
        lastBlock = monsterBlock
        currentBlock = self.game.coord_to_block((self.xcor() + self.blockSize, self.ycor()))
        if currentBlock in self.game.get_blocks():
            x, y = self.game.block_to_coord(currentBlock)
        while currentBlock in self.game.get_blocks()[lastBlock]:
            x += self.blockSize
            currentBlock = self.game.coord_to_block((x, y))
            if currentBlock == playerBlock:
                return True

        # look down
        lastBlock = monsterBlock
        currentBlock = self.game.coord_to_block((self.xcor(), self.ycor() - self.blockSize))
        if currentBlock in self.game.get_blocks():
            x, y = self.game.block_to_coord(currentBlock)
        while currentBlock in self.game.get_blocks()[lastBlock]:
            y -= self.blockSize
            lastBlock = currentBlock
            currentBlock = self.game.coord_to_block((x, y))
            if currentBlock == playerBlock:
                return True

        # look left
        lastBlock = monsterBlock
        currentBlock = self.game.coord_to_block((self.xcor() - self.blockSize, self.ycor()))
        if currentBlock in self.game.get_blocks():
            x, y = self.game.block_to_coord(currentBlock)
        while currentBlock in self.game.get_blocks()[lastBlock]:
            x -= self.blockSize
            lastBlock = currentBlock
            currentBlock = self.game.coord_to_block((x, y))
            if currentBlock == playerBlock:
                return True

        return False

    def get_ideal(self):
        """Monster.get_ideal() -> list of block numbers
        returns the ideal turns monster can make"""
        idealMoves = []
        block = self.game.coord_to_block(self.pos())  # get current block num

        # get coords
        oldX, oldY = self.pos()
        playerX, playerY = self.player.pos()

        # loop through directions
        if block not in self.game.get_blocks():
            return
        for direction in self.game.get_blocks()[block]:
            self.goto(self.game.block_to_coord(direction))
            newX, newY = self.pos()  # get new coords
            if abs(oldX - playerX) > abs(newX - playerX) or abs(oldY - playerY) > abs(newY - playerY):
                idealMoves.append(direction)
        self.goto(oldX, oldY)  # back in position
        return idealMoves

    def move(self):
        """Monster.move()
        moves the monster"""
        # can't move
        if self.game.coord_to_block(self.pos()) not in self.game.get_blocks() or \
                len(self.game.get_blocks()[self.game.coord_to_block(self.pos())]) == 0:
            return

        # can move
        ideals = self.get_ideal()
        passages = self.game.get_blocks()[self.game.coord_to_block(self.pos())]
        blockX, blockY = self.game.block_to_coord(self.game.coord_to_block(self.pos()))  # coords of block
        distanceFromBlock = ((self.xcor() - blockX) ** 2 + (self.ycor() - blockY) ** 2) ** (
                1 / 2)  # distance from the block
        playerPos = self.player.pos()

        if self.canMove and self.can_move_forward():
            self.fd(self.moveSpeed)
            # if away from block
            if self.blockToMoveFrom != self.game.coord_to_block(self.pos()):
                self.canMove = len(self.game.get_blocks()[self.game.coord_to_block(self.pos())]) < 3
        elif distanceFromBlock > self.moveSpeed and self.can_move_forward():
            self.fd(self.moveSpeed)
        elif monster.can_see():
            self.goto(self.game.block_to_coord(self.game.coord_to_block(self.pos())))
            self.seth(self.towards(self.game.block_to_coord(self.game.coord_to_block(playerPos))))
            self.canMove = True
            self.blockToMoveFrom = self.game.coord_to_block(self.pos())
        elif len(ideals) != 0:
            self.goto(self.game.block_to_coord(self.game.coord_to_block(self.pos())))
            self.seth(self.towards(self.game.block_to_coord(random.choice(ideals))))
            self.canMove = True
            self.blockToMoveFrom = self.game.coord_to_block(self.pos())
        else:
            self.goto(self.game.block_to_coord(self.game.coord_to_block(self.pos())))
            self.seth(self.towards(self.game.block_to_coord(
                random.choice(passages))))
            self.canMove = True
            self.blockToMoveFrom = self.game.coord_to_block(self.pos())

    def check_hit(self, monsterList):
        """Monster.check_hit(monsterList) -> list of monsters
        if hit my harpoon, hide monster and remove it from list"""
        if not self.isvisible():
            return

        # get block numbers
        currentBlock = self.game.coord_to_block(self.pos())
        harpoonBlock = self.game.coord_to_block(self.harpoon.pos())

        # get block behind
        self.harpoon.bk(self.blockSize)
        behindBlock = self.game.coord_to_block(self.harpoon.pos())
        self.harpoon.fd(self.blockSize)

        if self.harpoon.isvisible() and (currentBlock == harpoonBlock or currentBlock == behindBlock):
            self.harpoon.ht()
            self.ht()
            self.game.kill_monster()

            # update score
            self.game.add_score(100)

        return monsterList

    def check_hit_player(self):
        """Monster.check_hit_player()
        ends game if player has been hit"""
        if not self.isvisible():
            return

        # get block numbers
        currentBlock = self.game.coord_to_block(self.pos())
        playerBlock = self.game.coord_to_block(self.player.pos())

        # if player is hit
        if currentBlock == playerBlock:
            self.game.end_game()
            self.player.color("black", "red")

    def revive(self):
        """Monster.revive()
        revives the monster and puts in the correct place"""
        self.__init__(self.player, self.game, self.harpoon)

    def add_speed(self, speed):
        """Monster.add_speed(speed)
        adds speed to monster"""
        self.moveSpeed += speed


class Bonus(turtle.Turtle):
    """manipulates the bonus block. Bonus is random between 100 and 200"""

    def __init__(self, player, game):
        """Bonus(player) -> bonus
        constructs a bonus block for player
        game: Game
        player: DigDug"""
        # get game info
        self.game = game
        self.width = self.game.get_width()
        self.blockSize = self.game.get_block_size()
        self.player = player

        # get turtle
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(self.blockSize / 25)
        self.color("red")
        self.pu()
        self.goto(self.game.block_to_coord(self.choose_random_block()))

        self.recordTime = time.time()  # time on board
        self.numMoves = 0  # number of moves on board

    def choose_random_block(self):
        """Bonus.choose_random.block() -> block number
        chooses a random block that is not in blockDic"""
        randomBlock = 0
        while randomBlock in self.game.get_blocks():
            randomBlock = random.randint(-self.width ** 2 // 2 + 1, self.width ** 2 // 2)
        return randomBlock

    def is_hit(self):
        """Bonus.is_hit() -> boolean
        returns True if player hit self. Else returns False"""
        # get block nums
        currentBlock = self.game.coord_to_block(self.pos())
        playerBlock = self.game.coord_to_block(self.player.pos())

        if currentBlock == playerBlock and self.isvisible():
            self.game.add_score(random.randint(100, 200))  # add random score
            return True
        return False

    def make_goto(self):
        """Bonus.make_goto()
        makes the bonus go to a random spot and show itself"""
        if len(self.game.blockDic) > self.width ** 2 - 5:
            return

        self.goto(self.game.block_to_coord(self.choose_random_block()))
        self.recordTime = time.time()
        self.st()

    def move(self):
        """Bonus.move()
        moves the bonus if hit or times up"""
        if (self.is_hit() or time.time() - self.recordTime > 7.5) and self.isvisible():
            self.ht()
            self.screen.ontimer(self.make_goto, random.randint(0, 60000))


class Game:
    """represents and manipulates the game and game stats"""

    def __init__(self, startLevel):
        """Game(startLevel) -> Game
        constructs the game
        startLevel: int representing the level that starts"""
        self.width = 23  # width of game in blocks - game is square
        self.blockSize = 24  # the size of each cell
        self.blockDic = {}  # dictionary for all blocks

        # set up turtle
        self.t = turtle.Turtle()
        self.t.pu()
        self.t.ht()
        self.t.shapesize(self.blockSize / 20)
        self.t.shape("square")
        self.t.pensize(self.blockSize * 18 / 20)
        self.color = 179, 130, 74

        # add initial blocks and game stats
        self.score = 0
        self.level = startLevel
        self.draw_board()
        self.initial_passage(self.level)
        self.t.color("white")
        self.t.goto(-280, 280)
        self.t.write("DIG-DUG", False, "left", ("Arial", 20, "bold"))

        self.isEnded = False  # tells if game has ended
        self.gameSpeed = 0
        self.idealTime = 0.016

        # set up score turtle
        self.scoreTurtle = turtle.Turtle()
        self.scoreTurtle.pu()
        self.scoreTurtle.ht()
        self.scoreTurtle.color("white")
        self.scoreTurtle.goto(0, -310)
        self.update_stats()

    def draw_board(self):
        """Game.draw_board()
        draws the board using stamp"""
        self.t.color(self.color, self.color)
        self.t.seth(0)
        self.t.goto(self.width * self.blockSize / 2, self.width * self.blockSize / 2)
        self.t.begin_fill()
        for i in range(4):
            self.t.right(90)
            self.t.fd(self.width * self.blockSize)
        self.t.end_fill()

    def block_to_coord(self, blockNum):
        """Game.block_to_coord(blockNum) -> tuple containing the x and y coordinates
        returns the corresponding coordinate of a block
        if block not in board, returns None
        blockNum: int"""
        # if out of board
        if blockNum is None:
            return None
        elif blockNum < -self.width ** 2 // 2 or blockNum > self.width ** 2 // 2:
            return
        # if in board
        blockNum += self.width ** 2 // 2  # bring up for computation
        x = (blockNum % self.width + 0.5 - self.width / 2) * self.blockSize
        y = (blockNum // self.width + 0.5 - self.width / 2) * self.blockSize
        return x, y

    def coord_to_block(self, pos):
        """Game.coord_to_block(pos) -> int that is the block number
        returns the block number that point
        if point not on board, returns None
        pos: tuple (x,y)"""
        x, y = pos  # unpack tuple
        # translate the coords into the first quadrant
        newX = x + self.width * self.blockSize / 2
        newY = y + self.width * self.blockSize / 2
        # not in board
        if newX >= self.width * self.blockSize or newX <= 0 or newY > self.width * self.blockSize or newY < 0:
            return
        # output for in maze
        output = newX // self.blockSize + (newY // self.blockSize) * self.width - self.width ** 2 // 2
        return int(output)

    def get_blocks(self):
        """Game.get_blocks() -> dict
        returns a dictionary with all blocks and their turns"""
        return self.blockDic

    def get_block_size(self):
        """Game.get_block_size() -> int
        returns the size of the cells"""
        return self.blockSize

    def get_width(self):
        """Game.get_width() -> int
        returns the width of the game"""
        return self.width

    def add_block(self, blockNum, heading):
        """Game.add_block(blockNum,heading)
        adds a block the block dict"""
        score = 0
        # not in board or already recorded
        if blockNum is None:
            return score
        # not yet recorded
        elif blockNum not in self.blockDic:
            self.blockDic[blockNum] = []
            score = 1
        x, y = self.block_to_coord(blockNum)  # get position

        # dict of directions
        directDic = {}
        directDic[270] = x, y + self.blockSize
        directDic[180] = x + self.blockSize, y
        directDic[90] = x, y - self.blockSize
        directDic[0] = x - self.blockSize, y

        # add blockNum
        directNum = self.coord_to_block(directDic[heading])
        if directNum in self.blockDic:  # in block just left is in list
            # add dictionary
            if blockNum not in self.blockDic[directNum]:
                self.blockDic[directNum].append(blockNum)
            if directNum not in self.blockDic[blockNum]:
                self.blockDic[blockNum].append(directNum)
        return score

    def passage(self, length):
        """Game.passage(length)
        draws a passage and adds it to blockDic"""
        self.t.pd()
        self.add_block(self.coord_to_block(self.t.pos()), self.t.heading())  # add start pos
        for i in range(length):
            self.t.fd(self.blockSize)
            self.add_block(self.coord_to_block(self.t.pos()), self.t.heading())
        self.t.pu()

    def initial_passage(self, level):
        """Game.initial_passage(level)
        draws the initial passage for level"""
        self.t.color("black")

        # level type 1
        if (level - 1) % 3 == 0:
            self.t.goto((self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.t.seth(270)
            self.passage(5)
            self.t.right(90)
            self.passage(11)
            self.t.left(90)
            self.passage(6)

            self.t.goto(-(self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.t.seth(270)
            self.passage(11)
            self.t.left(90)
            self.passage(11)
            self.t.goto((self.width - 1) * self.blockSize / 2,
                        -(self.width - 1) * self.blockSize / 2)
            self.t.seth(180)
            self.passage(11)
            self.t.right(90)
            self.passage(11)
            self.t.goto(-(self.width - 1) * self.blockSize / 2,
                        -(self.width - 1) * self.blockSize / 2)
            self.t.seth(90)
            self.passage(5)
            self.t.right(90)
            self.passage(11)
        # level type 2
        elif (level - 1) % 3 == 1:
            self.t.goto((self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.t.seth(270)
            self.passage(22)
            self.t.goto(-(self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.passage(22)
            self.t.goto(self.blockSize * 5, 0)
            self.t.seth(180)
            self.passage(10)
        # level type 3
        else:
            self.t.goto((self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.t.seth(270)
            self.passage(22)
            self.t.goto(-(self.width - 1) * self.blockSize / 2,
                        (self.width - 1) * self.blockSize / 2)
            self.passage(22)
            self.t.goto(-self.blockSize * 11, 0)
            self.t.seth(0)
            self.passage(4)
            self.t.left(90)
            self.passage(7)
            for i in range(4):
                self.t.right(90)
                self.passage(14)
            self.t.goto(self.blockSize * 11, 0)
            self.t.seth(180)
            self.passage(4)
            self.t.goto(0, self.blockSize * 7)
            self.t.seth(270)
            self.passage(14)
            self.t.goto(-self.blockSize * 4, 0)
            self.t.seth(0)
            self.passage(8)

    def add_monsters(self, num, player, harpoon):
        """Game.add_monsters(num,player,harpoon)
        adds num monsters to the game
        player: DigDug
        harpoon: Harpoon"""
        self.monsters = [Monster(player, game, harpoon) for i in range(num)]
        self.live_monsters = num
        self.num_monsters = num

    def kill_monster(self):
        """Game.kill_monster(self)
        subtracts 1 from likeMonsters"""
        self.live_monsters -= 1

    def get_living_monsters(self):
        """Game.get_dead_monsters() -> int
        returns the number of living monsters"""
        return self.live_monsters

    def get_monsters(self):
        """Game.get_monsters() -> list of Monster obj
        returns a list of all monsters"""
        return self.monsters

    def reset_living_monsters(self):
        """Game.resent_living_monsters()
        resets the living monsters"""
        self.live_monsters = self.num_monsters

    def add_speed(self, speed, harp):
        """Game.add_speed(speed,harpoon)
        adds speed to the game"""
        if self.idealTime > 0.009:
            self.idealTime -= speed

    def update_stats(self):
        """Game.update_score(scoreToAdd)
        updates the game score"""
        if not self.isEnded:
            self.scoreTurtle.clear()
            msg = "Score: {} Level: {}".format(self.score, self.level)
            self.scoreTurtle.write(msg, False, "center", ("Arial", 18, "bold"))

    def add_level(self):
        """Game.add_level()
        adds a level to the game"""
        self.level += 1

        # set up again
        self.blockDic.clear()
        self.t.clear()
        self.draw_board()
        self.initial_passage(self.level)
        self.update_stats()

    def get_level(self):
        """Game.get_level() -> int
        returns the level of the game"""
        return self.level

    def add_score(self, scoreToAdd):
        """Game.add_score(scoreToAdd)
        adds scoreToAdd to score
        scoreToAdd: int"""
        self.score += scoreToAdd
        self.update_stats()

    def end_game(self):
        """Game.end_game()
        ends the game"""
        self.t.goto(0, -20)
        self.t.color("white")
        self.t.write("Game Over!", False, "center", ("Arial", 50, "italic"))
        self.isEnded = True

    def is_ended(self):
        """Game.is_ended() -> boolean
        returns True if the game has ended. Else returns False"""
        return self.isEnded

    def speed_regulate(self, speedTime, player, harpoon):
        """Game.speed_regulate(speedTime,player,harpoon)
        regulates the speed
        speedTime: float
        player: DigDug
        harpoon: Harpoon"""
        if speedTime == 0:
            return

        if speedTime > game.idealTime + 0.01 and self.gameSpeed < 1.5:
            harpoon.add_speed(0.01)
            for m in self.monsters:
                m.add_speed(0.01)
            self.gameSpeed += 0.01
        elif speedTime < self.idealTime - 0.01 and self.gameSpeed > 0.1:
            harpoon.add_speed(-0.02)
            for m in self.monsters:
                m.add_speed(-0.02)
            self.gameSpeed -= 0.02


# Game setup
turtle.tracer(0)  # speeds up animation
turtle.colormode(255)  # color to hex mode
turtle.setundobuffer(5)  # only saves last move

wn = turtle.Screen()  # environment for turtles
wn.bgcolor("black")  # window background color
wn.title("Dig Dug")  # adds caption

game = Game(1)
player = DigDug(game)
harpoon = Harpoon(player, game)
bonus = Bonus(player, game)
game.add_monsters(6, player, harpoon)

# key bindings
wn.onkeypress(player.go_up, "Up")
wn.onkeypress(player.go_right, "Right")
wn.onkeypress(player.go_down, "Down")
wn.onkeypress(player.go_left, "Left")
wn.onkeypress(harpoon.launch, "space")
wn.listen()

# Game play
speedRegulate = time.time()
while True:
    # regulate speed
    game.speed_regulate(time.time() - speedRegulate, player, harpoon)
    speedRegulate = time.time()

    player.move()  # move player
    harpoon.move()  # move harpoon
    bonus.move()  # move bonus
    for monster in game.get_monsters():  # loop through monsters
        monster.move()  # move monster
        monster.check_hit(game.get_monsters())
        monster.check_hit_player()

        # if game is over
        if game.is_ended():
            break

    wn.update()  # update the screen

    # if next level
    if game.get_living_monsters() == 0:
        player.set_moving(True)  # disable player key bindings
        player.home()  # player to origin
        player.clear()  # remove player's path
        harpoon.fill_meter()  # fill bonus meter
        game.add_level()  # add a level to the board
        game.add_score(game.get_level() * 50)  # add bonus for score level
        game.add_speed(0.003, harpoon)  # add small amount of speed
        game.add_monsters(5 + game.level, player, harpoon)
        game.reset_living_monsters()  # resets the number of living monsters
        bonus.make_goto()  # restart the bonus

        # read monsters
        for monster in game.get_monsters():
            monster.revive()

        time.sleep(0.4)
        player.set_moving(False)  # enable player key bindings
        wn.update()

    # if game is over
    if game.is_ended():
        player.set_moving(True)  # disable player key bindings
        break

wn.mainloop()
