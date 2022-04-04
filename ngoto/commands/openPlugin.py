# contains function open plugin
from ngoto.util.command import Command 
from ngoto.util import interface, Table
import os

class OpenPlugin(Command):
    def getDescription(self):
        return "Command to open plugin"

    def getActions(self):
        return ['openPlugin', 'openP']

    def performAction(self, *args):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        plugin = args[0].get_plugin( int(args[1][1]) - args[0].num_children - 1) # get chosen plugin
        if context := plugin.main(args[2]): # if context print resulting plugins information
            plugin.print_info(context, Table()) 
        else: # if a plugin that returns no context print options
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            interface.options(args[0])
        return args[0]
