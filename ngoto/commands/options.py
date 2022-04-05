# contains function to show options 
from ngoto.util.command import Command 
from ngoto.util import interface
import os

class Options(Command):
    def getDescription(self):
        return "Command to show options"

    def getActions(self):
        return ['o', 'options']

    def performAction(self, *args):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        interface.options(args[0])
        args[2].debug(f'Showing options', program='Options')
        return args[0]
