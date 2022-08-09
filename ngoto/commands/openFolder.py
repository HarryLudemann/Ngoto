# contains function open folder
from ngoto.util.command import Command 
from ngoto.util import interface
import os

class OpenFolder(Command):
    def get_description(self):
        return "Open folder"

    def get_actions(self):
        return ['openFolder', 'openF']

    def perform_action(self, *args):
        pos = args[0].get_child(int(args[1][1])-1)
        pos.set_parent(args[0])
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        interface.options(pos)
        args[2].debug(f'Opening folder {pos.get_name()}', program='OpenFolder')
        return pos
