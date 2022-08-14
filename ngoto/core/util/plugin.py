# script contains abstract class all plugins inherit from and must use

from abc import ABC, abstractmethod
import logging

class Plugin(ABC):
    """
    A abstract class used to represent an Plugin, a plugin is a function run once

    ...

    Attributes
    ----------
    name : str
        a formatted string with no spaces to represent the plugin
    description : str
        description of the tasks purpose
    version : str
        the version of the plugin
    req_modules : list[str]
        the required modules for the plugin to run
    req_apis : list[str]
        the required apis for the plugin to run
    parameters : list[str]
        the parameters for the plugin main function
    os : list[str]
        the operating systems the plugin is compatible with
    Methods
    -------
    get_context() -> dict
        Abstract method to return base information context dictionary
    print_info(context: dict)
        Abstract method to print base information context
    main()
        Abstract method for clt gets user input, retrieves and prints context
    
    """

    name: str = ''
    description: str = ''
    version: str = ''
    req_modules: list = [] # given in the pip install name
    req_apis: list = [] 
    parameters: list = [] # for get context
    os: list = [] # stores working os eg. Windows, Linux, MacOS

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
