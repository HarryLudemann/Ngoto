# contains function to exit program
from ngoto.commands.command import Command
import sys

class Exit(Command):
    def getDescription(self):
        return "Command to exit program"

    def getActions(self):
        return ["q", "exit", "0"]

    def performAction(self, *args):
        sys.exit()
        return args[0]