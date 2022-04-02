# contains function to check plugins modules are installed
from ngoto.commands.command import Command
from ngoto import constants as const
import os
from os.path import exists

class Paths(Command):
    def getDescription(self):
        return "Command to check plugins and workplace paths exist, if not create them."

    def getActions(self):
        return ['paths']

    def performAction(self, *args):
        if not exists(const.workplace_path):
            os.mkdir(const.workplace_path)
        if not exists(const.plugin_path):
            os.mkdir(const.plugin_path)
        return args[0]