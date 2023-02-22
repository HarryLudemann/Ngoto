# contains function to clear screen
from ngoto import CommandCog, command, clear_screen, output, show_options
from sys import exit


class Basic(CommandCog):
    """ Basic commands for ngoto eg. exit, clear, back"""
    @command(name='logs', aliases=['l'], help='Display logs')
    def perform_action(self, pos, options, logger):
        if len(options) == 2:
            output(logger.get_log(options[1]))
        else:
            output(logger.get_log("1"))
        return pos

    @command(name='clear', aliases=['cls'], help='Clear screen')
    def clear(self, pos, _, logger):
        clear_screen()
        logger.debug('Clearing screen', program='Clear')
        return pos

    @command(name='options', aliases=['o', 'ls'], help='Display Options')
    def options(self, pos, _, logger):
        clear_screen()
        show_options(pos)
        logger.debug('Showing options', program='Options')
        return pos

    @command(name='exit', aliases=['q'], help='Exit ngoto')
    def exit(self, pos, options, logger):
        output("Exiting...")
        logger.save_log()
        logger.info("Exiting ngoto")
        logger.debug('Exiting ngoto', program='Exit')
        exit()
        return pos

    @command(name='back', aliases=['b'], help='Back out of plugin etc')
    def back(self, pos, _, logger):
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


def setup():
    return Basic()
