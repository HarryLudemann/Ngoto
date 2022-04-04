# Base command class for all commands
from abc import ABC, abstractmethod

class Command(ABC):
 
    @abstractmethod
    def getDescription(self):
        pass

    @abstractmethod
    def getActions(self):
        pass

    @abstractmethod
    def performAction(self, *args):
        pass