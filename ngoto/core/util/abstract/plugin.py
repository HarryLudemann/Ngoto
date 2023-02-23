# script contains abstract class all plugins inherit from and must use

from abc import ABC, abstractmethod


class PluginBase(ABC):
    """
    A abstract class used to represent an Plugin,
    a plugin is a function run once.

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
    req_modules: list = []  # given in the pip install name
    parameters: list = []  # for get context
    os: list = []  # stores working os eg. Windows, Linux, MacOS

    @abstractmethod
    def get_context(self):
        """ function that returns context dict of information,
            given required args """
        pass

    @abstractmethod
    def print_info(self, context):
        """ given context dictionary, prints results """
        pass

    @abstractmethod
    def main(self, logger):
        """ Main function to handle input and call get_context method """
        pass


class Plugin:
    def __init__(self, func, args, kwargs, name, desc,
                 req_modules, os, folder):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.desc = desc
        self.func = func
        self.folder = folder
        if req_modules:
            self.req_modules = req_modules
        else:
            self.req_modules = []
        if os:
            self.os = os
        else:
            self.os = ['Windows', 'MacOS', 'Linux']

    def execute(self, logger):
        return self.func(self, logger)

    def __call__(self, logger) -> bool:
        return self.execute(logger=logger)


def plugin(name: str, desc="", req_modules=None, os=None, folder=''):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Plugin(
                func, args, kwargs, name, desc=desc,
                req_modules=req_modules, os=os, folder=folder)
        return wrapper
    return decorator
