# contains function to exit program
from ngoto.core.util.command import Command 
from ngoto.core.util.interface import output 
import sys

class Exit(Command):
    def get_description(self):
        return "Exit program"

    def get_actions(self):
        return ["q", "exit", "0", "&"]

    def perform_action(self, *args):
        output("Exiting...")
        args[2].info("Exiting ngoto")
        args[2].debug(f'Exiting ngoto', program='Exit')
        sys.exit()