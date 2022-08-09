# contains function to show options 
from ngoto.util.command import Command 
from ngoto.util import interface
import os

class Options(Command):
    def get_description(self):
        return "Show plugins/options"

    def get_actions(self):
        return ['o', 'options', 'ls']

    def perform_action(self, *args):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        interface.options(args[0])
        args[2].debug(f'Showing options', program='Options')
        return args[0]
