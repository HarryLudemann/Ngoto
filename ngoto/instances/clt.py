
# Script contains functions to handle the clt input output paired with utils instance class

__author__ = 'Harry Ludemann'
__version__ = '0.0.21'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

import importlib
from ngoto.util import interface
from ngoto.instances.ngoto import NgotoBase  
from ngoto import constants as const
from ngoto.commands import *
import os

class CLT(NgotoBase):
    """ Command line tool class, containing CLT specifc methods """
    commands = []

    def __init__(self):
        super().__init__()
        self.commands = self.load_commands()

    def load_commands(self) -> list:
        """ Returns list of instantiated command objects in folder """
        commands = []
        # get command file paths
        command_paths = [c for c in os.listdir(const.command_path) if c.endswith('.py') and not c.startswith('__')]
        for command_path in command_paths:
            module = const.command_path.replace('/', '.') + '.' + command_path[:-3]
            mod = importlib.import_module(module)
            # get module name from path and capitalize first letter to get class name
            module_name = module.split(".")[2] 
            class_ = getattr(mod, module_name[0].upper() + module_name[1:])
            commands.append(class_())
        return commands

    def run_command(self, command: str, options: list = []) -> bool:
        for cmd in self.commands:
            if command in cmd.getActions():
                if (pos := cmd.performAction(self.curr_pos, options, self.logger)) != None:
                    self.curr_pos = pos
                return True
        return False

    def main(self) -> None:  
        """ Main loop of CLT """  
        option = interface.get_input('\n[Ngoto] > ').split()
        if not option:
            pass
        elif (isDigit := option[0].isdigit()) and (num := int(option[0])-1) < self.curr_pos.num_children: # move into folder
            option = ['openF', option[0]]
        elif isDigit and  num < self.curr_pos.num_children + self.curr_pos.num_plugins: # open plugin
            option = ['openP', option[0]]
        if option != [] and not self.run_command(option[0], option): # check in commands
            interface.output("Unknown command")
        self.main()

    def start(self) -> None:
        """ Start CLT """
        self.run_command('clear') # clear screen
        self.run_command('options') # options screen
        self.main()
        