# contains function open plugin
from ngoto.core.util.command import CommandBase
from ngoto.core.util.interface import options
import os


class OpenPlugin(CommandBase):
    def get_description(self):
        return "Open plugin"

    def get_actions(self):
        return ['openPlugin', 'openP']

    def perform_action(self, *args):
        plugin = args[0].get_plugin(int(args[1][1]) - args[0].num_children - 1)
        if context := plugin.main(args[2]):  # if context print
            plugin.print_info(context)
        else:  # if a plugin that returns no context print options
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            options(args[0])

        args[2].debug(f'Opening plugin {plugin.name}', program='OpenPlugin')
