from ngoto.core.util.task import Task

class CPUTemp(Task):
    id = "PCUsage"
    delay = 30
    description = "CPU Temp"
    last_output = ""
    iteration = 0
    active = True
    os: list = ['Linux']

    def get_cpu_temp(self):
        import psutil
        """ Author: pimoroni """
        t = psutil.sensors_temperatures()
        for x in ['cpu-thermal', 'cpu_thermal']:
            if x in t:
                return t[x][0].current
        print("Warning: Unable to get CPU temperature!")
        return 0 

    def __call__(self) -> bool:
        cpu_temp = self.get_cpu_temp()
        self.last_output = f"CPU temp: {cpu_temp}"
        self.iteration += 1
        return [self.last_output, self.id]