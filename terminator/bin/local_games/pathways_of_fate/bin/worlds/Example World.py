from bin.world_base import *


class World(WorldBase):
    def __init__(self, display_machine, game_name, running_sub_world=False,
                 world_name='Put The Name Of The Story Here!'):
        super().__init__(display_machine, game_name, running_sub_world, world_name)
        self.add_item_to_world({  # You can give the players items, add them, and their effects here:
            'ring of stone': {
                'stamina': 5,
                'skill': 0,
                'luck': -3,
            },
            'goblin\'s thumb': {
                'stamina': 0,
                'skill': 0,
                'luck': 1,
            },
        })
        self.add_randomizable_locations_to_world({
            # These can be used to randomize the names of places in the story, you can refrence them later on in
            # f-strings using something like: `{self.RAND_LOCATIONS["the name, i.e. village"]}`.
            'village': random.choice(('Damalville', 'Gif-Town', 'Willowvale')),
        })
        self.add_imgs_to_world({
            # credits to Targon from https://ascii.co.uk/art/forest for the base image of the intro image
            'introduction': f' Fill these text boxes with copy and pasted ASCII images, you can add coloring with the '
                            f' colorama module (i.e.: {Fore.RED}, {Style.RESET_ALL}). You need to have an '
                            f' `introduction` image, but can also have any other image that you want. ',
            'pet_rock': f' ༼ つ ◕_◕ ༽つ ',
            'green_bold_pet_rock': f'{Fore.GREEN}{Back.BLUE}{Style.BRIGHT} ༼ つ ◕_◕ ༽つ {Style.RESET_ALL}{Fore.RED}≈≈≈≈'
            # This, above, has bold green text, with a blue background, and some non-bold, red waves at the end.
        })
        self.introduction_str = [
            f'Put the introduction to the world here, after being shown this, the reader will be given the choice to '
            f'take up the quest (which you need to introduce to the reader here) or leave. '
            # At the end of each string make sure there is a space, otherwise your words will meld together!
        ]

    def go_to_page(self, page_number):
        if page_number == 0:
            choice = self.dm.display(
                f'Put some story here! You can reference those random locations: {self.RAND_LOCATIONS["village"]}, '
                f'and other things, like the player\'s name (using single quote marks needs a backslash beforehand): '
                f'Hello, {self.player.name}, it\'s good to see that you have {self.player.luck} luck! ',
                ascii_image=self.IMAGES['pet_rock'],  # You can add the images from before
                options=(('N', 'E', 'S', 'W'),  # You can have any number of single character options here
                         ('Go along the northward path.',  # Here, below, you give a description of what each choice
                          'Eat some food.',  # will have the player do, but do not say the outcome.
                          'Go south for a jog.',
                          'Wander around aimlessly.')
                         )
            )

            if choice == 'N':  # Now, depending on the choice, do something different
                self.go_to_page(1)  # This will take the player to page 1 of the world, they are on page 0.

            elif choice == 'E':
                self.go_to_page(2)

            elif choice == 'S':
                self.go_to_page(3)

            elif choice == 'W':
                self.go_to_page(4)

        elif page_number == 1:
            choice = self.dm.display(
                ['You find an ugly goblin! '],
                options=(('F', 'H'), ('Fight the goblin.', 'Run to find a place to hide.'))
            )

            if choice == 'F':
                self.dm.display('You take a deep breath and ready yourself for the attack. ')
                self.fight([Enemy(self.dm, 'Ugly Goblin', 4, 2, 0)])  # It goes name, stamina, skill, luck.
                # This will make the player fight an enemy, if they die the world will end, otherwise they will move on
                # to here:
                self.player.change_inventory(['goblin\'s thumb'])
                # This will give the player the item with that name that you defined above

                self.dm.display(
                    'You are the luckiest player of all time. You won!, I\'m not sure how you did that... cheater? ')
                # The story ends now, since there is no code. But, don't just leave it empty, you need to add the
                # following line:
                self.dm.exit_program()

            elif choice == 'H':
                self.dm.display(['Loser! the goblin stabs you from behind.'])
                self.player.die('a stab in the back. (the reason for dying)')

        elif page_number == 2:
            self.dm.display('Something happens, blady, blady, blah.')
            self.go_to_page(3)

        elif page_number == 3:
            choice = self.dm.display(('Even more, intriguing storyline ',
                                      ' ',  # This makes an empty line, for splitting up paragraphs.
                                      'You find a portal!!! '),
                                     options=(('P', 'J'), ('Enter the portal.', 'Walk past it.')))
            self.player.change_statistics(luck_change=1, stamina_change=-1)
            # You change the player's attributes like this

            if choice == 'P':
                self.go_to_page(0)

            elif choice == 'J':
                self.go_to_page(4)

        elif page_number == 4:
            self.dm.display(('Put the story ending here. ',
                             ' ',  # This makes an empty line, for splitting up paragraphs.
                             'And, then they died... a sad ever after. '))
            self.player.die('starved to death in an endless labyrinth. (put the reason for death)', message_preset=1)
            # you can also set a `message_preset`, if you take a look at the code for the `self.player.die` function
            # you can read what all of the presets sounds like.

        else:  # keep this part here just incase, no need to edit it.
            self.dm.display(f"that's not a section ({page_number}), something's gone terribly wrong.")
            self.get_player_action(())
