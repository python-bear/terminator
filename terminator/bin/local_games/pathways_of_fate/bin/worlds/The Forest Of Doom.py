from bin.world_base import *


class World(WorldBase):
    def __init__(self, display_machine, game_name, running_sub_world=False, world_name='Forest Of Doom'):
        super().__init__(display_machine, game_name, running_sub_world, world_name)
        self.add_item_to_world({
            'ring of stone': {
                'stamina': 5,
                'skill': 0,
                'luck': -3,
            },
            'vulture\'s key': {
                'stamina': 0,
                'skill': 0,
                'luck': 0,
            },
        })
        self.add_randomizable_locations_to_world({
            'home': random.choice(('Harrowdale', 'Glenborough', 'Willowvale', 'Fernholm', 'Oakshire', 'Amberfield')),
            'second village': random.choice(('Kifgar', 'Rifkar', 'Vikgar', 'Kargif', 'Kifrag')),
            'backrooms': random.choice(('Bithlon', 'Limbo', 'Bardon', 'Fields Of Asphodel', 'Barzakh'))
        })
        self.add_imgs_to_world({
            # credits to Targon from https://ascii.co.uk/art/forest for the base image of the intro image
            'introduction': f' {Style.RESET_ALL}{Fore.WHITE}.. ........... .............  ........... . ..... ........ '
                            f'.......\n {Style.RESET_ALL}{Fore.WHITE}......  ....................%.... .... ..... .....'
                            f'....%............\n {Style.RESET_ALL}{Fore.WHITE}.{Fore.GREEN}@@@{Fore.WHITE} ........ '
                            f'{Fore.GREEN}@@{Fore.WHITE}.... {Fore.GREEN}@@@@{Fore.WHITE}  . ..........................'
                            f'..  {Style.BRIGHT}{Fore.GREEN}*  {Style.RESET_ALL}{Fore.WHITE}.....\n {Style.RESET_ALL}'
                            f'{Fore.WHITE}....{Fore.GREEN}@@{Fore.WHITE} ..... {Fore.GREEN}@{Fore.WHITE} .... '
                            f'{Fore.GREEN}@{Fore.WHITE} .............   ....... .....{Fore.GREEN};{Fore.WHITE} .... '
                            f'{Style.BRIGHT}{Fore.GREEN}*** {Style.RESET_ALL}{Fore.WHITE}.....\n {Style.RESET_ALL}'
                            f'{Fore.WHITE}.....{Fore.GREEN}\\@\\{Fore.WHITE}....{Fore.GREEN}@{Fore.WHITE} .... '
                            f'{Fore.GREEN}@{Fore.WHITE} ............................. {Fore.GREEN}#{Fore.WHITE}  .. '
                            f'{Style.BRIGHT}{Fore.GREEN}*****  {Style.RESET_ALL}{Fore.WHITE}...\n {Style.RESET_ALL}'
                            f'{Fore.WHITE} {Fore.GREEN}@@@.. {Fore.GREEN}@@@@@{Fore.WHITE}  {Fore.GREEN}@@@@@@___'
                            f'{Fore.WHITE}.. ....... ...%..... ...  {Fore.GREEN}(###)  {Style.BRIGHT}{Fore.GREEN}******'
                            f'*  {Style.RESET_ALL}{Fore.WHITE}..\n {Style.RESET_ALL}{Fore.WHITE}....{Fore.GREEN}@-@'
                            f'{Fore.WHITE}..{Fore.GREEN}@{Fore.WHITE} ..{Fore.GREEN}@{Fore.WHITE}......{Fore.GREEN}@@@'
                            f'\\{Fore.WHITE}...... %...... ....... {Fore.GREEN}<## ####>{Style.BRIGHT}{Fore.GREEN}*****'
                            f'***  {Style.RESET_ALL}{Fore.WHITE}.\n {Style.RESET_ALL}{Fore.WHITE}  {Fore.GREEN}@@@@\\'
                            f'{Fore.WHITE}...{Fore.GREEN}@ {Fore.GREEN}@{Fore.WHITE} ........{Fore.GREEN}\\@@@@'
                            f'{Fore.WHITE} ..... ...... ....... {Fore.GREEN}(###){Style.BRIGHT}{Fore.GREEN}***********'
                            f'\n {Style.RESET_ALL}{Fore.WHITE}....%..{Fore.GREEN}@  @@ /@@@@@{Fore.WHITE} . ....... ...'
                            f'............{Fore.GREEN}<###########> {Style.BRIGHT}{Fore.GREEN}*******\n '
                            f'{Style.RESET_ALL}{Fore.WHITE}...... .{Fore.GREEN}@-@@@@{Fore.WHITE} ...{Fore.GREEN}V'
                            f'{Fore.WHITE}......     .... %.......... {Fore.GREEN}(#######){Style.BRIGHT}{Fore.GREEN}**'
                            f'***** ***\n {Style.RESET_ALL}{Fore.WHITE}...... .  {Fore.GREEN}@@{Fore.WHITE} .. ..'
                            f'{Fore.GREEN}v{Fore.WHITE}.. .. . {Fore.YELLOW}[ ]{Fore.WHITE} ............{Fore.GREEN}<##'
                            f'#############>{Style.BRIGHT}{Fore.GREEN}*******\n {Style.RESET_ALL}{Fore.WHITE}......... '
                            f'{Fore.GREEN}@@{Fore.WHITE} .... ........ {Fore.YELLOW}[{Fore.RED}^^,{Fore.WHITE}   ......'
                            f'...   {Fore.GREEN}(## ######){Style.BRIGHT}{Fore.GREEN}***** ****\n {Style.RESET_ALL}'
                            f'{Fore.WHITE}..%..... {Fore.GREEN}@@{Fore.WHITE} .. .%.... . .. {Fore.RED}(   `-;'
                            f'{Fore.WHITE}  .... {Fore.GREEN}<###################> {Style.BRIGHT}{Fore.GREEN}****\n '
                            f'{Style.RESET_ALL}{Fore.WHITE}. .... . {Fore.GREEN}@@{Fore.WHITE} . .... .. {Fore.RED}_'
                            f'{Fore.WHITE}  .. {Fore.RED}`;;~~{Fore.WHITE} ......... {Fore.GREEN}(#############)'
                            f'{Style.BRIGHT}{Fore.GREEN}********\n {Style.RESET_ALL}{Fore.WHITE}.... ... {Fore.GREEN}@@'
                            f'{Fore.WHITE} ... ..   {Fore.RED}/(______);{Fore.WHITE} .. ....{Fore.GREEN}<##############'
                            f'##  #####>{Style.BRIGHT}{Fore.GREEN}***\n {Style.RESET_ALL}{Fore.WHITE}. .... ..'
                            f'{Fore.GREEN}@@@{Fore.WHITE} ...... {Fore.RED}(         ({Fore.WHITE}  .........'
                            f'{Fore.GREEN}(##################){Style.BRIGHT}{Fore.GREEN}*****\n {Style.RESET_ALL}'
                            f'{Fore.WHITE}......... {Fore.GREEN}@@@{Fore.WHITE}  ....  {Fore.RED}|:------( )'
                            f'{Fore.WHITE}  .. {Fore.GREEN}<##########################>{Style.BRIGHT}{Fore.GREEN}**\n '
                            f'{Style.RESET_ALL}{Fore.WHITE}@@@@ ....{Fore.GREEN}@@@{Fore.WHITE}  ...  {Fore.RED}_//'
                            f'{Fore.WHITE} ...... {Fore.RED}\\ \\{Fore.WHITE} ...... {Fore.GREEN}(###   ##############)'
                            f'{Style.BRIGHT}{Fore.GREEN}****\n {Style.RESET_ALL}{Fore.WHITE}@@@@@@@  {Fore.GREEN}@@@@@'
                            f'{Fore.WHITE} .. {Fore.RED}/ /{Fore.WHITE}@@@@@@@@@ {Fore.MAGENTA}vv  {Fore.GREEN}<#######'
                            f'#######################>\n {Style.RESET_ALL}{Fore.WHITE}@@@@@@@ {Fore.GREEN}@@@@@@@'
                            f'{Fore.WHITE} @@@@@@@@@@@@@@@@@@@ .....{Fore.WHITE} @@@@@@  @@@@@@@  @@@@   @\n '
                            f'{Style.RESET_ALL}{Fore.WHITE}@@@@@@{Fore.GREEN}###@@@@@{Fore.GREEN}###{Fore.WHITE} @@@@@@'
                            f'@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n {Style.RESET_ALL}{Fore.WHITE}@@@@@@@@'
                            f'{Fore.GREEN}###{Fore.WHITE}@{Fore.GREEN}##{Fore.WHITE}@@ @@@@@@@@@@@@@@@@@@@@@ @@@@@   @@'
                            f'@@@@@@@@@@@@@@@@@@\n {Style.RESET_ALL}{Fore.WHITE}@@@@@@@@@@@{Fore.GREEN}###{Fore.WHITE} '
                            f'@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@\n {Style.RESET_ALL}{Fore.WHITE}@@@@@'
                            f'@@@@{Fore.GREEN}#####{Fore.WHITE}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',

            'valley': f'     .                 .-.    .  {Fore.YELLOW}_{Fore.RESET}   {Fore.WHITE}{Style.BRIGHT}*'
                      f'{Style.RESET_ALL}     _   .\n           {Fore.WHITE}{Style.BRIGHT}*{Style.RESET_ALL}          /'
                      f'   \\     {Fore.YELLOW}(_){Fore.RESET}      _/ \\       {Fore.WHITE}{Style.BRIGHT}*'
                      f'{Style.RESET_ALL}    .\n          _    .   .--\'\\/\\_ \\            /    \\  {Fore.WHITE}'
                      f'{Style.BRIGHT}*{Style.RESET_ALL}    ___\n      {Fore.WHITE}{Style.BRIGHT}*{Style.RESET_ALL}  / '
                      f'\\_    _/ ^      \\/\\\'__       /\\/\\  /\\  __/   \\ {Fore.WHITE}{Style.BRIGHT}*'
                      f'{Style.RESET_ALL}\n        /    \\  /    .\'   _/  /  \\  {Fore.WHITE}{Style.BRIGHT}*'
                      f'{Style.RESET_ALL}\' /    \\/  \\/ .`\'\\_/\\   .\n   .   /\\/\\  /\\/ :\' __  ^/  ^/    `--./.'
                      f'\'  ^  `-.\\ _    _:\\ _\n      /    \\/  \\  _/  \\-\' __/.\' ^ _   \\_   .\'\\   _/ \\ .  __/'
                      f' \\\n    /\\  .-   `. \\/     \\ / -.   _/ \\ -. `_/   \\ /    `._/  ^  \\\n   /  `-.__ ^   / .'
                      f'-\'.--\'    . /    `--./ .-\'  `-.  `-. `.  -  `.\n {Fore.GREEN}@{Fore.RESET}/        `.  / /  '
                      f'    `-.   /  .-\'   / .   .\'   \\    \\  \\  .-  \\{Fore.GREEN}%\n @&8jgs@@%% @)&@&(88&@.'
                      f'{Fore.BLUE}-_=_-=_-=_-=_-=_{Fore.GREEN}.8@% &@&&8(8%@%8)(8@%8 8%@)%\n @88:::&(&8&&8:::::%&`.'
                      f'{Fore.BLUE}~-_~~-~~_~-~_~-~~={Fore.GREEN}.\'@(&%::::%@8&8)::&#@8::::\n `::::::8%@@%:::::@%&8:`.'
                      f'{Fore.BLUE}=~~-{Fore.GREEN}.{Fore.BLUE}~~-{Fore.GREEN}.~~={Fore.GREEN}..~\'8::::::::&@8:::::&8:'
                      f'::::\'\n  `::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.\'\n',

            # Credits to VK from https://www.asciiart.eu/mythology/skeletons
            'skull': f'{Fore.WHITE}         .AMMMMMMMMMMA.          \n       .AV. :::.:.:.::MA.        \n      A\' :.. '
                     f'       : .:`A       \n     A\'..              . `A.     \n    A\' :.    :::::::::  : :`A    \n  '
                     f'  M  .    :::.:.:.:::  . .M    \n    M  :   ::.:.....::.:   .M    \n    V : :.::.:........:.:  :'
                     f'V    \n   A  A:    ..:...:...:.   A A   \n  .V  MA:.....:M.::.::. .:AM.M   \n A\'  .VMMMMMMMMM:.'
                     f':AMMMMMMMV: A  \n:M .  .`VMMMMMMV.:A `VMMMMV .:M: \n V.:.  ..`VMMMV.:AM..`VMV\' .: V  \n  V.  .:'
                     f'. .....:AMMA. . .:. .V   \n   VMM...: ...:.MMMM.: .: MMV    \n       `VM: . ..M.:M..:::M\'      '
                     f'\n         `M::. .:.... .::M       \n          M:.  :. .... ..M       \n {Fore.BLACK}VK'
                     f'{Fore.WHITE}       V:  M:. M. :M .V       \n          `V.:M.. M. :M.V\'       \n',

            'key': f'  {Fore.RED}ooo,    {Fore.WHITE}.---.                   \n {Fore.RED}o`  o   {Fore.WHITE}/    |\\_'
                   f'_______________  \n{Fore.RED}o`   \'oooo{Fore.WHITE}()  | ________   _   _) \n{Fore.RED}`oo   o` '
                   f'{Fore.WHITE}\\    |/        | | | |   \n  {Fore.RED}`ooo\'   {Fore.WHITE}`---\'         "-" |_|   '
                   f'\n',

            'tree': f'                    {Fore.GREEN}       .\u007B\u007D\u007D\u007D.\n                          '
                    f'\u007B\u007B\u007B(`)\u007D).\n                         \u007B((`))\u007D\u007D)\u007D)\n        '
                    f'               \u007B\u007D\u007D\u007D)\u007B(`)\u007B(\u007D\u007D\n                      '
                    f'\u007B\u007D\u007D\u007B\u007B(`)\u007D\u007B\u007B\u007B\u007B\u007B\n                     '
                    f'\u007B((`))\u007D\u007D\u007D()\u007D\u007D\u007D\u007D\u007D\n                    \u007B\u007B'
                    f'\u007B\u007B(`)\u007D\u007D\u007D\u007D\u007D[\u007B\u007B\u007B\u007D\u007D\n                   '
                    f' \u007B\u007B\u007B()\u007B\u007B(`)\u007D\u007D\u007D\u007B\u007B\u007D\u007D\u007D\u007D\n     '
                    f'                \u007B\u007B((`)   \u007B[((`))\'\n                      `""\'" {Fore.RED}|   |'
                    f'{Fore.GREEN} "\'"\'\n                      {Fore.YELLOW}(`)  {Fore.RED}/     \\\n                '
                    f'    {Fore.LIGHTGREEN_EX}~~~~~~~~~~~~~~~~~~~\n'
        })
        self.introduction_str = [
            f'Rumors have been spreading through the land of a growing evil in the {self.WORLD_NAME}. The '
            f'days are getting darker, winter has come in early this year, a gloomy cloud is gathering above '
            f'the {self.WORLD_NAME}, and dark creatures have been creeping through the night and been seen '
            f'hiding around the land. Civil unrest has spread like wildfire through your small village, '
            f'{self.RAND_LOCATIONS["home"]} and an assembly has been called in the community hall, to '
            f'which all must attend.',
            ' ',
            f'The villagers shuffle into their places in the community hall and hush their murmurs as the '
            f'village thane approaches the podium. His face is grave and lined with worry as he clears his '
            f'throat and begins speaking in a solemn voice.',
            ' ',
            f'"My beloved villagers," he says. "You are all aware of the darkness that creeps through the '
            f'woods to the East. It is a blight upon our land, and it threatens not only our village, but all '
            f'those around us. We cannot allow it to continue unchecked."',
            ' ',
            f'There is a murmur of agreement from the crowd, but also a sense of fear and uncertainty. The '
            f'thane pauses, looking out over the sea of faces before him.',
            ' ',
            f'"Therefore," he continues, "I am calling upon a brave volunteer to venture into the forest '
            f'to find and destroy this darkness. It will be a perilous journey, but it is one that must be '
            f'taken if we are to save our homes and our families. Who among you will step forward and take '
            f'up this noble quest?"',
            ' ',
            f'The room falls silent, all eyes turned to the front of the hall. The thane waits, his gaze '
            f'unwavering, but no one steps forward. A tense silence fills the air as the weight of the task '
            f'ahead seems to bear down upon the villagers. The thane\'s expression remains stern and '
            f'resolute, but there is a flicker of disappointment in his eyes as he realizes the depth of '
            f'their fear.',
            ' ',
            f'"I see," he says at last, his voice heavy with understanding. "This task is not one to be taken '
            f'lightly. But let us remember why we are here. We are here to protect our homes and our '
            f'families. And so, to whoever embarks on this journey and return victorious, a prize will be '
            f'granted of all that you ask!"',
            ' ',
            f'The room falls silent, all heads look around the hall, in search of who will step up for the '
            f'challenge. Will you take on this mortal quest in search of evil and darkness to vanquish it '
            f'from the land and save all from the forecasted doom?']

    def go_to_page(self, page_number):
        if page_number == 0:
            choice = self.dm.display(
                f'You\'ve collected all of your items, but you can\'t shake the feeling of dread that '
                f'weighs heavily on your chest. The thane\'s final speech and the cheering of the '
                f'villagers only served to remind you of the enormity of the task ahead. As you set off '
                f'eastward towards the village of {self.RAND_LOCATIONS["second village"]}, you venture through '
                f'the lush plains, drizzling rivers, and rolling hills of the natural landscape. As you '
                f'walk through the natural landscape, you can\'t help but feel a sense of peace and '
                f'tranquility. Yet, you know that the night in {self.RAND_LOCATIONS["second village"]} will '
                f'offer little respite for your journey. The villagers are wary of outsiders and will '
                f'likely charge you an exorbitant price for a bed in the dilapidated inn. But what other '
                f'choice do you have? The journey to the Forest of Doom is long, and you need your '
                f'strength to face the horrors that await you there. But for now the only thing that '
                f'lingers on you mind is the rumble of your belly, it\'s, well time for lunch!',
                ascii_image=self.IMAGES['valley'], options=(('T', 'P', 'W'),
                                                            ('Eat lunch and rest by the tree that is '
                                                             'nearby to the path.',
                                                             'Sit by the side of the path and eat.',
                                                             'Don\'t rest and eat while you continue '
                                                             'walking.')))

            if choice == 'T':
                self.go_to_page(1)

            elif choice == 'P':
                self.go_to_page(2)

            elif choice == 'W':
                self.go_to_page(3)

        elif page_number == 1:
            self.dm.display(
                ('As you walk off the beaten path to the tree, the fatigue from your journey finally catches up to '
                 'you. You sit down at the base of the tree and pull out a provision to have for lunch. As you '
                 'eat, the soothing shade of the tree and the gentle rustling of its leaves lull you into a '
                 'peaceful slumber.',
                 ' ',
                 'However, your rest is abruptly interrupted by a loud buzzing sound. As you open your '
                 'eyes, you realize with horror that there\'s a beehive dangling precariously above you! Quick, '
                 'test your luck to see if manage to escape from the bees unharmed.'),
                ascii_image=self.IMAGES['tree'])
            self.player.eat(2)
            action = self.get_player_action(self.PLAYER_COMMANDS['%'])

            lucky = self.player.test_luck()

            if lucky:
                self.dm.display(('Panic sets in as you jump up and run as fast as you can away from the tree, narrowly '
                                 'avoiding being stung by the angry bees. You sprint back to the safety of the path, '
                                 'gasping for breath and adrenaline coursing through your veins. ',
                                 ' ',
                                 'As you catch your breath, you take a moment to '
                                 'reflect on the close call. You realize that even in the peacefulness of nature, '
                                 'danger can still be lurking just around the corner. With renewed vigilance, you '
                                 'press on, determined to make it to your destination in one piece.'))

            else:
                self.dm.display(
                    ('Panic grips you as you jump up and run as fast as you can away from the tree, but it\'s too '
                     'late. The angry swarm of bees descends upon you, stinging you mercilessly all over your '
                     'body. You scream in agony as you sprint back to the path, your breaths coming in short gasps '
                     'and your adrenaline reaching an all-time high.',
                     ' ',
                     'As you collapse to the ground, tears streaming '
                     'down your face from the pain of the stings, you curse your luck. The once beautiful day has '
                     'turned into a nightmare, and you can feel your body reacting badly to the venom coursing '
                     'through your veins. ',
                     ' ',
                     'You take a moment to reflect on your foolishness, knowing that you should '
                     'have been more cautious. Danger lurks around every corner, and now you have paid the price '
                     'for your carelessness. ',
                     ' ',
                     'With a heavy heart and a body wracked with pain, you continue on your '
                     'journey, determined to push through the discomfort and make it to your destination. The road '
                     'ahead will be long and arduous, but you know that you cannot let this setback stop you. You '
                     'grit your teeth and set off, hoping that the worst is behind you.'))
                self.player.change_statistics(stamina_change=-1)
            self.go_to_page(4)

        elif page_number == 2:
            self.dm.display(
                ('You feel the fatigue of the journey setting in as you sit down by the side of the path, grateful '
                 'for the chance to rest for a few moments. Your stomach grumbles loudly, reminding you that it\'s '
                 'been hours since your last meal. You rummage through your pack and pull out a meager lunch of '
                 'hard bread and cheese. It\'s not much, but it will have to do.',
                 ' ',
                 'As you take a bite of the dry bread, you feel a sense of relief wash over you. The simple act of '
                 'sitting down and eating has reinvigorated your weary body. The midday sun beats down on you, but '
                 'you don\'t mind. The warmth feels good against your skin, and for a brief moment, you allow '
                 'yourself to relax.',
                 ' ',
                 'But you know that you cannot linger for long. The road ahead is still long and treacherous, and '
                 'you must press on if you hope to reach your destination before nightfall. With a deep breath, '
                 'you pack up your meager lunch and rise to your feet, feeling a renewed sense of determination. '
                 'You may be tired, but you will not let that stop you. You set off once again.'))
            self.player.eat(2)
            self.go_to_page(4)

        elif page_number == 3:
            self.dm.display(
                ('As you continue walking along the path, you take a moment to catch your breath and grab a couple '
                 'of provisions from your bag. The food gives you some much-needed energy, and you feel your '
                 'spirits lift slightly as you munch on the dried fruit and jerky.',
                 ' ',
                 'But your moment of respite is short-lived as your foot catches on a root, and you trip and '
                 'stumble forward. You feel the air knocked out of your lungs as you fall to the ground, and one '
                 'of your rations tumbles out of your hand and onto the ground.'))

            if random.randint(1, 2) == 1:
                self.go_to_page(100)

            self.dm.display((' ',
                             'You scramble to pick it up, but as you do, you realize that the ground is teeming with '
                             'ants. You watch in horror as they swarm over the food, devouring it in seconds.',
                             ' ',
                             'You curse your misfortune, but you know that there is nothing you can do about it now. '
                             'You leave the ant swarm behind and continue on your way, feeling a pang of hunger in '
                             'your stomach and a sense of unease in your mind.'))
            self.go_to_page(4)

        elif page_number == 4:
            choice = self.dm.display(
                'You continue trekking through the tranquil natural landscape for the remainder of the '
                'day until in the distance you see a signpost ahead, and as you draw nearer you see that '
                'the trampled path splits two ways. You walk up to the signpost to inspect what it says, '
                'but to your disdain it is weathered and difficult to read. The paths both go fairly '
                'forwards, but one you can see goes of to the left after a hill, and the other one seems '
                'to stay fairly consistent with the direction you have been going. The leftward arrow of '
                'the sign post, is hard to make out, but you do your best: `░kı▓▒▒r░yon░`, and the '
                'forwards pointing sign is in no better condition `░▒ıƒȝа▓░v▒ȝ░`.',
                options=(('F', 'L'), ('Continue forwards, in the direction you thought was correct; '
                                      'following the sign that says `░▒ıƒȝа▓░v▒ȝ░`.',
                                      'Trek along the leftwards path; saying `░kı▓▒▒r░yon░` to see what '
                                      'fate awaits you there.')))

            if choice == 'F':
                self.go_to_page(5)

            elif choice == 'L':
                self.go_to_page(6)

        elif page_number == 5:
            self.dm.display(
                ('You decide to continue forwards, in the direction that you thought was correct, following the '
                 'sign that says ░▒ıƒȝа▓░v▒ȝ░. The path takes you through plains with tall grass swaying in the '
                 'wind. You take in the tranquility of the natural landscape around you, enjoying the peace and '
                 'quiet.',
                 ' ',
                 'Suddenly, you hear a loud screeching sound coming from above. You look up to see a giant vulture '
                 'circling overhead, its eyes fixed on you. You quickly realize that you\'re in danger and draw '
                 'your weapon.',
                 ' ',
                 'The vulture swoops down towards you... quickly test your luck!'))

            action = self.get_player_action(self.PLAYER_COMMANDS['%'])
            lucky = self.player.test_luck()

            if lucky:
                self.dm.display(
                    'you swing your weapon at it. The vulture tries to dodge your attack, but you manage to land a '
                    'hit, causing it to screech in pain. The vulture circles back around for another attack, and '
                    'you brace yourself for the impact.')

            else:
                self.dm.display(
                    'you swing your weapon at it. But the vulture smacks your sword out of your hands and slashes '
                    'at your chest with it\'s claws. The vulture then flies back up and circles back around for '
                    'another attack, and you brace yourself for the impact.')
                self.player.change_statistics(stamina_change=-4)

            self.dm.display('Now you\'ll need to fight the giant vulture')

            if lucky:
                self.fight([Enemy(self.dm, 'Giant Vulture', 6, 2, 0)])

            else:
                self.fight([Enemy(self.dm, 'Giant Vulture', 8, 2, 0)])

            self.dm.display(
                ('As the vulture swoops down towards you, you swing your weapon at it. You manage to land a hit, '
                 'causing the vulture to screech in pain. It circles back around for another attack, but you\'re '
                 'ready for it this time. With a swift movement, you swing your weapon once more and strike the '
                 'vulture\'s head, delivering a deadly blow.',
                 ' ',
                 'The vulture drops to the ground, lifeless. You breathe a sigh of relief and turn to walk away, '
                 'but as you step over the bird\'s wing, you trip and stumble. You look back and see that the '
                 'vulture\'s wing is caught on a rock, and as you try to free yourself, you notice a small glint '
                 'of metal hidden beneath the feathers.',
                 ' ',
                 'You pull back the feathers and see that the metal is a small key. You have no idea what it '
                 'unlocks, but you tuck it away in your pocket, knowing that it may come in handy later.',
                 ' ',
                 'With the danger past and the key in hand, you continue on your journey, ready for whatever '
                 'challenges lie ahead. You see a forest up ahead, and, now cautious, of the monsters of the sky '
                 'you decide that you should trek to the forest and then continue you journey from within.'),
                ascii_image=self.IMAGES['key'])

            self.player.change_inventory(['vulture\'s key'])

            self.go_to_page(20)

        elif page_number == 6:
            choice = self.dm.display(
                ('As you take the leftward path, you trek uphill and after some time you start to notice '
                 'a faint outline of a small hut nestled among the hills. The path leading to it is '
                 'overgrown with weeds, suggesting that it has not been visited in quite some time. As '
                 'you approach the hut, you notice that it seems abandoned with no sign of life, and the '
                 'wooden door is ajar, creaking in the breeze.',
                 ' ',
                 'As you stand before the hut, you take a moment to study it. The roof is made of '
                 'thatched straw, which is now discolored and frayed. The wooden planks that make up the '
                 'walls are weathered and appear to be on the verge of falling apart. The windows are '
                 'made of thin panes of glass, some of which are broken and others covered with dirt and '
                 'grime.',
                 ' ',
                 'You can\'t help but feel drawn to the hut, wondering what secrets it might hold. But at '
                 'the same time, you feel a sense of caution and hesitation, unsure if entering the hut '
                 'is a good idea.'),
                options=(('C', 'H'), ('Continue walking along the path, leaving the abandoned hut behind.',
                                      'Go an explore the overgrown hut.')))

            if choice == 'C':
                self.go_to_page(9)

            elif choice == 'H':
                self.go_to_page(7)

        elif page_number == 7:
            choice = self.dm.display(
                'You enter the hut and look around. There are old, musty books scattered on a small '
                'wooden table and a rickety bed in the corner. In the other corner, you notice a chest '
                'with a rusty lock. As you investigate the chest, you find a rusty key lying beside it. '
                'You can try to open the chest with the key or leave the hut and continue your journey.',
                options=(('K', 'L'), ('Pickup the key and try to open the chest with it.',
                                      'Leave the hut and continue on your journey without exploring '
                                      'further.')))

            if choice == 'K':
                self.go_to_page(8)

            elif choice == 'L':
                self.go_to_page(9)

        elif page_number == 8:
            self.dm.display(
                ('You decide to use the rusty key to try and open the chest. You insert the key and turn it with '
                 'some difficulty, but the lock clicks open. As you lift the lid, you are met with a gruesome '
                 'sight. Inside the chest lies the body of a man, shoved in and haphazardly covered with old '
                 'clothes. You recoil in shock and horror, trying to catch your breath. The stench of death is '
                 'overwhelming, and you quickly realize that the body has been here for a long time.',
                 ' ',
                 'You search the chest further and find a note hidden inside. The note reads:',
                 '"Here lies the body of a thief who thought he could outsmart me. He tried to steal my treasures, '
                 'but I caught him and put him in here. May his rotting corpse serve as a warning to others who '
                 'dare to cross my path."',
                 ' ',
                 'You shudder at the sinister message and quickly leave the hut, feeling relieved to be out of the '
                 'oppressive atmosphere. You continue your journey, wondering who could have left the note and the '
                 'dead body in the abandoned hut.',
                 ' ',
                 'As you walk, you can\'t shake off the feeling that you are being watched. The hairs on the back '
                 'of your neck stand on end, and you feel an uneasy sense of danger. You wonder if there is more '
                 'to the story of the dead body in the chest, and if you should have left it alone.'),
                ascii_image=self.IMAGES['skull'])
            self.player.change_statistics(luck_change=-1)
            self.player.change_inventory('rusty key')
            self.go_to_page(9)

        elif page_number == 9:
            choice = self.dm.display(
                ('After walking for half an hour or so, the path splits in two. The first path leads up a '
                 'mountain, winding through the peaks that stretch out ahead of you. The air feels cooler '
                 'here, and the clouds seem to hover low, shrouding the mountaintops in a misty veil. You '
                 'can\'t see far up the path, but you can make out the outline of some large rocks and '
                 'boulders that dot the landscape.',
                 ' ',
                 'The second path leads into a thick forest, which curves to the right as far as you can '
                 'see. The trees look tall and imposing, their leaves turning shades of red and gold in '
                 'the autumn sunlight. The forest seems dark and mysterious. You can hear the rustling of '
                 'leaves and the chirping of birds coming from within; it seems to be crawling with life.',
                 ' ',
                 'Which path shall you trek through?'),
                options=(('M', 'F'), ('Keep going straight, up through the mountains.',
                                      'Turn right, into the forest path, which may provide more '
                                      'protection from the elements.')))

            if choice == 'M':
                self.go_to_page(10)

            elif choice == 'F':
                self.go_to_page(20)

        elif page_number == 10:
            choice = self.dm.display(
                ('As you keep walking, the landscape gradually transforms, and the hills become more '
                 'mountainous. The air becomes cooler, and you can feel a breeze blowing through the '
                 'trees. You walk for what seems like hours until you come across a bricked path that '
                 'leads up to a temple atop one of the hills.',
                 ' ',
                 'The temple is made of white marble, and its walls and pillars are intricately carved '
                 'with mythical creatures and symbols. You stand in awe, marveling at the impressive '
                 'architecture of the temple. You can see a set of stairs leading up to the entrance, and '
                 'you can also see a path leading through the mountain.',
                 ' ',
                 'But then, suddenly, your foot catches a rock on the path and you trip.'))
            self.go_to_page(100)

        elif page_number == 20:
            self.dm.display(
                    ('As you make your way towards the forest path, the rustling of leaves grows louder, and the '
                     'chirping of birds becomes more distinct. You feel a sense of excitement as you approach the '
                     'entrance to the forest. The trees look tall and imposing, their leaves turning shades of red and '
                     'gold in the autumn sunlight. ',
                     ' ',
                     'You take a few steps forward, admiring the beauty of the scenery around you. But just as you '
                     'reach the entrance to the forest, you suddenly hear a loud snap, followed by a sharp pain in '
                     'your leg. You look down to see that you\'ve fallen into a spike trap hidden under a net with '
                     'leaves on top, and you\'ve been pierced. ',
                     ' ',
                     'Panic sets in as you realize the severity of your injury. You struggle to free yourself from the '
                     'trap, but it\'s too late. You collapse onto the ground, your vision growing hazy. You look up at '
                     'the beautiful autumn scene around you, feeling a sense of regret for not choosing the safer '
                     'path. ',
                     ' ',
                     'As your consciousness begins to fade, you realize that sometimes the most beautiful paths can '
                     'lead to the darkest outcomes. You hear a group of high-pitched raspy voices approach you, then a '
                     'bludgeoning force pounds into your head and everything goes black.'))
            self.player.die(' at the hands of a devious trap. ')

        elif page_number == 100:
            choice = self.dm.display((' ',
                                      'Then you fall forwards, into the path, and through it, through the world.',
                                      ' ',
                                      'You find yourself walking down a dimly lit hallway, the walls painted a sickly '
                                      'shade of yellow that seems to seep into your skin. The fluorescent lights above '
                                      'flicker sporadically, casting strange shadows on the endless expanse of '
                                      'identical doors and hallways that stretch out before you.',
                                      ' ',
                                      'As you make your way down the hallway, you begin to feel a growing sense of '
                                      'unease. There\'s something deeply wrong about this place, something that makes '
                                      'your skin crawl and your heart race.',
                                      ' ',
                                      'Suddenly, you hear a sound behind you - a faint shuffling noise, like someone '
                                      'or something is following you. Deep down fear tingles through your body, and '
                                      'you feel almost paralyzed by it, you have only two choices of action.'),
                                     options=(('I', 'T'), ('Ignore the noise and keep walking straight ahead.',
                                                           'Turn around and confront whatever is following you.')))

            if choice == 'I':
                self.go_to_page(102)

            elif choice == 'T':
                self.go_to_page(101)

        elif page_number == 101:
            choice = self.dm.display(
                'You turn around, your heart pounding in your chest. As you face the direction of the '
                'sound, you see a dark figure shambling towards you, its body hunched over and its limbs '
                'contorted at unnatural angles. You can\'t make out any features on its face, but you '
                'feel a deep sense of dread as it draws closer.',
                options=(('R', 'F'), ('Run in the opposite direction of the creature.',
                                      'Try to fight off the creature with whatever you have in your '
                                      'inventory')))

            if choice == 'R':
                self.go_to_page(103)

            elif choice == 'F':
                self.go_to_page(104)

        elif page_number == 102:
            choice = self.dm.display(
                ('You continue down the hallway, trying to ignore the feeling of eyes watching you from '
                 'the shadows. The hallway seems to stretch on forever, and you begin to wonder if '
                 'you\'ll ever find your way out.',
                 ' ',
                 'Eventually, you come to a door that looks different from the others. It\'s old and '
                 'weathered, with peeling paint and rusted hinges. As you approach it, you hear a faint '
                 'humming sound coming from the other side.'),
                options=(('D', 'W'), ('Open the door and investigate the sound.',
                                      'Keep walking and ignore the door.')))

            if choice == 'D':
                self.go_to_page(105)

            elif choice == 'W':
                self.go_to_page(106)

        elif page_number == 103:
            choice = self.dm.display(('You turn and run as fast as you can in the opposite direction, hoping to escape '
                                      'whatever is chasing you. But as you run, you realize that the hallway seems to '
                                      'be stretching out ahead of you, growing longer and longer with every step you '
                                      'take.',
                                      ' ',
                                      'Before long, you\'re gasping for air and your legs feel like they\'re about to '
                                      'give out. You stop and turn around, but the creature is still following you, '
                                      'its grotesque form looming closer and closer.'),
                                     options=(('R', 'H'), ('Keep on running.', 'Try to find a place to hide.')))

            if choice == 'R':
                self.go_to_page(107)

            elif choice == 'H':
                self.go_to_page(108)

        elif page_number == 104:
            self.dm.display(
                ('You try to fight off the creature with whatever objects you have on hand, but it seems immune to '
                 'your attacks. No matter how many times you hit it or throw things at it, it just keeps coming, '
                 'its twisted form advancing on you relentlessly.',
                 ' ',
                 'As the creature reaches out to grab you, you feel a sudden jolt of pain and disorientation. The '
                 'next thing you know, you\'re falling through the floor, tumbling down into the depths of the '
                 'maze like dimension.'))
            self.go_to_page(109)

        elif page_number == 105:
            choice = self.dm.display(
                ('You push open the old, weathered door and step inside. The humming sound grows louder '
                 'as you move deeper into the room, and you begin to see strange, flickering lights '
                 'dancing across the walls.',
                 ' ',
                 'As you turn a corner, you come face to face with a figure unlike anything you\'ve ever '
                 'seen before. It\'s humanoid in shape, but its skin is a sickly shade of green and its '
                 'eyes glow an eerie yellow. It speaks to you in a language you don\'t understand, but '
                 'you can sense that it\'s trying to communicate something important.'),
                options=(('C', 'L'), ('Try to communicate with the creature.',
                                      'Try to leave the room and walk down the hallway.')))

            if choice == 'C':
                self.go_to_page(110)

            elif choice == 'L':
                self.go_to_page(111)

        elif page_number == 106:
            choice = self.dm.display(
                ('You ignore the old, weathered door and keep walking down the hallway. But as you '
                 'continue on, the humming sound grows louder and louder, until it feels like it\'s '
                 'echoing inside your head.',
                 ' ',
                 'You begin to feel dizzy and disoriented, and before long, you\'re lost in a maze of '
                 'identical corridors that all look the same. You start to panic, wondering if you\'ll '
                 'ever find your way out.'),
                options=(('W', 'R'), ('Keep wandering aimlessly.',
                                      'Try to retrace your steps and find your way back to where you '
                                      'started')))

            if choice == 'W':
                self.go_to_page(112)

            elif choice == 'R':
                self.go_to_page(113)

        elif page_number == 107:
            choice = self.dm.display(
                ('You keep running, even as your legs burn and your lungs ache. But no matter how fast '
                 'you go, the hallway just seems to keep stretching out ahead of you, endless and '
                 'unchanging.',
                 ' ',
                 'As you run, you begin to see strange, flickering lights in the distance. They seem to '
                 'be coming from some kind of room or chamber up ahead.'),
                options=(('L', 'H'), ('Keep running towards the lights.',
                                      'Try to find a place to hide.')))

            if choice == 'L':
                self.go_to_page(114)

            elif choice == 'H':
                self.go_to_page(115)

        elif page_number == 108:
            self.dm.display(
                ('You try to find a place to hide, but the hallway seems to offer no shelter or cover. The walls '
                 'are smooth and unbroken, and there\'s nowhere to hide from the creature that\'s pursuing you.',
                 ' ',
                 f'As the creature draws closer, you feel a sudden jolt of pain and disorientation. The next thing '
                 f'you know, you\'re falling through the floor, tumbling down into the depths of a place beyond '
                 f'reality, a place clearly of nightmares.'))
            self.go_to_page(109)

        elif page_number == 109:
            choice = self.dm.display(('You land in a strange, dimly lit room that seems to stretch on forever in all '
                                      'directions. The walls are made of some kind of stained, yellowed material, and '
                                      'the floor is covered in a thick layer of grime and dust.',
                                      ' ',
                                      f'You realize with a sinking feeling that you\'ve fallen into the '
                                      f'{self.RAND_LOCATIONS["backrooms"]}, a twisted, maze-like world of endless '
                                      f'hallways and rooms that exist somewhere between reality and unreality, you\'ve '
                                      f'heard of this place through legends and rumours alone. You know you must take '
                                      f'action, so what will you try to do? Dark evils lurk here and that it may not '
                                      f'be long until you are found by them.'),
                                     options=(
                                     ('L', 'E'),
                                     (f'Search around for a way to escape the {self.RAND_LOCATIONS["backrooms"]}.',
                                      f'Spend some time looking around the {self.RAND_LOCATIONS["backrooms"]}.')))

            if choice == 'L':
                self.go_to_page(116)

            elif choice == 'E':
                self.go_to_page(117)

        elif page_number == 110:
            self.dm.display(
                ('You try to communicate with the strange, green-skinned creature, but you can\'t seem to make '
                 'yourself understood. It continues to speak in its own language, its yellow eyes fixed on you.',
                 ' ',
                 'As you try to decipher its meaning, you suddenly feel a jolt of pain and disorientation. You '
                 'pass out.'))
            self.player.change_statistics(stamina_change=-1)

            self.dm.pause(5, 30)

            self.player.die('at the dim wits of an alien creature.')

        elif page_number == 111:
            choice = self.dm.display(
                ('You retrace your steps and find your way back to where you started, but the maze of '
                 'identical corridors seems to shift and change around you. It\'s like the world itself '
                 'playing tricks on you, leading you down dead ends and false paths.',
                 ' ',
                 'As you wander, you begin to hear strange, whispering voices in the darkness. They seem '
                 'to be calling out to you, but you can\'t make out what they\'re saying.'),
                options=(('V', 'O'), ('Follow the voice, to see where it takes you.',
                                      'Try to block out the voices and focus on finding a way out.')))

            if choice == 'V':
                self.go_to_page(118)

            elif choice == 'O':
                self.go_to_page(119)

        elif page_number == 112:
            choice = self.dm.display(
                ('You keep wandering aimlessly, hopelessly lost in the maze of corridors. You begin to '
                 'feel like you\'re going in circles, passing the same doors and rooms over and over '
                 'again.',
                 ' ',
                 'Just when you\'re about to give up hope, you see a flickering light in the distance. It '
                 'seems to be coming from some kind of room or chamber up ahead.'),
                options=(('W', 'I'), ('Keep wandering down the hallway.',
                                      'Investigate the room with the flickering light.')))

            if choice == 'W':
                self.go_to_page(120)

            elif choice == 'I':
                self.go_to_page(121)

        elif page_number == 113:
            self.dm.display(
                ('You try to retrace your steps and find your way back to where you started. It takes some time '
                 'for you to realise, but it seems that this maze of corridors and rooms changes when your not '
                 'looking. With this realization you decide in horror that there must be no way to escape this '
                 'maze-like prison that you find yourself entrapped in.',
                 ' ',
                 'Full of despair you go to lean against the nearest, yellow-wallpapered, wall. As you lean over, '
                 'however you somehow miss the wall, and fall right through it. You scream as you fall into the '
                 'wall and then become consumed by an endless void of darkness, there is nothing you can do, as '
                 'you fall forever in the lifeless void.'))

            self.player.die('as you starve to death in an endlessly deep void of darkness')

        elif page_number == 114:
            choice = self.dm.display(
                ('You run towards the strange, flickering lights, your heart pounding in your chest. As '
                 'you get closer, you realize that the lights are coming from some kind of chamber or '
                 'room up ahead.',
                 ' ',
                 'As you step inside the room, you see a strange, glowing artifact in the center. It '
                 'looks like some kind of ancient, alien technology, pulsing with an otherworldly '
                 'energy.'),
                options=(('A', 'J'), ('Try to interact with the artifact.',
                                      'Leave the room and continue on your journey.')))

            if choice == 'A':
                self.go_to_page(122)

            elif choice == 'J':
                self.go_to_page(123)

        elif page_number == 115:
            choice = self.dm.display(
                ('You try to find a place to hide, but the hallway seems to offer no shelter or cover. '
                 'The yellow walls are unbroken and flat, and there\'s nowhere to hide from the creature '
                 'that\'s pursuing you.',
                 ' ',
                 'As the creature draws closer it\'s grotesque form morphs and changes into an '
                 'unfathomable, black, angular, beast. It opens it\'s mouth, and is coming in for the '
                 'kill.'),
                options=(('F', 'S'), ('Try and fight the abomination.',
                                      'Huddle up and wait for your impending doom')))

            if choice == 'F':
                self.fight([Enemy(self.dm, 'Black Abomination', 115, 15, 0)])

                self.dm.display(
                    'You are the luckiest player of all time. You won!, I\'m not sure how you did that... cheater')

            elif choice == 'S':
                self.dm.display(
                    ('You feel a surge of fear and desperation as the creature closes in on you. With nowhere to '
                     'run or hide, you decide to huddle up and wait for your impending doom. You close your eyes '
                     'tightly and try to steady your breathing as you hear the creature\'s footsteps grow louder '
                     'and louder.',
                     ' ',
                     'Suddenly, you feel a searing pain as the creature sinks its sharp teeth into your flesh. You '
                     'scream in agony as you feel its powerful jaws crushing your bones and tearing your flesh '
                     'apart. You try to fight back, but your feeble attempts are no match for the creature\'s '
                     'immense strength.'))

                self.player.die(message_preset=6)

        elif page_number == 116:
            self.dm.display(
                ('You try to find a way out of the labyrinth, but the maze of corridors seems to stretch on '
                 'forever. Every door and hallway leads to another dead end or false path, and you begin to feel '
                 'like you\'re going in circles.',
                 ' ',
                 'Just when you\'re about to give up hope, you see a faint glimmer of lights in the distance. You '
                 'can\'t tell what it\'s coming from, but it reinvigorates you with hope.'))
            self.go_to_page(114)

        elif page_number == 117:
            choice = self.dm.display(
                ('You decide to explore this place, and see what you can find. As you wander through '
                 'the endless maze of corridors and rooms, you come across all sorts of strange and '
                 'eerie sights.',
                 ' ',
                 'You see strange, glowing symbols etched into the walls, flickering lights that seem to '
                 'move of their own accord, and rooms filled with bizarre and otherworldly artifacts.',
                 ' ',
                 'But as you explore deeper and deeper in the labyrinth, you begin to feel a growing '
                 'sense of unease. You realize that this place is not meant for human minds to '
                 'comprehend, and that the longer you stay here, the more your sanity will be at risk.',
                 ' ',
                 'As you come to this realization, a sudden rustling noise startles you, and you quickly '
                 'turn to see a black, humanoid, sinewy creature stalking towards you. Its eyes glow with '
                 'an unnatural intensity, and you can feel a sense of malevolence emanating from it.'),
                options=(('F', 'H'), ('Fight the stalker.', 'Run to find a place to hide.')))

            if choice == 'F':
                self.dm.display('You take a deep breath and ready yourself for the attack.')
                self.fight([Enemy(self.dm, 'Black Abomination', 99, 19, 0)])

                self.dm.display(
                    'You are the luckiest player of all time. You won!, I\'m not sure how you did that... cheater')

            elif choice == 'H':
                self.dm.display(('you choose to hide, you frantically look around for a suitable spot, hoping that the '
                                 'creature doesn\'t notice you. You spot a nearby room with a partially closed door '
                                 'and dive inside, quietly shutting the door behind you.',
                                 ' ',
                                 'You can hear the creature sniffing and snarling outside, but it seems to be moving '
                                 'away. You wait for what feels like an eternity before you muster the courage to peek '
                                 'outside. The creature is nowhere to be seen, and you quickly make your way out of '
                                 'the room, but just as you do a searing pain develops in through your back and belly.',
                                 ' ',
                                 'You look down, and to your horror and black appendices, of sinew, bones, and veins '
                                 'has gorged itself through your abdomen. You hold your hand to the wound, while blood '
                                 'splatters out of it, staining the carpet and your clothes. A violent force from '
                                 'behind swings you violently to the floor. And as you lay, dying, you see that ugly, '
                                 'evil face. It stares back at you with a gruesome smile and you can sense a hint of '
                                 'cruel cleverness in it\'s smile.'))
                self.player.die('at the gruesome will of an dark alien fiend.')

        elif page_number == 118:
            choice = self.dm.display(
                ('You follow the whispering voices, drawn towards them like a moth to a flame. The voices '
                 'lead you through a winding maze of corridors, deeper and deeper into the labyrinth.',
                 ' ',
                 'Finally, you reach a small, dark chamber. In the center of the room is a strange, '
                 'glowing object. It looks like some kind of ancient, alien technology, pulsing with an '
                 'otherworldly energy.'),
                options=(('O', 'J'), ('Try to interact with the object.',
                                      'Leave the chamber and continue your journey.')))

            if choice == 'O':
                self.go_to_page(122)

            elif choice == 'J':
                self.go_to_page(123)

        elif page_number == 119:
            self.dm.display(
                ('You take a deep breath and try to block out the whispering voices, focusing instead on finding a '
                 'way out of this labyrinth. However, as you continue to wander, the voices grow louder and more '
                 'insistent. They seem to be repeating a phrase over and over again, but you can\'t quite make out '
                 'what it is.',
                 ' ',
                 'You try to shake off the feeling of unease that is growing inside of you, but it\'s no use. The '
                 'voices are getting louder and more frequent, until they become almost unbearable.',
                 ' ',
                 'You cover your ears with your hands, hoping to drown out the voices, but it\'s no use. They seem '
                 'to be coming from inside your own head, echoing through your mind.',
                 ' ',
                 'As you stumble through the endless corridors, the voices seem to be leading you somewhere. '
                 'You\'re not sure where, but you feel an almost irresistible urge to follow them.',
                 ' ',
                 'Despite your better judgment, you begin to follow the voices, feeling as though you\'re being '
                 'pulled along by an invisible force.',
                 ' ',
                 'The voices grow louder and more frantic, until they become almost deafening. They repeat the '
                 'same phrase over and over again, until it becomes almost like a chant.',
                 ' ',
                 'Finally, you come to a stop in front of a dark, ominous-looking door. You crouch down, not by '
                 'will, but by some supernatural force. Then the voices start speaking consistently, chanting.'))

            index = 0
            poem = [' ',
                    'In the dark and twisting maze we dwell,',
                    'Where the lost and broken souls do dwell.',
                    'We call out to you, oh wandering one,',
                    'To join our legion and be undone.',
                    ' ',
                    'We\'ll wrap our tendrils \'round your mind,',
                    'Until you\'re lost and left behind.',
                    'Our whispers soft will turn to screams,',
                    'And haunt you in your darkest dreams.',
                    ' ',
                    'You\'ll see our faces in the dark,',
                    'Our twisted visages leave their mark.',
                    'Our grip on you will not relent,',
                    'Until your will is finally spent.',
                    ' ',
                    'So come to us, oh traveler lost,',
                    'And join our army at all cost.',
                    'Our master\'s bidding you must do,',
                    'Or suffer madness ever anew.',
                    ' ',
                    'The only way to find release,',
                    'Is to give in and find your peace.',
                    'Succumb to us and our control,',
                    'And join us in our endless role.',
                    ' ',
                    'We\'ll sing our song into your mind,',
                    'Until you leave this world behind.',
                    'Come to us, and find your rest,',
                    'In our embrace, forever blessed.']

            while True:
                if poem[index] == ' ':
                    self.dm.display(' ')

                else:
                    color = random.choice((Fore.RED, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX,
                                           Fore.LIGHTYELLOW_EX))
                    style = random.choice((Style.RESET_ALL, Style.BRIGHT, Style.DIM, Style.NORMAL))

                    self.dm.display(f'{color}{style}{poem[index]}')

                if index >= len(poem) - 1:
                    index = 0

                else:
                    index += 1

        elif page_number == 120:
            self.dm.display(
                ('You keep wandering down the hallway, hoping to find some kind of exit or escape. But the hallway '
                 'seems to stretch on forever, and every door and corridor leads to another dead end or false '
                 'path.',
                 ' ',
                 'As you keep walking, you begin to feel a growing sense of unease. You realize that you may be '
                 'trapped in the labyrinth forever, doomed to wander its endless corridors for all eternity.',
                 ' ',
                 'Then, you hear a whisper. It was small, but close by. You look around, but see no source to the '
                 'strange noise. Then you hear it again... You look backwards and forth down the hallway, but see '
                 'no one. Then it becomes a little louder, and you realise that the voices are coming fro inside '
                 'of your head.'))
            self.go_to_page(119)

        elif page_number == 121:
            choice = self.dm.display(
                ('You investigate the room with the flickering light, cautiously stepping inside. The '
                 'room is filled with strange, otherworldly artifacts, each one pulsing with an eerie, '
                 'pulsing energy.',
                 ' ',
                 'As you explore the room, you begin to feel a growing sense of unease. You realize that '
                 'these artifacts are not meant for human minds to comprehend, and that the longer you '
                 'stay in the room, the more your sanity will be at risk. But the object seems to promise '
                 'something to you, something good'),
                options=(('A', 'J'), ('Continue to explore the room and study the artifacts.',
                                      'Leave the room and continue on your journey.')))

            if choice == 'A':
                self.go_to_page(122)

            elif choice == 'J':
                self.go_to_page(123)

        elif page_number == 122:
            self.dm.display(
                ('You try to interact with the strange, glowing object in the chamber. As you reach out to touch '
                 'it, you feel a sudden surge of energy coursing through your body. At first, it feels good, '
                 'invigorating, like a shot of adrenaline.',
                 ' ',
                 'But then, the energy starts to feel painful. It\'s like fire coursing through your veins, '
                 'searing your nerves and causing unbearable agony.',
                 ' ',
                 'You try to pull your hand away from the object, but it\'s too late. Your hand is melted onto the '
                 'surface, fused to the object by some strange, otherworldly force.',
                 ' ',
                 'You scream in agony as the energy courses through your body, burning you alive from the inside '
                 'out. Your vision starts to blur, and you feel yourself slipping away into darkness.',
                 ' ',
                 'And then, everything goes black.',
                 ' ',
                 'The next thing you know, you\'re lying on the ground, your body twisted and contorted in '
                 'unnatural angles. Your hand is still fused to the object, but now it\'s cold and black.',
                 ' ',
                 'You realize with horror that you\'ve been trapped in this labyrinth forever, doomed to spend '
                 'eternity as a twisted, tortured creature, forever bound to the strange, glowing object that has '
                 'claimed your life.'))
            self.player.die('. Now twisted into a abborant fiend, forever to crawl through the labyrinth in which you '
                            'where caught.', message_preset=1)

        elif page_number == 123:
            self.dm.display(
                ('You take a deep breath and gather your wits as you leave the room, looking for the next way out '
                 'of this labyrinthine nightmare. You walk through the yellowed hallways and rooms, trying to keep '
                 'track of where you\'ve been and where you haven\'t.',
                 ' ',
                 'But after journeying for what feels like hours, you start to get a sinking feeling in your '
                 'stomach. You feel like you\'ve seen this room before, with its cracked walls and flickering '
                 'lights. And then it hits you: you\'re stuck in an infinite loop.',
                 ' ',
                 'You try retracing your steps, but every door leads to the same place, and every hallway looks '
                 'identical to the last. The more you try to find your way out, the more lost you become. It\'s '
                 'like the labyrinth is playing a cruel game with you, taunting you with the illusion of escape.',
                 ' ',
                 'You start to feel a sense of panic rising within you. How long have you been stuck in this loop? '
                 'How many times have you passed through this same room, only to end up back where you started? '
                 'You try to shake the feeling off and focus on finding a way out, but it\'s no use. You\'re ',
                 'trapped, and there\'s no way out.',
                 ' ',
                 'As you wander aimlessly through the endless maze, your sanity begins to slip away. You start to '
                 'see strange, twisted creatures lurking in the shadows, their eyes glowing with an otherworldly '
                 'light. You hear voices whispering in your ear, taunting you, driving you further into madness.',
                 ' ',
                 'And then, finally, you collapse onto the ground, exhausted and defeated. You realize that '
                 'you\'re not getting out of this place alive. You have been claimed victim by this endless, '
                 'yellowed, nightmare.'))
            self.player.die('exhausted to death, and stuck in a infinitely looping labyrinth.')

        else:
            self.dm.display(f"that's not a section ({page_number}), something's gone terribly wrong.")
            self.get_player_action(())
