# contains function open folder
from ngoto.util.command import Command 
from ngoto.util import interface
import os

class OpenFolder(Command):
    def getDescription(self):
        return "Command to open folder"

    def getActions(self):
        return ['openFolder', 'openF']

    def performAction(self, *args):
        pos = args[0].get_child(int(args[1][1])-1)
        pos.set_parent(args[0])
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        interface.options(pos)
        return pos
