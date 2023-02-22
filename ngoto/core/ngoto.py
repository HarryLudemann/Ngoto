from ngoto.core.util.node import Node
from ngoto.core.util.logging import Logging
from ngoto.core import constants as const
from ngoto.core.util.task_controller import TaskController
from ngoto.core.util.interface import show_commands, output, get_input
from concurrent.futures import ThreadPoolExecutor
from sys import platform
import os
from time import sleep, time


def load_plugins(curr_node: Node, file_path: str, curr_os: str) -> Node:
    """ Recursive function to traverse plugin directory adding
        each folder as node to tree and each plugin to node"""
    for file in os.listdir(file_path):
        if file.endswith(".py"):    # if python script
            mod = __import__(
                file_path.replace('/', '.') +
                file[:-3], fromlist=['Plugin'])
            plugin = getattr(mod, 'Plugin')()
            if curr_os in plugin.os:
                curr_node.add_plugin(plugin)
        elif '__pycache__' not in file:  # if folder
            new_node = Node(file + '/')  # create node of folder
            new_node = load_plugins(new_node, file_path + file + '/', curr_os)
            curr_node.add_child(new_node)
    return curr_node


def load_cogs(folder):
    """Load all commands in commands folders __init__ __all__ list """
    cogs, commands, files_paths = [], [], []
    for c in os.listdir(folder):
        if c.endswith('.py') and not c.startswith('__'):
            files_paths.append(c)
    for files_path in files_paths:
        complete_path = folder + '/' + files_path
        complete_path = complete_path.replace('/', '.')[:-3]
        # load file and call setup function
        module = __import__(complete_path, fromlist=['setup'])
        cogs.append(module.setup())

    for cog in cogs:
        # for each class method thats not inbuilt call and add returned
        for method in dir(cog):
            if method[0] != '_':
                method = getattr(cog, method)
                commands.append(method('', '', '', ''))
    return commands


class Ngoto:
    """ Base ngoto class for implementations of ngoto """
    curr_pos: Node = None  # current position in plugin tree
    logger: Logging
    os: str = None  # eg 'Linux', 'Windows', 'MacOS'
    tasks = TaskController()
    commands = []

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            self.os = "Linux"
        elif platform == "darwin":
            self.os = "MacOS"
        elif platform == "win32":
            self.os = "Windows"

        self.logger = Logging()
        self.curr_pos = load_plugins(Node('root'), const.plugin_path, self.os)
        self.commands = load_cogs(const.command_path)

    def run_command(self, command: str, options: list = []) -> bool:
        check_commands = True
        if command.isdigit():
            if (num := int(options[0])-1) < self.curr_pos.num_children:
                command = 'openFolder'
            elif num < self.curr_pos.num_children + self.curr_pos.num_plugins:
                command = 'openPlugin'
        elif command in ['c', 'commands', 'h', 'help']:  # display commands
            show_commands(self.commands)
            check_commands = False
        elif command in ['t', 'task']:
            self.tasks.run_command(options, self.os, self.logger)
            check_commands = False
        if check_commands:
            for cmd in self.commands:
                if command in cmd.aliases or command is cmd.name:
                    pos = cmd.func(self, self.curr_pos, options, self.logger)
                    if pos:
                        self.curr_pos = pos
                    return True
            return False
        else:
            return True

    def clt(self):
        """ CLT loop"""
        option = get_input('\n[Ngoto] > ').split()
        if not option:
            pass
        elif not self.run_command(option[0], option):
            output("Unknown command")
        self.clt()

    def main(self) -> None:
        """ Main loop """
        self.run_command('clear')
        self.run_command('options')
        with ThreadPoolExecutor(max_workers=3) as executor:
            clt_loop = executor.submit(self.clt)
            while True:
                curr_time = time()
                self.tasks.check_available_tasks(executor, curr_time, self.os)
                self.tasks.check_running_tasks(self.logger)
                if clt_loop.done():
                    break
                sleep(1 - (time() - curr_time))
