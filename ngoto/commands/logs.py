# contains function to show logs
from ngoto.util.command import Command
class Logs(Command):

    def getDescription(self):
        return "Command to prints logs"

    def getActions(self):
        return ["logs", "l"]

    def performAction(self, *args):
        print(args[2].get_log())