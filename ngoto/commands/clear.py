# contains function to clear screen
from ngoto.core.util.command import CommandBase
from ngoto.core.util.clear import clear_screen


class Clear(CommandBase):

    def get_description(self):
        return "Clear console"

    def get_actions(self):
        return ["cls", "clear"]

    def perform_action(self, pos, _, logger):
        clear_screen()
        logger.debug('Clearing screen', program='Clear')
        return pos
