from ngoto.core.util.node import Node
from ngoto.core.util.logging import Logging
from ngoto.core.util.task_controller import TaskController
from ngoto.core.util.interface import output, get_input
from ngoto.core.decorators import Command, Plugin, Task
from concurrent.futures import ThreadPoolExecutor
from ngoto import cogs as inbuilt_cogs
from sys import platform
import os
from time import sleep, time


def get_object_from_method(method):
    """ Returns object from method """
    num_args = method.__code__.co_argcount
    args = []
    for _ in range(num_args):
        args.append('')
    return method(*args)


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
        self.curr_pos = Node('root')
        cogs = [getattr(inbuilt_cogs, cog)() for cog in inbuilt_cogs.__all__]
        self.load_cogs(cogs)

    def add_plugin(self, plugin: Plugin, location: str) -> None:
        """ Add plugin to the correct point in tree """
        curr_node = self.curr_pos
        for folder in location.split('/'):
            if folder != '':
                # if folder exists in tree
                if curr_node.has_child(folder):
                    curr_node = curr_node.get_child_from_name(folder)
                else:  # if folder does not exist in tree
                    new_node = Node(folder)
                    curr_node.add_child(new_node)
                    curr_node = new_node
        curr_node.add_plugin(plugin)

    def load_cogs(self, cog_classes: list):
        """ Load cogs from list of classes """
        for cog in cog_classes:
            for method in dir(cog):
                if method[0] != '_':
                    method = getattr(cog, method)
                    method_object = get_object_from_method(method)
                    if isinstance(method_object, Command):
                        self.commands.append(method_object)
                    elif isinstance(method_object, Task):
                        method_object.logger = self.logger
                        self.tasks.add_task(method_object)
                    elif isinstance(method_object, Plugin):
                        self.add_plugin(method_object, method_object.folder)

    def load_cogs_from_folder(self, folder) -> None:
        """Load all commands in commands folders __init__ __all__ list """
        cogs, files_paths = [], []
        for c in os.listdir(folder):
            if c.endswith('.py') and not c.startswith('__'):
                files_paths.append(c)
        for files_path in files_paths:
            complete_path = folder + '/' + files_path
            complete_path = complete_path.replace('/', '.')[:-3]
            # load file and call setup function
            module = __import__(complete_path, fromlist=['setup'])
            cogs.append(module.setup())
        self.load_cogs(cogs)

    def run_command(self, command: str, options: list = []) -> bool:
        if command.isdigit():
            if (num := int(options[0])-1) < self.curr_pos.num_children:
                command = 'openFolder'
            elif num < self.curr_pos.num_children + self.curr_pos.num_plugins:
                command = 'openPlugin'
        for cmd in self.commands:
            if command in cmd.aliases or command == cmd.name:
                pos = cmd.func(self, self.logger, options)
                if pos:
                    self.curr_pos = pos
                return True
        return False

    def clt(self):
        """ CLT loop"""
        option = get_input('\n[Ngoto] > ').split()
        if not option:
            pass
        elif not self.run_command(option[0], option):
            output("Unknown command")
        self.clt()

    def start(self) -> None:
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
