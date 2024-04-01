import ctypes
import subprocess

from bin import worlds
from bin import interface

RUNNING_EXE = False

if RUNNING_EXE:
    subprocess.run(['CMD Color\\ColorTool.exe', '-b', '-q', 'OneHalfDarkish.itermcolors'], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11
    FOREGROUND_RED = 0x04 | 0x08
    FOREGROUND_GREEN = 0x02 | 0x08
    FOREGROUND_BLUE = 0x01 | 0x08


    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]


    def set_cmd_font(font_name="Lucida Console", font_size=18):
        font_info = CONSOLE_FONT_INFOEX()
        font_info.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font_info.dwFontSize.X = font_size
        font_info.dwFontSize.Y = font_size
        font_info.FontFamily = 0
        font_info.FontWeight = 100
        font_info.FaceName = font_name
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font_info))


    set_cmd_font()


class Program:
    def __init__(self):
        self.GAME_NAME = 'Pathways of Fate'
        self.dm = interface.DisplayMachine()
        self.dm.clear_screen()
        self.world = None

    def world_menu(self):
        self.dm.clear_screen()
        world_names = [world_class[0] for world_class in worlds.world_classes]
        self.dm.display(title=f'=== {self.GAME_NAME.upper()}: WORLD SELECT ===')
        world_i = int(self.dm.display(f'Choose which world you would like to play, from the following selection:',
                                      options=([str(i + 1) for i in range(len(world_names))], world_names))) - 1
        self.world = worlds.world_classes[world_i][1](self.dm, self.GAME_NAME)
        self.dm.world = self.world

    def main_menu(self):
        self.dm.clear_screen()
        self.dm.display(title=f'=== {self.GAME_NAME.upper()} ===')

    def settings_menu(self):
        self.dm.clear_screen()
        self.dm.display(title=f'=== {self.GAME_NAME.upper()}: SETTINGS ===')

    def run(self):
        self.world_menu()
        self.dm.clear_screen()
        self.dm.display(title=f'=== {self.GAME_NAME.upper()}: {self.world.WORLD_NAME.upper()} ===',
                        ascii_image=self.world.IMAGES['introduction'])

        action = self.dm.display(input_string=self.world.introduction(),
                                 options=(('S', 'E'),
                                          ('Step forwards, and present yourself as the one who shall take on this '
                                           'mighty quest.', 'Or, end the journey before it even begins.'))).upper()

        if action == 'S':
            self.world.run()

        elif action == 'E':
            self.dm.display('The story ends here, before it even truly began... you will not be the hero of this '
                            'story, and it\'s future is left uncertain.')
            self.dm.exit_program()
