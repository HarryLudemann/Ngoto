import logging
import traceback
import sys
from hazzah.modules.utilities.plugin import Plugin

class Interface:
    class bcolors:
        """ Stores colours """
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def output(self, output):
        """ Print Method """
        bcolors = self.bcolors()
        print(f"{bcolors.BOLD} > ", output, f"{bcolors.ENDC}")

    def get_input(self, text='', position='', current_position=''):
        """ Input Method """
        bcolors = self.bcolors()
        user_input = str( input(f"{bcolors.OKCYAN}{bcolors.BOLD}" + current_position + position + f'{bcolors.ENDC}{bcolors.BOLD} > ' + str(text)) )
        if user_input in ['exit']:  
            sys.exit()
        return user_input

    # UI Methods
    def logo(self):
        bcolors = self.bcolors()
        print(f'''{bcolors.BOLD}{bcolors.HEADER}
     _   _                    _     
    | | | |                  | |    
    | |_| | __ _ __________ _| |__  
    |  _  |/ _` |_  /_  / _` | '_ \ 
    | | | | (_| |/ / / / (_| | | | |
    \_| |_/\__,_/___/___\__,_|_| |_|      
        {bcolors.ENDC}''')

    def options(self, hz):
        self.logo()
        bcolors = self.bcolors()
        options = f'{bcolors.BOLD}\n0. Exit'
        for index, plugin in enumerate(hz.plugins):
            options += f'\n{index+1}. {plugin.name}'
        print(options + f'\n\nWorkplace: {hz.current_workplace}\n{bcolors.ENDC}')

    def commands(self):
        self.logo()
        print(f'''
    {self.bcolors.HEADER}[Basic]{self.bcolors.ENDC}{self.bcolors.BOLD}
    o/options                   --  Returns osint options
    c/commands                  --  Returns this list of commands
    cls/clear                   --  Clear console
    0/exit                      --  closes program

    {self.bcolors.HEADER}[Workplace]{self.bcolors.ENDC}{self.bcolors.BOLD}
    wp/workshop create (NAME)   --  Creates (NAME) workplace
    wp/workshop join (NAME)     --  Joins (NAME) workplace
    wp/workshop delete (NAME)   --  Deletes (NAME) workplace
    wp/workshop leave           --  Leave current workplace
        {self.bcolors.ENDC}''')