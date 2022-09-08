# contains function open folder
from ngoto import CommandBase, show_options, clear_screen


class OpenFolder(CommandBase):
    def get_description(self):
        return "Open folder"

    def get_actions(self):
        return ['openFolder', 'openF']

    def perform_action(self, pos, options, logger):
        folder = pos.get_child(int(options[0])-1)
        folder.set_parent(pos)
        clear_screen()
        show_options(folder)
        logger.debug(
            f'Opening folder {folder.get_name()}',
            program='OpenFolder')
        return folder
