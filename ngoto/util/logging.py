from ngoto.util import interface
from rich.style import Style
from rich.table import Table
import time

class Logging():
    log: str = '\n' # current log
    table: Table = None

    title_style = Style(color="blue", blink=True, bold=True)
    border_style = Style(color="black", blink=True, bold=True)
    header_style = Style(color="black", blink=True, bold=True)
    
    danger_style = Style(color="red", blink=True, bold=True)
    success_style = Style(color="green", blink=True, bold=True)
    warning_style = Style(color="yellow", blink=True, bold=True)
    debug_style = Style(color="blue", blink=True, bold=True)

    def __init__(self) -> None:
        self.table = Table(title="Ngoto Logs", title_style=self.title_style, border_style = self.border_style)   
        self.table.add_column("Time", justify="center", header_style=self.header_style)
        self.table.add_column("Level", justify="center", header_style=self.header_style)
        self.table.add_column("Program", justify="center", header_style=self.header_style)
        self.table.add_column("Message", justify="left", header_style=self.header_style)

    def get_log(self) -> Table:
        return self.table

    def print_log(self) -> None:
        interface.output(self.table)

    def logging_print(self, msg: str, level: int, program:str = '') -> None:
        # add row
        if level == 1: # debug
            self.log += f'[DEBUG]{msg}\n'
            self.table.add_row(time.strftime("%H:%M:%S"), 'DEBUG', program, msg, style=self.debug_style)
        elif level == 2: # info
            self.log += f'[INFO]{msg}\n'
            self.table.add_row(time.strftime("%H:%M:%S"), 'INFO', program, msg, style=self.success_style)
        elif level == 3: # warning 
            self.log += f'[WARNING]{msg}\n'
            self.table.add_row(time.strftime("%H:%M:%S"), 'WARNING', program, msg, style=self.warning_style)
        elif level == 4: # error
            self.log += f'[ERROR]{msg}\n'
            self.table.add_row(time.strftime("%H:%M:%S"), 'ERROR', program, msg, style=self.danger_style)
        elif level == 5: # critical
            self.log += f'[CRITICAL]{msg}\n'
            self.table.add_row(time.strftime("%H:%M:%S"), 'CRITICAL', program, msg, style=self.danger_style)

    def debug(self, msg: str, program: str = '') -> None:
        self.logging_print(msg, 1, program)
    
    def info(self, msg: str, program: str = '') -> None:
        self.logging_print(msg, 2, program)
    
    def warning(self, msg: str, program: str = '') -> None:
        self.logging_print(msg, 3, program)
    
    def error(self, msg: str, program: str = '') -> None:
        self.logging_print(msg, 4, program)
    
    def critical(self, msg: str, program: str = '') -> None:
        self.logging_print(msg, 5, program)
