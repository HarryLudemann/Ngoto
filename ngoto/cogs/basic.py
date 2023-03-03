# contains function to clear screen
from ngoto.core.util.interface import output
from ngoto.core.util.interface import show_options, show_commands, clear_screen
from ngoto.core.decorators import command


class Basic():
    """ Basic commands for ngoto eg. exit, clear, back"""
    @staticmethod
    @command(name='logs', aliases=['l'], desc='Display logs')
    def log(self, logger, options):
        if len(options) == 2:
            output(logger.get_log(options[1]))
        else:
            output(logger.get_log("1"))
        return self.curr_pos

    @staticmethod
    @command(name='clear', aliases=['cls'], desc='Clear screen')
    def clear(self, logger, options):
        clear_screen()
        logger.debug('Clearing screen', program='Clear')
        return self.curr_pos

    @staticmethod
    @command(name='options', aliases=['o', 'ls'], desc='Display Options')
    def options(self, logger, options):
        clear_screen()
        show_options(self.curr_pos)
        logger.debug('Showing options', program='Options')
        return self.curr_pos

    @staticmethod
    @command(name='exit', aliases=['q'], desc='Exit ngoto')
    def exit(self, logger, options):
        output("Exiting...")
        logger.save_log()
        logger.info("Exiting ngoto")
        logger.debug('Exiting ngoto', program='Exit')
        exit()

    @staticmethod
    @command(name='commands', aliases=['c', 'h', 'help'], desc='Exit ngoto')
    def commands(self, logger, options):
        show_commands(self.commands)

    @staticmethod
    @command(name='tasks', aliases=['t'], desc='Exit ngoto')
    def tasks(self, logger, options):
        self.tasks.run_command(options, self.os, self.logger)

    @staticmethod
    @command(name='back', aliases=['b'], desc='Back out of plugin etc')
    def back(self, logger, options):
        if self.curr_pos.has_parent:
            clear_screen()
            parent = self.curr_pos.get_parent()
            show_options(parent)
            logger.debug(
                f'Going back to {parent.get_name()}',
                'Back')
            return parent
        else:
            output("You are already in root")
            logger.debug('Cannot go back, in root dir', program='Back')

    @staticmethod
    @command(name='openPlugin', aliases=['openP'], desc='Open plugin')
    def open_plugin(self, logger, options):
        plugin = self.curr_pos.get_plugin(int(options[0]) - self.curr_pos.num_children - 1)
        if not plugin(logger=logger):  # if context print
            clear_screen()
            show_options(self.curr_pos)
        logger.debug(f'Opening plugin {plugin.name}', program='OpenPlugin')
        return self.curr_pos

    @staticmethod
    @command(name='openFolder', aliases=['openF'], desc='Open folder')
    def open_folder(self, logger, options):
        folder = self.curr_pos.get_child(int(options[0])-1)
        folder.set_parent(self.curr_pos)
        clear_screen()
        show_options(folder)
        logger.debug(
            f'Opening folder {folder.get_name()}',
            program='OpenFolder')
        return folder


def setup():
    return Basic()
