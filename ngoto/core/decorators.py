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


class Task:
    last_output = ''
    iteration = 0
    last_run = 0

    def __init__(self, func, args, kwargs, name: str, delay: int, id: str,
                 desc="", active=True, os=None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.desc = desc
        self.func = func
        self.delay = delay
        self.active = active
        self.id = id
        if os:
            self.os = os
        else:
            self.os = ['Windows', 'MacOS', 'Linux']

    def execute(self):
        return self.func(self)

    def __call__(self) -> bool:
        self.last_output = self.execute()
        return self.last_output


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


def task(name: str, delay: int, id: str, desc="", active=True, os=None):
    """Decorator to add task to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Task(
                func, args, kwargs, name, delay, id, desc=desc, active=active,
                os=os)
        return wrapper
    return decorator


def plugin(name: str, desc="", req_modules=None, os=None, folder=''):
    """Decorator to add plugin to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Plugin(
                func, args, kwargs, name, desc=desc,
                req_modules=req_modules, os=os, folder=folder)
        return wrapper
    return decorator


def command(name, desc='', aliases=None):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Command(
                func, args, kwargs, name, desc=desc, aliases=aliases)
        return wrapper
    return decorator
