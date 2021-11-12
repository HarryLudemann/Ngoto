# script contains interface functions

import sys

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
     _   _             _        
    | \ | |           | |       
    |  \| | __ _  ___ | |_ ___  
    | . ` |/ _` |/ _ \| __/ _ \ 
    | |\  | (_| | (_) | || (_) |
    |_| \_|\__, |\___/ \__\___/ 
            __/ |               
           |___/                   
        {bcolors.ENDC}''')

    def options(self, curr_node, curr_workplace:str = 'N/A'): # given Node in plugin and optionally workplace string
        self.logo()
        bcolors = self.bcolors()
        index = 1
        options = f'{bcolors.BOLD}\n0. Exit'
        for folder in curr_node.get_children(): # print folders
            options += f'\n{index}. {folder.name}'
            index += 1
        for plugin in curr_node.get_plugins(): # print plugins
            options += f'\n{index}. {plugin.name}'
            index += 1
        print(options + f'\n\nWorkplace: {curr_workplace}\n{bcolors.ENDC}')

    def commands(self):
        self.logo()
        print(f'''
    {self.bcolors.HEADER}[Basic]{self.bcolors.ENDC}{self.bcolors.BOLD}
    o/options                   --  Returns osint options
    c/commands                  --  Returns this list of commands
    cls/clear                   --  Clear console
    b/back                      --  Back out of plugin for folder
    0/exit                      --  closes program

    {self.bcolors.HEADER}[Workplace]{self.bcolors.ENDC}{self.bcolors.BOLD}
    wp/workshop create (NAME)   --  Creates (NAME) workplace
    wp/workshop join (NAME)     --  Joins (NAME) workplace
    wp/workshop delete (NAME)   --  Deletes (NAME) workplace
    wp/workshop leave           --  Leave current workplace
        {self.bcolors.ENDC}''')