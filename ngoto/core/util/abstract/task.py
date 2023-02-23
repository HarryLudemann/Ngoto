class Task:
    id: str = ""
    last_output = ''
    iteration = 0
    last_run = 0

    def __init__(self, func, args, kwargs, name: str, delay: int, desc="",
                 active=True, os=None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.desc = desc
        self.func = func
        self.delay = delay
        self.active = active
        if os:
            self.os = os
        else:
            self.os = []

    def execute(self):
        return self.func(self)

    def __call__(self) -> bool:
        return self.execute()


def task(name: str, delay: int, desc="", active=True, os=None):
    """Decorator to add command to cog"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return Task(
                func, args, kwargs, name, delay, desc=desc, active=active,
                os=os)
        return wrapper
    return decorator
