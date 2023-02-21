# import functools


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


commands = []


def command(name, help='', aliases=[]):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Command(
                func, args, kwargs, name, help=help, aliases=aliases)
        return wrapper
    return decorator


class CommandCog:
    pass


class Options(CommandCog):
    @command(name='options', help='Display Options', aliases=['o', 'ls'])
    def tester(self, pos, options, logger):
        print('testing')


for cog in [Options]:
    for method in dir(cog):
        if method[0] != '_':
            print(method)


# cog = Options()
# command = cog.tester("", "", "")
# command.func(cog, "", "", "")
