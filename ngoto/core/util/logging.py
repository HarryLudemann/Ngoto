from rich.style import Style
from rich.table import Table
import time


class Row:
    def __init__(self, time, level, program, message):
        self.time = time
        self.level = level
        self.program = program
        self.message = message


class Logging():
    log: list = []  # current log
    table: Table = None

    title_style = Style(color="blue", blink=False, bold=True)
    border_style = Style(color="black", blink=False, bold=True)
    header_style = Style(color="black", blink=False, bold=True)

    danger_style = Style(color="red", blink=False, bold=True)
    success_style = Style(color="green", blink=False, bold=True)
    warning_style = Style(color="yellow", blink=False, bold=True)
    debug_style = Style(color="blue", blink=False, bold=True)

    def save_log(self) -> None:
        with open("log.txt", "w") as f:
            for row in self.log:
                f.write(
                    row.time + " " +
                    row.level + " " +
                    row.program + " " +
                    row.message + "\n")

    def convert_level(self, level: str) -> str:
        level = level.upper()
        result = -1
        if level == "DEBUG":
            result = 1
        elif level == "INFO":
            result = 2
        elif level == "WARNING":
            result = 3
        elif level == "ERROR":
            result = 4
        elif level == "CRITICAL":
            result = 5
        return result

    def level_style(self, level: str) -> Style:
        level = level.upper()
        result = self.debug_style
        if level == "DEBUG":
            result = self.debug_style
        elif level == "INFO":
            result = self.success_style
        elif level == "WARNING":
            result = self.warning_style
        elif level == "ERROR":
            result = self.danger_style
        elif level == "CRITICAL":
            result = self.danger_style
        return result

    def get_log(self, level) -> Table:
        self.table = Table(
            title="Ngoto Logs",
            title_style=self.title_style,
            border_style=self.border_style)
        self.table.add_column(
            "Time", justify="center", header_style=self.header_style)
        self.table.add_column(
            "Level", justify="center", header_style=self.header_style)
        self.table.add_column(
            "Program", justify="center", header_style=self.header_style)
        self.table.add_column(
            "Message", justify="left", header_style=self.header_style)
        if level in ["1", "2", "3", "4", "5"]:
            level = int(level)
            for row in self.log:
                if level <= self.convert_level(row.level):
                    self.table.add_row(
                        row.time,
                        row.level,
                        row.program,
                        row.message,
                        style=self.level_style(row.level))
            return self.table
        else:
            self.warning("Invalid level", "Logs")
            return self.get_log("1")

    def debug(self, msg: str, program: str = '') -> None:
        self.log.append(Row(time.strftime("%H:%M:%S"), "DEBUG", program, msg))

    def info(self, msg: str, program: str = '') -> None:
        self.log.append(Row(time.strftime("%H:%M:%S"), "INFO", program, msg))

    def warning(self, msg: str, program: str = '') -> None:
        self.log.append(Row(
            time.strftime("%H:%M:%S"), "WARNING", program, msg))

    def error(self, msg: str, program: str = '') -> None:
        self.log.append(Row(time.strftime("%H:%M:%S"), "ERROR", program, msg))

    def critical(self, msg: str, program: str = '') -> None:
        self.log.append(Row(
            time.strftime("%H:%M:%S"),
            "CRITICAL", program, msg))
