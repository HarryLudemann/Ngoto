# contains function to clear screen
from ngoto import CommandCog, command, clear_screen


class Clear(CommandCog):
    @command(name='clear', aliases=['cls'], help='Clear screen')
    def clear(self, pos, _, logger):
        clear_screen()
        logger.debug('Clearing screen', program='Clear')
        return pos


def setup():
    return Clear()
