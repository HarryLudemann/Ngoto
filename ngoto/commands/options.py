# contains function to show options
from ngoto import CommandBase, show_options, clear_screen


class Options(CommandBase):
    def get_description(self):
        return "Show plugins/options"

    def get_actions(self):
        return ['o', 'options', 'ls']

    def perform_action(self, *args):
        clear_screen()
        show_options(args[0])
        args[2].debug('Showing options', program='Options')
        return args[0]
