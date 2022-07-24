# contains function to show options 
from ngoto.util.command import Command 
from ngoto.util import interface
from sys import platform

class Os(Command):
    def getDescription(self):
        return "Command to current os"

    def getActions(self):
        return ['os']

    def performAction(self, *args):
        if platform == "linux" or platform == "linux2":
            os = "Linux"
        elif platform == "darwin":
            os = "MacOS"
        elif platform == "win32":
            os = "Windows"
        args[2].debug(f'Current OS: ' + os, program='OS')
        return None # dont need to move from root
