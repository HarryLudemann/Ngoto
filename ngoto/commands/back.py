from ngoto.core.util.command import CommandBase
from ngoto.core.util.interface import show_options, output
from ngoto.core.util.clear import clear_screen


class Back(CommandBase):

    def get_description(self):
        return "Back out of folder"

    def get_actions(self):
        return ['b', 'back']

    def perform_action(self, pos, _, logger):
        if pos.has_parent:
            clear_screen()
            parent = pos.get_parent()
            show_options(parent)
            logger.debug(
                f'Going back to {parent.get_name()}',
                'Back')
            return parent
        else:
            output("You are already in root")
            logger.debug('Cannot go back, in root dir', program='Back')
