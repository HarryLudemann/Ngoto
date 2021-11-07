from abc import ABC, abstractmethod

class Plugin(ABC):
    name = ''
    version = ''
    description = ''

    def get_name(self):
        return self.name

    @abstractmethod  
    def create_table(self):
        """ function that returns string of sqlite query to create table """
        pass

    @abstractmethod  
    def get_context(self):
        """ function that returns context dict given required args """
        pass

    @abstractmethod  
    def print_info(self, context):
        """ gets context dictionary, prints results """
        pass

    @abstractmethod 
    def main(self): 
        """ Main function to handle purpose """ 
        pass
