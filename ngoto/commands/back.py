# contains function to go back
from ngoto.core.util.command import CommandBase
from ngoto.core.util.interface import show_options, output
import os


class Back(CommandBase):

    def get_description(self):
        return "Back out of folder"

    def get_actions(self):
        return ['b', 'back']

    def perform_action(self, pos, _, logger):
        if pos.has_parent:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            show_options(pos.get_parent())
            logger.debug(
                f'Going back to {pos.get_parent().get_name()}',
                'Back')
            return pos.get_parent()
        else:
            output("You are already in root")
            logger.debug('Cannot go back, in root dir', program='Back')
