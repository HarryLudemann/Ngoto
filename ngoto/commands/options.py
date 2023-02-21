# contains function to show options
from ngoto import CommandCog, command, show_options, clear_screen


class Options(CommandCog):
    @command(name='options', aliases=['o', 'ls'], help='Display Options')
    def options(self, pos, _, logger):
        clear_screen()
        show_options(pos)
        logger.debug('Showing options', program='Options')
        return pos


def setup():
    return Options()
