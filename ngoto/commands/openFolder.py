# contains function open folder
from ngoto import CommandCog, command, show_options, clear_screen


class OpenFolder(CommandCog):
    @command(name='openFolder', aliases=['openF'], help='Open folder')
    def open_folder(self, pos, options, logger):
        folder = pos.get_child(int(options[0])-1)
        folder.set_parent(pos)
        clear_screen()
        show_options(folder)
        logger.debug(
            f'Opening folder {folder.get_name()}',
            program='OpenFolder')
        return folder


def setup():
    return OpenFolder()
