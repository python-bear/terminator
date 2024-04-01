from bin.utils import *
from bin.models import Player, Enemy
from bin.interface import Fore, Style, Back, random, time, colorama


class WorldBase:
    def __init__(self, display_machine, game_name, running_sub_world, world_name):
        self.dm = display_machine
        self.GAME_NAME = game_name
        self.WORLD_NAME = world_name
        self.is_sub_world = running_sub_world
        self.player = None
        self.PLAYER_COMMANDS = {
            '~': ('~', 'eat', 'eat provisions', 'eat food', 'take provisions', 'provision'),
            '!': ('!', 'quit', 'exit', 'suicide'),
            '@': ('@', 'bag', 'inventory'),
            '#': ('#', 'stats', 'statistics', 'attribs', 'attributes'),
            '$': ('$', 'random', 'coin', 'flip coin'),
            '%': ('%', 'test luck', 'test', 'test my luck', 'take chance', 'take a chance', 'chance', 'luck'),
            '>': ('>', 'random', 'coin', 'flip coin'),
            '?': ('?', 'help', 'what', 'what?'),
            '*': ('*', 'set', 'setting', 'settings', 'cog', 'customize', 'custom', 'speed', 'pref')
        }
        self.PLAYER_COMMANDS_TABLE = ([command for command in self.PLAYER_COMMANDS.keys()],
                                      (f'[{str(self.PLAYER_COMMANDS["~"])[6:-1]}] You eat one of your provisions, '
                                       f'gaining two stamina points and losing that provision. You can call this '
                                       f'command whenever you are not fighting.',
                                       f'[{str(self.PLAYER_COMMANDS["!"])[6:-1]}] This will end the game.',
                                       f'[{str(self.PLAYER_COMMANDS["@"])[6:-1]}] Shows you what is in your inventory, '
                                       f'how much you have of each item in your inventory, and any effects the items '
                                       f'in your inventory are granting you.',
                                       f'[{str(self.PLAYER_COMMANDS["#"])[6:-1]}] Displays your current stamina, '
                                       f'skill, and luck scores',
                                       f'[{str(self.PLAYER_COMMANDS["$"])[6:-1]}] This command can only be called if '
                                       f'you have at least one coin in your inventory. It will return either `heads` '
                                       f'or `tails`, but doesn\'t actually have any effect on the game.',
                                       f'[{str(self.PLAYER_COMMANDS["%"])[6:-1]}] This is the command for testing your '
                                       f'luck, which is explained above. You will only be able to run this '
                                       f'command when explicitly told so by the story, not whenever you want like '
                                       f'other commands in this list.',
                                       f'[{str(self.PLAYER_COMMANDS[">"])[6:-1]}] Shows this table; displays a list of '
                                       f'universal commands and their actions.',
                                       f'[{str(self.PLAYER_COMMANDS["?"])[6:-1]}] Displays this help message, which '
                                       f'will teach you how to play the game.',
                                       f'[{str(self.PLAYER_COMMANDS["*"])[6:-1]}] Sets/changes the reading speed.'))
        self.ITEMS = {
            'gold coins': {
                'stamina': 0,
                'skill': 0,
                'luck': 0,
            },
            'provisions': {
                'stamina': 0,
                'skill': 0,
                'luck': 0,
            },
            'rusty key': {
                'stamina': 0,
                'skill': 0,
                'luck': 0,
            },
            'leather armor': {
                'stamina': 2,
                'skill': 0,
                'luck': 0,
            },
            'short-sword': {
                'stamina': 0,
                'skill': 2,
                'luck': 0,
            },
            'daggers': {
                'stamina': 0,
                'skill': 3,
                'luck': 0,
            }
        }
        self.RAND_LOCATIONS = {

        }
        self.IMAGES = {
            'introduction': ''
        }
        self.introduction_str = ''

    def run(self):
        self.player = Player(self, self.dm)

        self.go_to_page(0)

    def add_item_to_world(self, new_items_dict):
        self.ITEMS.update(new_items_dict)

    def add_imgs_to_world(self, new_imgs_dict):
        self.IMAGES.update(new_imgs_dict)

    def add_randomizable_locations_to_world(self, new_randomizable_locations_dict):
        self.RAND_LOCATIONS.update(new_randomizable_locations_dict)

    def get_player_action(self, expected_answers, answer_format=str):
        while True:
            player_action = self.dm.display(question=(None, answer_format))  # answer_format = str | int | float
            ran_command = False

            if player_action.upper() in expected_answers:
                return player_action.upper()

            for aliases in self.PLAYER_COMMANDS.values():
                if player_action.lower() in aliases or ('{' in player_action and self.player.name == 'POF_ADMIN'):
                    self.handle_player_command(player_action)
                    ran_command = True

            if not ran_command:
                self.dm.display(f'{Fore.RED}That command is not recognized{Fore.RESET}, you have to choose from the '
                                f'options{expected_answers}, explained above or choose one of the base commands. If '
                                f'this is your first time playing, or you don\'t know what to do, type `help` and then '
                                f'press `enter`.')

    def handle_player_command(self, player_command):
        if player_command in self.PLAYER_COMMANDS['?']:
            self.help_message()

        elif player_command in self.PLAYER_COMMANDS['@']:
            self.player.show_inventory()

        elif player_command in self.PLAYER_COMMANDS['!']:
            self.player.die('at your own hands, the strain of continuing too much for you to bare')
            self.exit_world()

        elif player_command in self.PLAYER_COMMANDS['#']:
            if '+' in player_command or '^' in player_command or '*' in player_command:
                self.player.show_stats(show_explanation=True)

            else:
                self.player.show_stats()

        elif player_command in self.PLAYER_COMMANDS['~']:
            self.player.eat()

        elif player_command in self.PLAYER_COMMANDS['$']:
            self.player.flip_coin()

        elif player_command in self.PLAYER_COMMANDS['>']:
            self.dm.display(table=self.PLAYER_COMMANDS_TABLE)

        elif player_command in self.PLAYER_COMMANDS['*']:
            speed = self.dm.display(question=('What do you want to change the speed to? Set it to 0 to remove it. '
                                              'The speed that you set here is the pause in seconds that will be '
                                              'applied', float))
            self.dm.pause_time = speed

        elif self.player.name == 'POF_ADMIN' and '{' in player_command:
            try:
                self.go_to_page(int(player_command.replace('{', '').strip()))

            except ValueError:
                self.player.name = player_command.replace('{', '').strip()

    def go_to_page(self, page_number):
        if page_number == 0:
            pass

        else:
            self.dm.display(f"that's not a page ({page_number}), something's gone terribly wrong!")
            self.get_player_action(())
            self.exit_world()

    def fight(self, enemies):
        keep_fighting = True

        def check_dead():
            global keep_fighting

            for enemy in enemies:
                if enemy.is_dead():
                    self.dm.display(f'You have killed the {enemy.name}!')
                    enemy.die()
                    enemies.remove(enemy)
                    models.remove(enemy)

            if len(enemies) == 0:
                self.dm.display(('You have won the fight!', ' '))
                keep_fighting = False
                return True

            if self.player.is_dead():
                if len(enemies) == 1:
                    self.player.die(f'at the hands of the {enemies[0].name}')

                else:
                    self.player.die(f'in your fight with the {str(enemy.name for enemy in enemies[:-1])[1:-1]} and the '
                                    f'{enemies[-1].name}')

                keep_fighting = False
                self.exit_world()

        models = enemies.copy()
        models.append(self.player)

        while keep_fighting:
            for attacker_index in range(len(enemies)):
                self.dm.display(card=models)
                enemy_attack = sum(self.dm.roll_dice([0, 5], 
                                                     (2, (f'{proper(enemies[attacker_index].name)} attack roll',
                                                          f'{proper(enemies[attacker_index].name)} attack roll')),
                                                     'dice'))
                enemy_attack += enemies[attacker_index].calculate_total_attribute('skill')

                player_attack = sum(self.dm.roll_dice([0, 5], (2, (f'{proper(self.player.name)} attack roll',
                                                      f'{proper(self.player.name)} attack roll')), 'dice'))
                player_attack += self.player.calculate_total_attribute('skill')

                self.dm.display(' ', table=((f'{proper(enemies[attacker_index].name)}\'s total attack score',
                                             f'{proper(self.player.name)}\'s total attack score'),
                                            (enemy_attack, player_attack)))

                if enemy_attack == player_attack:
                    self.dm.display(f'You and the {enemies[attacker_index].name} both failed to injure each other.')

                elif enemy_attack > player_attack:
                    self.dm.display(f'The {enemies[attacker_index].name} injured you!')
                    self.player.change_statistics(stamina_change=-2)

                    if self.dm.display(
                            options=(('%', 'D'), ('Would you like to test your luck?', 'Take the damage.'))) in \
                            self.PLAYER_COMMANDS['%']:
                        luck_check = self.player.test_luck()

                        if luck_check:
                            self.player.change_statistics(stamina_change=2)

                        else:
                            self.player.change_statistics(stamina_change=-2)

                    if check_dead():
                        return

                elif enemy_attack < player_attack:
                    self.dm.display(f'You injured the {enemies[attacker_index].name}.')
                    enemies[attacker_index].change_statistics(stamina_change=-2)

                    if self.dm.display(options=(('%', 'D'), 
                                                ('Would you like to test your luck?', 
                                                 'Do the damage.'))) in self.PLAYER_COMMANDS['%']:
                        luck_check = self.player.test_luck()

                        if luck_check:
                            enemies[attacker_index].change_statistics(stamina_change=-2)

                        else:
                            enemies[attacker_index].change_statistics(stamina_change=2)

                    if check_dead():
                        return

    def exit_world(self):
        del self.player

        self.dm.exit_program()

    def introduction(self):
        intro_str = [
                     f'Part story, part game, this is an adventure in which YOU are the',
                     f'hero... enter the {Fore.RED}{self.WORLD_NAME}{Style.RESET_ALL}:',
                     f' ',
                     *self.introduction_str
                    ]

        return intro_str

    def help_message(self):
        self.dm.display(title='HELP PAGE', input_string=
                        (f'\nWelcome to the {self.GAME_NAME} game {self.WORLD_NAME} help page, where you will become '
                         f'accustomed with the mechanics of the game and learn how to play. {self.GAME_NAME} is a game '
                         f'of exploration, through mystical worlds of magic and monsters.',
                         ' ',
                         f'The progression of the game is simple, a section of a story will be read to you, until a '
                         f'decision needs to be made, then you will need to decide what to do, if you choose wisely '
                         f'then you may lead the journey to victory, otherwise you foolishness will result in your '
                         f'defeat. Once you have made a decision you will type it into the prompt and click enter. You '
                         f'will be given a list of single-character long option to choose from. Whenever you need to '
                         f'make a decision you can also run any of a list of preset commands found in a table below, '
                         f'along with a description of what they do. ',
                         ' ',
                         f'Sometimes you may need to test your luck, testing your luck can either result in you being '
                         f'lucky, or unlucky, and can change the outcome of the journey. But, whenever you test your '
                         f'luck, no matter if you where or not, your luck will decrease, if it reaches 0 then you will '
                         f'no longer be able to test your luck.',
                         ' ',
                         f'During the adventure you will likely encounter many foes, some of which you will '
                         f'fight. When you fight, round after round of battling will occur, until one of you either '
                         f'dies or runs away. In each round two dice will be rolled for each attacker, and added to '
                         f'their skill scores.Then, whoever has the higher skill score wounds the other attacker, '
                         f'causing them to take 2 point from their stamina. Whenever you are wounded you may test your '
                         f'luck, if you are lucky you take no damage, otherwise you take an additional two damage. '
                         f'Furthermore, whenever you wound an attacker you may test your luck, if you are lucky you '
                         f'deal an additional two damage, otherwise you instead deal no damage.',
                         ' ',
                         f'In this game you have three attributes, stamina, skill, and luck. Each is described in '
                         f'depth below. You will also have an inventory, containing all of your gold, provisions, and '
                         f'other items and clothing. You start out with rudimentary equipment, but during your journey '
                         f'you can find more, which can give you bonuses to your stamina, skill, and luck scores. Your '
                         f'provisions are the food that you carry, you can eat provisions to increase your stamina '
                         f'when it is below normal.',
                         ' '),
                        table=(('Stamina', 'Skill', 'Luck'),
                               ('Your health, and ability to continue. If your stamina ever reaches 0 then you will '
                                'die. Throughout your adventure your stamina will decrease as you lose fights, hurt '
                                'yourself, or become injured in any way. You will be able to increase your stamina by '
                                'eating, resting, or through any other healing means.',

                                'Your ability to perform physical tasks, fight and use equipment. As you don more '
                                'advanced tools, train yourself, and learn new things your skill will increase. When '
                                'you fight enemies it is your skill that will decide how swiftly you can cut them '
                                'down, and will be the deciding factor between success and failure in all physical '
                                'feats.',

                                'Your overall chance of coming upon good fortune and the likeliness of your success in '
                                'different situations. Luck is a magical force that can be very helpful, but if you '
                                'test your luck too much it will run out. Being lucky will let you inflict more damage '
                                'on enemies, make you more likely to avoid traps, and will lead you to hidden '
                                'treasures.')))

        self.dm.display(
            f'Below is a table of commands and a description on the right of what they will do if you call them. '
            f'Some commands have aliases, and they are seperated by commas, but are on the right square brackets.',
            table=self.PLAYER_COMMANDS_TABLE)
