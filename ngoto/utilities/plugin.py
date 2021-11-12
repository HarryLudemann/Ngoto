# script contains abstract class all plugins inherit from and must use

from abc import ABC, abstractmethod
import logging

class Plugin(ABC):
    name: str = ''
    version: str = ''
    description: str = ''
    req_modules: list = []
    req_apis: list = []

    def __str__(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def check_requirements(self) -> bool:
        """
        Checks if all required modules are installed
        """
        success: str = [] # modules successfully installed
        for module in self.req_modules:
            try:
                __import__(module)
                success.append(f'found {module} - for {self.name} plugin')
            except ImportError:
                logging.warning(f"No module named '{module}' found, cannot use {self.name}")
        return success

    @abstractmethod  
    def create_table(self):
        """ function that returns string of sqlite query to create appropriate table """
        pass

    @abstractmethod  
    def get_context(self):
        """ function that returns context dict of information, given required args """
        pass

    @abstractmethod  
    def print_info(self, context):
        """ given context dictionary, prints results """
        pass

    @abstractmethod 
    def main(self): 
        """ Main function to handle input and call get_context method """ 
        pass
