# contains function open plugin
from ngoto import CommandCog, command, show_options, clear_screen


class OpenPlugin(CommandCog):
    @command(name='openPlugin', aliases=['openP'], help='Open plugin')
    def open_plugin(self, pos, options, logger):
        plugin = pos.get_plugin(int(options[0]) - pos.num_children - 1)
        if context := plugin.main(logger):  # if context print
            plugin.print_info(context)
        else:  # if a plugin that returns no context print options
            clear_screen()
            show_options(pos)

        logger.debug(f'Opening plugin {plugin.name}', program='OpenPlugin')
        return pos


def setup():
    return OpenPlugin()
