import socket
from ngoto.util import Plugin
from ngoto.util import interface

class Plugin(Plugin):
    name = 'URL'
    version = 0.1
    description = 'Search URL'
    req_modules: list = []
    req_apis: list = []

    # Returns dict of acquired information, given desired information
    def get_context(self, target_url):
        context = {
            'ip': socket.gethostbyname(target_url)
        }
        return context

    # main function to handle input, then calls and return get_context method
    def main(self):
        target = interface.get_input("Target URL: ", '[URL]', '')
        if target in ['back', 'b']: return {}
        return self.get_context(target)

    # given context of information prints information
    def print_info(self, context, tables):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [item, context[item]] )
        interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    # holds sqlite3 create table query to store information
    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS url (
        id integer PRIMARY KEY AUTOINCREMENT,
        ip text );
        '''