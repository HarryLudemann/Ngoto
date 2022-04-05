import socket
from ngoto.util import Plugin
from ngoto.util import interface
from rich.table import Table # used in this plugin
from rich.style import Style # used in this plugin

class Plugin(Plugin):
    name = 'URL'
    version = 0.1
    description = 'Search URL'
    req_modules: list = []
    req_apis: list = []

    table: Table = None # used in this plugin 
    title_style = Style(color="blue", blink=True, bold=True) # used in this plugin
    border_style = Style(color="black", blink=True, bold=True) # used in this plugin
    header_style = Style(color="black", blink=True, bold=True) # used in this plugin

    # Returns dict of acquired information, given desired information
    def get_context(self, target_url):
        context = {
            'ip': socket.gethostbyname(target_url)
        }
        return context

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        target = interface.get_input("[URL] Target URL: ")
        if target in ['back', 'b']: return {}
        logger.info(f'Getting IP for URL {target}', program='OSINT URL')
        context = self.get_context(target)
        logger.info(f'IP for URL {target} is {context["ip"]}', program='OSINT URL')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(title="Ngoto Logs", title_style=self.title_style, border_style = self.border_style)   
        self.table.add_column("Description", justify="center", header_style=self.header_style)
        self.table.add_column("Value", justify="center", header_style=self.header_style)
        for item in context:
            if type(context[item]) != list:
                self.table.add_row(item, context[item], style=self.title_style)
        interface.output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS url (
        id integer PRIMARY KEY AUTOINCREMENT,
        ip text );
        '''