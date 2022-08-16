from ngoto.core.util.task import Task
import subprocess


class NvidiaGPUUsage(Task):
    id = "NvidiaGPUUsage"
    delay = 30
    description = "Nvidia GPU Usage Notifier"
    last_output = ""
    iteration = 0
    active = True
    os: list = ['Windows']

    def get_gpu_memory_map(self) -> list:
        """
            Returns List, all memory info in mb
            [0] Memory used,
            [1] Total memory
            [2] Free memory
            [3] Power draw
        """
        result = subprocess.check_output(
            [
                'nvidia-smi',
                '--query-gpu=memory.used,memory.total,memory.free,power.draw',
                '--format=csv,nounits,noheader'
            ])
        return result.decode('utf-8').strip().split(',')

    def __call__(self) -> bool:
        from ngoto.core.util.notify import notify
        usage = self.get_gpu_memory_map()
        if len(usage) > 3:
            if int(usage[2]) < 2048:
                notify("Nivida GPU Usage", "Less than 1gb gpu memory free")
            self.last_output = ''.join([
                f"GPU Memory Used: {usage[0]}MB",
                "\nTotal Memory: {usage[1]}MB",
                "\nFree Memory: {usage[2]}MB",
                "\nPower Draw: {usage[3]}"])
            self.iteration += 1
            return [self.last_output, self.id]
        self.last_output = "Failed to get gpu memory map, usage: "
        self.last_output += str(usage)
        self.iteration += 1
        return [self.last_output, self.id]
