
# Script contains functions to handle the clt input output paired with utils instance class

__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

from ngoto.util import interface, Table
from ngoto.instances.ngotoBase import NgotoBase 
from ngoto.commands import *

class CLT(NgotoBase):
    """ Command line tool class, containing CLT specifc methods """
    commands = []

    def __init__(self):
        self.commands = [
            Commands(),
            Clear(),
            Options(),
            Plugins(),
            WP(),
            OpenPlugin(),
            Exit(),
            Back(),
            Paths(),
            OpenFolder()
        ]

    def run_command(self, command: str, options: list = []) -> bool:
        for cmd in self.commands:
            if command in cmd.getActions():
                if (pos := cmd.performAction(self.curr_pos, options)) != None:
                    self.curr_pos = pos
                return True
        return False

    def main(self) -> None:  
        """ Main loop of CLT """  
        # get input
        option = interface.get_input().split()
        # return if no input
        if not option: 
            pass
        # if choosing onscreen option add command prefix
        if (isDigit := option[0].isdigit()) and (num := int(option[0])-1) < self.curr_pos.num_children: # move into folder
            option = ['openF', option[0]]
        elif isDigit and  num < self.curr_pos.num_children + self.curr_pos.num_plugins: # open plugin
            option = ['openP', option[0]]
        # run command, if not command run: print unknown command
        if not self.run_command(option[0], option): # check in commands
            interface.output("Unknown command")

        self.main()