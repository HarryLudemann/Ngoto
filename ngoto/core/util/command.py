# Base command class for all commands
from abc import ABC, abstractmethod


class CommandBase(ABC):

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def perform_action(self, *args):
        pass
