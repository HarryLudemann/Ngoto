# contains function to check modules are installed
from ngoto.commands.command import Command
from ngoto.util import interface
import os

class Commands(Command):
    def getDescription(self):
        return "Command to show commands"

    def getActions(self):
        return ['c', 'commands', 'h', 'help']

    def performAction(self, *args):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        interface.commands() 
        return args[0]
