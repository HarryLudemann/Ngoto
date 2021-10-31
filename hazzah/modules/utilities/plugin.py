from abc import ABC, abstractmethod 
import sys
from hazzah.modules.utilities.tables import Table

class Plugin(ABC):
    name = ''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    class Tables(Table):
        """Inherits table functions accessable from osint module"""
        def __init__(self):
            pass

    def get_input(self, text='', position=''):
        """ Get input method, returns string of input, exits program if input is exit"""
        user_input = str( input(f'{self.OKCYAN}{self.BOLD}[Hazzah]' + position + f'{self.ENDC}{self.BOLD} > ' + str(text)) )
        if user_input in ['0', 'exit']:  
            sys.exit()
        return user_input

    @abstractmethod  
    def create_table(self):
        """ function that returns string of sqlite query to create table """
        pass

    @abstractmethod 
    def main(self): 
        """ Main function to handle purpose """ 
        pass
