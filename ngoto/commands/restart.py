# command to restart ngoto
from ngoto.util.command import Command
import os

class Restart(Command):

    def getDescription(self):
        return "Command to restart clt"

    def getActions(self):
        return ["restart", "r", "&"]

    def performAction(self, *args):
        args[2].debug(f'Restarting clt', program='Restart')
        args[2].info("Restarting ngoto")
        os.system("python main.py") # restart script
        exit() # exit this script
