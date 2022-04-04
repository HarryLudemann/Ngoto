from ngoto.util import interface

class Logging():
    levels: list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    level: int = 2 # position in levels of selected level
    log: str = f'\n{interface.bcolors.ENDC}' # current log

    def __init__(self, level: str = 'INFO'):
        self.setLevel(level)

    def setLevel(self, level: str) -> None:
        if level in self.levels:
            self.level = self.levels.index(level) + 1

    def getLevel(self) -> str:
        return self.level

    def get_log(self, lines: int = -1) -> str:
        if lines == -1:
            return self.log
        # if less then lines in lines, return all
        if lines < len((split_log := self.log.split('\n'))):
            return self.log
        else:
            return '\n'.join(split_log[-lines:])

    def logging_print(self, msg: str, level: int) -> None:
        if level == 1: # debug
            self.log += f'{interface.bcolors.OKBLUE}[DEBUG]{msg}{interface.bcolors.ENDC}\n'
        elif level == 2: # info
            self.log += f'{interface.bcolors.OKGREEN}[INFO]{msg}{interface.bcolors.ENDC}\n'
        elif level == 3: # warning 
            self.log += f'{interface.bcolors.WARNING}[WARNING]{msg}{interface.bcolors.ENDC}\n'
        elif level == 4: # error
            self.log += f'{interface.bcolors.FAIL}[ERROR]{msg}{interface.bcolors.ENDC}\n'
        elif level == 5: # critical
            self.log += f'{interface.bcolors.FAIL}[CRITICAL]{msg}{interface.bcolors.ENDC}\n'

    def debug(self, msg: str) -> None:
        if self.level >= 1:
            self.logging_print(msg, 1)
    
    def info(self, msg: str) -> None:
        if self.level >= 2:
            self.logging_print(msg, 2)
    
    def warning(self, msg: str) -> None:
        if self.level >= 3:
            self.logging_print(msg, 3)
    
    def error(self, msg: str) -> None:
        if self.level >= 4:
            self.logging_print(msg, 4)
    
    def critical(self, msg: str) -> None:
        if self.level >= 5:
            self.logging_print(msg, 5)
