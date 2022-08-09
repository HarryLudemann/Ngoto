# contains function to go back
from ngoto.core.util.command import Command 
from ngoto.core.util.interface import options, output
import os

class Back(Command):

    def get_description(self):
        return "Back out of folder"

    def get_actions(self):
        return ['b', 'back']

    def perform_action(self, *args):
        if args[0].has_parent:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
            options(args[0].get_parent())
            args[2].debug(f'Going back to {args[0].get_parent().get_name()}', program='Back')
            return args[0].get_parent()
        else:
            output("You are already in root")
            args[2].debug('Cannot go back, in root dir', program='Back')