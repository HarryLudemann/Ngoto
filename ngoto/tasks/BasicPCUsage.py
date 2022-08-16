from ngoto.core.util.task import Task


class BasicPCUsage(Task):
    id = "BasicPCUsage"
    delay = 30
    description = "RAM and CPU Usage Notifier, Req winsdk module"
    last_output = ""
    iteration = 0
    active = True
    os: list = ['Windows']

    def __call__(self) -> bool:
        from ngoto.core.util.notify import notify
        import psutil
        ram_usage = psutil.virtual_memory()[2]
        cpu_usage = psutil.cpu_percent()
        self.last_output = f"RAM used: {ram_usage}\nCPU used: {cpu_usage}"
        self.iteration += 1
        if ram_usage > 80 or cpu_usage > 80:
            notify("Computer Usage", self.last_output)
        return [self.last_output, self.id]
