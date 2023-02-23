# contains function open plugin
from ngoto import command, show_options, clear_screen


class Open():
    """ Open commands for ngoto eg. openPlugin, openFolder"""
    @staticmethod
    @command(name='openPlugin', aliases=['openP'], desc='Open plugin')
    def open_plugin(_, pos, options, logger):
        plugin = pos.get_plugin(int(options[0]) - pos.num_children - 1)
        if not plugin(logger=logger):  # if context print
            clear_screen()
            show_options(pos)
        logger.debug(f'Opening plugin {plugin.name}', program='OpenPlugin')
        return pos

    @staticmethod
    @command(name='openFolder', aliases=['openF'], desc='Open folder')
    def open_folder(_, pos, options, logger):
        folder = pos.get_child(int(options[0])-1)
        folder.set_parent(pos)
        clear_screen()
        show_options(folder)
        logger.debug(
            f'Opening folder {folder.get_name()}',
            program='OpenFolder')
        return folder


def setup():
    return Open()
