# contains function to check plugins modules are installed
from ngoto.util.command import Command 
from ngoto import constants as const
import os
from os.path import exists

class Paths(Command):
    def get_description(self):
        return "Check paths in for plugins, commands and tasks exists"

    def get_actions(self):
        return ['paths']

    def perform_action(self, *args):
        args[2].debug(f'Checking paths', program='Paths')
        if not exists(const.plugin_path):
            os.mkdir(const.plugin_path)
        if not exists(const.command_path):
            os.mkdir(const.command_path)
        if not exists(const.task_path):
            os.mkdir(const.task_path)