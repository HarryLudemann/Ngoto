# Base command class for all commands
# from abc import ABC, abstractmethod


class Command:
    def __init__(self, func, args, kwargs, name: str, help="", aliases=[]):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.help = help
        self.aliases = aliases
        self.func = func

    def execute(self):
        self.func(self.args, self.kwargs)


class CommandCog:
    pass


def command(name, help='', aliases=[]):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Command(
                func, args, kwargs, name, help=help, aliases=aliases)
        return wrapper
    return decorator
