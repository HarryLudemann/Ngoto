# contains function to exit program
from ngoto import CommandCog, command, output
import sys


class Exit(CommandCog):
    @command(name='exit', aliases=['q'], help='Exit ngoto')
    def exit(self, pos, options, logger):
        output("Exiting...")
        logger.save_log()
        logger.info("Exiting ngoto")
        logger.debug('Exiting ngoto', program='Exit')
        sys.exit()
        return pos


def setup():
    return Exit()
