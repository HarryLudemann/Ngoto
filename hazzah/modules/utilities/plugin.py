from abc import ABC, abstractmethod 
import sys
from hazzah.modules.utilities.tables import Table

class Plugin(ABC):
    name = ''
    class Tables(Table):
        """Inherits table functions accessable from osint module"""
        def __init__(self):
            pass

    @abstractmethod  
    def create_table(self):
        """ function that returns string of sqlite query to create table """
        pass

    @abstractmethod  
    def print_info(self, context):
        """ gets context dictionary, prints results """
        pass

    @abstractmethod 
    def main(self): 
        """ Main function to handle purpose """ 
        pass
