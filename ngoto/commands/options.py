# contains function to show options
from ngoto import CommandBase, show_options, clear_screen


class Options(CommandBase):
    def get_description(self):
        return "Show plugins/options"

    def get_actions(self):
        return ['o', 'options', 'ls']

    def perform_action(self, pos, options, logger):
        clear_screen()
        show_options(pos)
        logger.debug('Showing options', program='Options')
        return pos
