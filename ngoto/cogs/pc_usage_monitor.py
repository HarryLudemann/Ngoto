# contains function open plugin
from ngoto.core.decorators import task
from subprocess import check_output


def get_gpu_memory_map() -> list:
    """
        Returns List, all memory info in mb
        [0] Memory used,
        [1] Total memory
        [2] Free memory
        [3] Power draw
    """
    result = check_output(
        [
            'nvidia-smi',
            '--query-gpu=memory.used,memory.total,memory.free,power.draw',
            '--format=csv,nounits,noheader'
        ], shell=False)
    return result.decode('utf-8').strip().split(',')


class Tasks():
    @classmethod
    @task(name='PCUsage', delay=30, id='pcusage', os=['Windows'],
          desc="RAM and CPU Usage Notifier, Req winsdk module")
    def pc_usage(self):
        from ngoto import notify
        import psutil
        ram_usage = psutil.virtual_memory()[2]
        cpu_usage = psutil.cpu_percent()
        self.last_output = f"RAM used: {ram_usage}\nCPU used: {cpu_usage}"
        self.iteration += 1
        if ram_usage > 80 or cpu_usage > 80:
            notify("Computer Usage", self.last_output)
        return [self.last_output, self.id]

    @classmethod
    @task(name='NvidiaGPUUsage', delay=30, id='nvidia', os=['Windows'],
          desc="Nvidia GPU Usage Notifier")
    def nvidia_usage(self):
        from ngoto import notify
        usage = get_gpu_memory_map()
        if len(usage) > 3:
            if int(usage[2]) < 2048:
                notify("Nivida GPU Usage", "Less than 1gb gpu memory free")
            self.last_output = ''.join([
                f"GPU Memory Used: {usage[0]}MB",
                f"\nTotal Memory: {usage[1]}MB",
                f"\nFree Memory: {usage[2]}MB",
                f"\nPower Draw: {usage[3]}"])
            self.iteration += 1
            return [self.last_output, self.id]
        self.last_output = "Failed to get gpu memory map, usage: "
        self.last_output += str(usage)
        self.iteration += 1
        return [self.last_output, self.id]


def setup():
    return Tasks()
