
# Script contains functions to handle the clt input output paired with utils instance class

__author__ = 'Harry Ludemann'
__version__ = '0.0.21'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

import importlib
import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time
from ngoto.util import interface
from ngoto.instances.ngoto import NgotoBase  
from ngoto import constants as const
from ngoto.commands import *
from ngoto.tasks import *
import os
from ngoto.util.clear import clear_screen

class CLT(NgotoBase):
    """ Command line tool class, containing CLT specifc methods """
    commands = []
    tasks = []
    tasks_running = []

    def __init__(self):
        super().__init__()
        self.commands = self.load_from_folder(const.command_path)
        self.tasks = self.load_from_folder(const.task_path)

    def load_from_folder(self, folder: str) -> list:
        """ Loads all py files in folder as classes except init files, returns list of obj"""
        files = []
        # get command file paths
        files_paths = [c for c in os.listdir(folder) if c.endswith('.py') and not c.startswith('__')]
        for files_path in files_paths:
            module = folder.replace('/', '.') + '.' + files_path[:-3]
            mod = importlib.import_module(module)
            # get module name from path and capitalize first letter to get class name
            module_name = module.split(".")[2] 
            class_ = getattr(mod, module_name[0].upper() + module_name[1:])
            files.append(class_()) 
        return files

    def run_command(self, command: str, options: list = []) -> bool:
        if command.lower() in ['c', 'commands', 'h', 'help']: # display commands
            clear_screen()
            interface.commands(self.commands)
            return True
        elif len(options) == 4 and command.lower() in ['t', 'task']: # toggle tasks
            if command.lower() in ['t', 'tasks'] and options[1] == 'delay':
                self.set_delay(options[2], int(options[3]))
                return True
        elif len(options) == 3 and command.lower() in ['t', 'task']: # toggle tasks
            if command.lower() in ['t', 'task'] and options[1] in ['e', 'enable']:
                self.enable_task(options[2])
                return True
            elif command.lower() in ['t', 'task'] and options[1] in ['d', 'disable']:
                self.disable_task(options[2])
                return True
        elif command.lower() in ['t', 'task']: # display tasks
            clear_screen()
            interface.tasks(self.tasks)
            return True
        for cmd in self.commands:
            if command in cmd.get_actions():
                if (pos := cmd.perform_action(self.curr_pos, options, self.logger)) != None:
                    self.curr_pos = pos
                return True
        return False

    def enable_task(self, task_id: str) -> None:
        """ Enable task """
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.active = True
                self.logger.info('Enabled task: ' + task.id)
                return
        self.logger.info('Task not found: ' + task_id)

    def disable_task(self, task_id: str) -> None:
        """ Disable task """
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.active = False
                self.logger.info('Disabled task: ' + task.id)
                return
        self.logger.info('Task not found: ' + task_id)

    def set_delay(self, task_id: str, delay: int) -> None:
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.delay = delay
                self.logger.info('Set delay of: ' + task.id + ' to ' + str(delay))
                return
        self.logger.info('Task not found: ' + task_id)

    def clt(self):
        """ CLT loop"""
        option = interface.get_input('\n[Ngoto] > ').split()
        if not option:
            pass
        elif (isDigit := option[0].isdigit()) and (num := int(option[0])-1) < self.curr_pos.num_children: # move into folder
            option = ['openF', option[0]]
        elif isDigit and  num < self.curr_pos.num_children + self.curr_pos.num_plugins: # open plugin
            option = ['openP', option[0]]
        if option != [] and not self.run_command(option[0], option): # check in commands
            interface.output("Unknown command")
        self.clt()

    def main(self) -> None:  
        """ Main loop """ 
        with ThreadPoolExecutor(max_workers=3) as executor: 
            clt_loop = executor.submit(self.clt)
            while True:
                curr_time = time()
                for task in self.tasks:
                    if (curr_time - task.last_run) > task.delay and task.active:
                        self.tasks_running.append(executor.submit(task))
                        task.last_run = curr_time
                for task in self.tasks_running:
                    if task.done():
                        self.logger.info(task.result()[0], task.result()[1])
                        self.tasks_running.remove(task)
                if clt_loop.done():
                    break
                sleep(1 - (time() - curr_time))
            
               

    def start(self) -> None:
        """ Start CLT """
        self.run_command('clear') # clear screen
        self.run_command('options') # options screen
        self.main()
        