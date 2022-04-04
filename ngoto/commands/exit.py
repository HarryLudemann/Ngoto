# contains function to exit program
from ngoto.util.command import Command 
from ngoto.util import interface
import sys

class Exit(Command):
    def getDescription(self):
        return "Command to exit program"

    def getActions(self):
        return ["q", "exit", "0"]

    def performAction(self, *args):
        print(f"{interface.bcolors.ENDC}") # reset colors
        args[2].info("Exiting ngoto")
        sys.exit()