# contains function to show logs
from ngoto import CommandCog, command, output


class Logs(CommandCog):
    @command(name='logs', aliases=['l'], help='Display logs')
    def perform_action(self, pos, options, logger):
        if len(options) == 2:
            output(logger.get_log(options[1]))
        else:
            output(logger.get_log("1"))
        return pos


def setup():
    return Logs()
