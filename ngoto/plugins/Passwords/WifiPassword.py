from ngoto.util import Plugin
from ngoto.util import interface, Logging
from rich.table import Table # used in this plugin
from rich.style import Style # used in this plugin
import subprocess

class Plugin(Plugin):
    name = 'Wifi Passwords'
    version = 0.1
    description = 'Get stored wifi passwords'
    req_modules: list = []
    req_apis: list = []
    logger: Logging = None
    parameters: list = []
    os: list = ['Linux', 'Windows', 'MacOS']

    table: Table = None # used in this plugin 
    title_style = Style(color="blue", blink=False, bold=True) # used in this plugin
    border_style = Style(color="black", blink=False, bold=True) # used in this plugin
    header_style = Style(color="black", blink=False, bold=True) # used in this plugin

    def get_context(self) -> list:
        return {"data": subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        logger.info(f'Getting Wifi Passwords', program='Wifi Passwords')
        context = self.get_context()
        logger.info(f'Successfully Got Wifi Passwords', program='Wifi Passwords')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(title="Ngoto Wifi Passwords Plugin", title_style=self.title_style, border_style = self.border_style)   
        self.table.add_column("Profile Name", style=self.header_style)
        self.table.add_column("Password", style=self.header_style)
        profiles = [i.split(":")[1][1:-1] for i in context['data'] if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    self.table.add_row(i, results[0])
                except IndexError:
                    self.table.add_row(i, "")
            except subprocess.CalledProcessError:
                self.table.add_row(i, "ENCODING ERROR")
        interface.output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return ''