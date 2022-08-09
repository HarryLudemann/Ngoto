# contains function to show logs
from ngoto.util.command import Command
from ngoto.util import interface
class Logs(Command):

    def get_description(self):
        return "Show logs"

    def get_actions(self):
        return ["logs", "l"]

    def perform_action(self, *args):
        interface.output(args[2].get_log())