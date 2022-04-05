# contains function to go back
from ngoto.util.command import Command 
from ngoto.util import interface
import os

class Back(Command):

    def getDescription(self):
        return "Command to go back"

    def getActions(self):
        return ['b', 'back']

    def performAction(self, *args):
        if args[0].has_parent:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
            interface.options(args[0].get_parent())
            args[2].debug(f'Going back to {args[0].get_parent().get_name()}', program='Back')
            return args[0].get_parent()
        else:
            interface.output("You are already in root")
            args[2].debug('Cannot go back, in root dir', program='Back')