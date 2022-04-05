# contains function to show logs
from ngoto.util.command import Command
from ngoto.util import interface
class Logs(Command):

    def getDescription(self):
        return "Command to prints logs"

    def getActions(self):
        return ["logs", "l"]

    def performAction(self, *args):
        interface.output(args[2].get_log())