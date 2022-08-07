# Base command class for all tasks
from abc import ABC, abstractmethod
from time import time
from time import sleep

class Task:
    last_run = None
    id = ""
    delay = 1

    def __init__(self):
        self.last_run = time()

    @abstractmethod
    def __call__(self):
        pass