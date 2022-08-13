# contains function to show logs
from ngoto.core.util.command import Command
from ngoto.core.util.interface import output
from ngoto.core.util.clear import clear_screen
class Logs(Command):

    def get_description(self):
        return "Show logs"

    def get_actions(self):
        return ["logs", "l"]

    def perform_action(self, _, options, logger):
        clear_screen()
        if len(options) == 2:
            output(logger.get_log(options[1]))
        else:
            output(logger.get_log("1"))