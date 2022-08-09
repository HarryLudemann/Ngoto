# contains function to show logs
from ngoto.core.util.command import Command
from ngoto.core.util.interface import output
class Logs(Command):

    def get_description(self):
        return "Show logs"

    def get_actions(self):
        return ["logs", "l"]

    def perform_action(self, *args):
        output(args[2].get_log())