from ngoto import CommandCog, command, show_options, output, clear_screen


class Back(CommandCog):
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
    return Back()
