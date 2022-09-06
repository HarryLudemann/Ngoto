from ngoto.core import constants as const
from ngoto.core.util.interface import show_tasks
from ngoto.core.util.clear import clear_screen
from ngoto.core.util.load_scripts import load_scripts


class TaskController:
    tasks = []
    tasks_running = []

    def __init__(self) -> None:
        self.tasks = load_scripts(const.task_path)

    def enable_task(self, task_id: str, logger) -> None:
        """ Enable task """
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.active = True
                logger.info('Enabled task: ' + task.id)
        logger.info('Task not found: ' + task_id)

    def disable_task(self, task_id: str, logger) -> None:
        """ Disable task """
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.active = False
                logger.info('Disabled task: ' + task.id)
        logger.info('Task not found: ' + task_id)

    def set_delay(self, task_id: str, delay: int, logger) -> None:
        for task in self.tasks:
            if task.id == task_id or task_id == 'all':
                task.delay = delay
                logger.info(
                    'Set delay of: ' + task.id + ' to ' + str(delay))
        logger.info('Task not found: ' + task_id)

    def update_task(self, task, curr_time, os: str) -> bool:
        if ((curr_time - task.last_run) > task.delay and
                task.active and os in task.os and (
                curr_time - task.last_run) > task.delay):
            return True
        return False

    def check_available_tasks(self, executor, curr_time, os: str) -> None:
        for task in self.tasks:
            if self.update_task(task, curr_time, os):
                self.tasks_running.append(executor.submit(task))
                task.last_run = curr_time

    def check_running_tasks(self, logger):
        for task in self.tasks_running:
            if task.done():
                logger.info(task.result()[0], task.result()[1])
                self.tasks_running.remove(task)

    def run_command(self, options: list, os: str, logger):
        if len(options) == 4 and options[1] == 'delay':
            self.set_delay(options[2], int(options[3]), logger)
        elif len(options) == 3 and options[1] in ['e', 'enable']:
            self.enable_task(options[2], logger)
        elif len(options) == 3 and options[1] in ['d', 'disable']:
            self.disable_task(options[2], logger)
        else:  # show tasks status
            clear_screen()
            show_tasks(self.tasks, os)
