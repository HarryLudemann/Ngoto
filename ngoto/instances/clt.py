
# Script contains functions to handle the clt input output paired with utils instance class

__author__ = 'Harry Ludemann'
__version__ = '0.0.21'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

from ngoto.util import interface, Node, Logging
from ngoto.util.ngotoBase import NgotoBase  
from ngoto.commands import *
from ngoto import constants as const

class CLT(NgotoBase):
    """ Command line tool class, containing CLT specifc methods """
    commands = []

    def __init__(self):
        """ Instansiate and loads commands, plugins and logger """
        self.commands = [
            Commands(),
            Clear(),
            Options(),
            Back(),
            Plugins(),
            OpenPlugin(),
            OpenFolder(),
            Logs(),
            Exit(),
            Paths(),
            Restart(),
            WP(),
        ]
        self.curr_pos = self.load_plugins(Node('root'), const.plugin_path) # load plugins
        self.logger = Logging()


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
        self.run_command('options') # clear screen
        self.main()
        