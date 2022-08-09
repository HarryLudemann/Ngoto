# contains function to clear screen
from ngoto.core.util.command import Command
from ngoto.core.util.clear import clear_screen

class Clear(Command):

    def get_description(self):
        return "Clear console"

    def get_actions(self):
        return ["cls", "clear"]

    def perform_action(self, *args):
        clear_screen()
        args[2].debug(f'Clearing screen', program='Clear')
        return args[0]