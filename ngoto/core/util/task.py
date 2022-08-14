# Base command class for all tasks
from abc import ABC, abstractmethod
from time import time

class Task(ABC):
    """
    A abstract class used to represent an Task, a task is run every set delay

    ...

    Attributes
    ----------
    id : str
        a formatted string with no spaces to represent the task
    description : str
        description of the tasks purpose
    last_output : str
        the last output of the task
    delay : int
        the delay in seconds between runs
    iteration : int
        the number of times the task has run
    active : bool
        whether the task is active or not
    os : list
        the operating systems the task is compatible with

    Methods
    -------
    __call__()
        Abstract method to be implemented by all tasks
    """

    id: str = ""
    description = ""
    last_output = ""
    delay = 30
    iteration = 0
    active = False
    os: list = ['Linux', 'Windows', 'MacOS']

    def __init__(self):
        self.last_run = 0

    @abstractmethod
    def __call__(self):
        pass