
class Command:
    def __init__(self, func, args, kwargs, name: str, desc="", aliases=None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.desc = desc
        self.func = func
        if aliases:
            self.aliases = aliases
        else:
            self.aliases = []

    def execute(self):
        self.func(self.args, self.kwargs)


def command(name, desc='', aliases=None):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Command(
                func, args, kwargs, name, desc=desc, aliases=aliases)
        return wrapper
    return decorator
