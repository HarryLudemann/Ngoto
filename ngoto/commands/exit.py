# contains function to exit program
from ngoto.util.command import Command 
import sys

class Exit(Command):
    def getDescription(self):
        return "Command to exit program"

    def getActions(self):
        return ["q", "exit", "0"]

    def performAction(self, *args):
        args[2].info("Exiting ngoto")
        args[2].debug(f'Exiting ngoto', program='Exit')
        sys.exit()