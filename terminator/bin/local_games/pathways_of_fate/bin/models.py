from bin.utils import *
from bin.interface import random, Fore


class Player:
    def __init__(self, world, display_machine):
        self.world = world
        self.dm = display_machine
        self.name = self.dm.display(question=('What is your name adventurer?', str)).strip()

        self.dm.display(title='CHARACTER CREATION', input_string=
                        f'{self.name}, welcome to the {self.world.WORLD_NAME}. But before you begin, your character '
                        f'still needs to be fleshed out... you need to generate your stamina, skill, and luck scores. '
                        f'Once, they have been randomly rolled you will have the ability to add an additional three '
                        f'points to one score and two points to another score of your choice. Choose wisely, as your '
                        f'decision here may be the difference between success and failure, or even life and death '
                        f'later on in your journey. You will also start your journey with some basic leather armour '
                        f'and clothing, a short-sword, your life savings in gold coinage, and some provisions.')

        self.stamina = self.dm.roll_dice((1, 12), (1, ['Stamina']))[0]
        self.skill = self.dm.roll_dice((1, 5), (1, ['Skill']))[0]
        self.luck = self.dm.roll_dice((0, 6), (1, ['Luck']))[0]

        choice = self.dm.display((' ', f'Which skill would you like to {Fore.GREEN}add{Fore.RESET} three additional '
                                       f'points to?'),
                                 options=(('S', 'K', 'L'), ('Your stamina?', 'Your skill?', 'Your luck?')))

        if choice == 'S':
            self.stamina += 3

        elif choice == 'K':
            self.skill += 3

        if choice == 'L':
            self.luck += 3

        choice = self.dm.display((' ', f'Which skill would you like to {Fore.GREEN}add{Fore.RESET} two additional '
                                       f'points to?'),
                                 options=(('S', 'K', 'L'), ('Your stamina?', 'Your skill?', 'Your luck?')))

        if choice == 'S':
            self.stamina += 2

        elif choice == 'K':
            self.skill += 2

        if choice == 'L':
            self.luck += 2

        self.inventory = {}

        for item in self.world.ITEMS:  # creates an empty inventory
            self.inventory[item] = 0

        self.inventory['gold coins'] = 7
        self.inventory['provisions'] = 6
        self.inventory['leather armor'] = 1
        self.inventory['short-sword'] = 1

        self.dm.display(
            (f'Your stamina is your health, and your ability to keep going. Your skill, your dexterity, speed, and '
             f'mastery of battle. And in the magical world of the {self.world.WORLD_NAME}, luck is a tangible '
             f'force, it\'s the chance of favourable things happening to you and your good fortune as a person. All '
             f'of these attributes will be tested as you progress through your journey, as well as your wisdom and '
             f'intelligence. You will have to find ways to boost and regain your stamina and luck as they wear out, '
             f'or you will surely die. Good luck on your journeys, and may luck be with you, {self.name}.',
             ' '))

    def is_dead(self):
        return self.stamina < 1

    def die(self, cause=None, message_preset=None):
        self.skill = self.stamina = self.luck = 0

        if message_preset is None:
            message_number = random.randint(0, 5)

        else:
            message_number = message_preset

        if cause.endswith('.'):
            cause = cause[:-1]

        self.dm.display(' ')

        if message_number == 0:
            self.dm.display(
                f'Though you tried, {self.name}, you have met your end {cause.strip()}. Your journey stops here, where '
                f'your legacy shall slowly vanish, and your purpose forgotten. This is the end, your story stops '
                f'here.')

        elif message_number == 1:
            self.dm.display(
                f'Despite your efforts, {self.name}, your journey comes to an end {cause.strip()}. Here, your legacy '
                f'fades away gradually, and your purpose is lost and forgotten. Your story ends here.')

        elif message_number == 2:
            self.dm.display(
                f'Although you tried your best, {self.name}, you have reached the end of your journey {cause.strip()}. '
                f'Your legacy will slowly vanish, and your purpose will be forgotten. This is where your story '
                f'comes to a close.')

        elif message_number == 3:
            self.dm.display(
                f'Your efforts have been in vain, {self.name}, as your journey has put an end {cause.strip()}. Your '
                f'legacy will slowly fade, and your purpose will be forgotten. This is the end of your story.')

        elif message_number == 4:
            self.dm.display(
                f'Although you have tried, {self.name}, your journey ends here {cause.strip()}. Your legacy will '
                f'slowly disappear, and your purpose will be forgotten. This is where your story concludes.')

        elif message_number == 5:
            self.dm.display(
                f'Your journey has reached a conclusion, {self.name}, your end has been brought about {cause.strip()}. '
                f'Your legacy will dissipate slowly, and your purpose will be forgotten. This is where your story '
                f'ends.')

        elif message_number == 6:
            self.dm.display(
                f'You feel your life slipping away. You regret your decisions, wishing you had have made smarter '
                f'moves. But it\'s too late now, as the darkness closes in and you take your last breath, forever '
                f'lost in a soon to be forgotten place, where your body will rot along with your legacy and '
                f'purpose.')

        self.world.exit_world()

    def change_inventory(self, add_list=None, remove_list=None):
        if add_list is not None:
            if isinstance(add_list, str):
                self.inventory[add_list] += 1

            else:
                for item in add_list:
                    self.inventory[item] += 1

        if remove_list is not None:
            if isinstance(add_list, str):
                self.inventory[add_list] -= 1

            else:
                for item in add_list:
                    self.inventory[item] -= 1

    def has_item(self, item_name, find_amount=False):
        if find_amount:
            return self.inventory.get(item_name, 0)

        else:
            return item_name in self.inventory

    def change_statistics(self, stamina_change=0, skill_change=0, luck_change=0, silence=False):
        if stamina_change != 0:
            self.stamina += stamina_change

            if not silence:
                if stamina_change < 0:
                    self.dm.display((' ',
                                     f'{self.name}\'s stamina has been {Fore.RED}decreased{Fore.RESET} by '
                                     f'{abs(stamina_change)}.',
                                     ' '))

                else:
                    self.dm.display((' ',
                                     f'{self.name}\'s stamina has been {Fore.GREEN}increased{Fore.RESET} by '
                                     f'{abs(stamina_change)}.',
                                     ' '))

        if self.stamina < 0:
            self.stamina = 0

        if skill_change != 0:
            self.skill += skill_change

            if not silence:
                if skill_change < 0:
                    self.dm.display((' ',
                                     f'{self.name}\'s skill has been {Fore.RED}decreased{Fore.RESET} by '
                                     f'{abs(skill_change)}',
                                     ' '))

                else:
                    self.dm.display((' ',
                                     f'{self.name}\'s skill has been {Fore.GREEN}increased{Fore.RESET} by '
                                     f'{abs(skill_change)}',
                                     ' '))

        if self.skill < 0:
            self.skill = 0

        if luck_change != 0:
            self.luck += luck_change

            if not silence:
                if stamina_change < 0:
                    self.dm.display((' ',
                                     f'{self.name}\'s luck has been {Fore.RED}decreased{Fore.RESET} by '
                                     f'{abs(luck_change)}',
                                     ' '))

                else:
                    self.dm.display((' ',
                                     f'{self.name}\'s luck has been {Fore.GREEN}increased{Fore.RESET} by '
                                     f'{abs(luck_change)}',
                                     ' '))

        if self.luck < 0:
            self.luck = 0

    def calculate_total_attribute(self, attribute, attribute_change=0):
        if attribute == 'stamina':
            for item in self.inventory:
                if self.inventory[item] != 0:
                    attribute_change += self.world.ITEMS.get(item, 0)['stamina']

            return self.stamina + attribute_change

        elif attribute == 'skill':
            for item in self.inventory:
                if self.inventory[item] != 0:
                    attribute_change += self.world.ITEMS.get(item, 0)['skill']

            return self.skill + attribute_change

        elif attribute == 'luck':
            return self.luck + attribute_change

    def test_luck(self):
        if self.luck <= 0:
            print(f'\n   You have been {Fore.RED}unlucky{Fore.RESET}!\n')

            return False

        self.change_statistics(luck_change=-1, silence=True)

        roll = self.dm.roll_dice((1, 6), (1, ['Testing Luck']))[0]

        if roll <= self.luck + 1:
            print(f'\n   You have been {Fore.GREEN}lucky{Fore.RESET}!\n')

        else:
            print(f'\n   You have been {Fore.RED}unlucky{Fore.RESET}!\n')

        return roll <= self.luck + 1

    def flip_coin(self):
        if self.inventory['gold coins'] != 0:
            self.dm.roll_dice(form='coin')

        else:
            self.dm.display(f'{Fore.RED}You have no coins to flip!')

    def eat(self, number_of_provisions=1):
        if self.inventory['provisions'] == 0:
            self.dm.display(f'{Fore.RED}You don\'t have any provisions to eat!')
            return

        number_of_eaten_provisions = 0

        if self.inventory['provisions'] != 0:
            for provisions in range(number_of_provisions):
                if self.inventory['provisions'] > 0:
                    self.inventory['provisions'] -= 1
                    number_of_eaten_provisions += 1
                    self.change_statistics(stamina_change=1, silence=True)

                else:
                    self.dm.display(f'{Fore.RED}You don\'t have any more provisions to eat!')
                    break

            self.dm.display(f'You ate {number_of_eaten_provisions} of your provisions, you have '
                            f'{self.inventory["provisions"]} left and your stamina score is {self.stamina}.')

    def show_stats(self, show_explanation=False):
        self.dm.display(f'{self.name.upper()}\'s STATISTICS: ',
                        table=(('Stamina', 'Skill', 'Luck'),
                               (f'{self.stamina} (total: {self.calculate_total_attribute("stamina")})',
                                f'{self.skill} (total: {self.calculate_total_attribute("skill")})',
                                f'{self.luck} (total: {self.calculate_total_attribute("luck")})')))

        if show_explanation:
            self.dm.display(f'Your total statistics include all of the effects of items that you have, such as the '
                            f'increase in skill you might get from a sword, or the increase in stamina you might get '
                            f'from a helmet.')

    def show_inventory(self):
        column_one = [item if self.inventory[item] != 0 else None for item in self.inventory.keys()]
        column_one = list(filter(lambda item: item is not None, column_one))

        column_two = [f'#({self.inventory[item]}) Stamina change: {self.world.ITEMS[item]["stamina"]}, skill change: '
                      f'{self.world.ITEMS[item]["skill"]}, luck benefit: {self.world.ITEMS[item]["luck"]}.' if
                      self.inventory[item] != 0 else None for item in self.inventory.keys()]
        column_two = list(filter(lambda item: item is not None, column_two))

        self.dm.display(f'{self.name.upper()}\'S INVENTORY: ', table=(column_one, column_two))


class Enemy:
    def __init__(self, display_machine, name, stamina, skill, luck=0):
        self.name = name
        self.stamina = stamina
        self.skill = skill
        self.luck = luck
        self.dm = display_machine

    def is_dead(self):
        return self.stamina < 1

    def die(self, cause=None):
        self.skill = self.stamina = self.luck = 0

        if cause is not None:
            self.dm.display(f'{proper(self.name)} died {cause}')

    def calculate_total_attribute(self, attribute, attribute_change=0):
        if attribute == 'stamina':
            return self.stamina + attribute_change

        elif attribute == 'skill':
            return self.skill + attribute_change

        elif attribute == 'luck':
            return self.luck + attribute_change

    def change_statistics(self, stamina_change=0, skill_change=0, luck_change=0):
        self.stamina += stamina_change

        if self.stamina < 0:
            self.stamina = 0

        self.skill += skill_change

        if self.skill < 0:
            self.skill = 0

        self.luck += luck_change

        if self.luck < 0:
            self.luck = 0
