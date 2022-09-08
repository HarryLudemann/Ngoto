# contains function to show logs
from ngoto import CommandBase, output


class Logs(CommandBase):

    def get_description(self):
        return "Show logs"

    def get_actions(self):
        return ["logs", "l"]

    def perform_action(self, pos, options, logger):
        if len(options) == 2:
            output(logger.get_log(options[1]))
        else:
            output(logger.get_log("1"))
        return pos
