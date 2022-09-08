# contains function open plugin
from ngoto import CommandBase, show_options, clear_screen


class OpenPlugin(CommandBase):
    def get_description(self):
        return "Open plugin"

    def get_actions(self):
        return ['openPlugin', 'openP']

    def perform_action(self, pos, options, logger):
        plugin = pos.get_plugin(int(options[0]) - pos.num_children - 1)
        if context := plugin.main(logger):  # if context print
            plugin.print_info(context)
        else:  # if a plugin that returns no context print options
            clear_screen()
            show_options(pos)

        logger.debug(f'Opening plugin {plugin.name}', program='OpenPlugin')
        return pos
