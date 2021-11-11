import socket
from ngoto import Plugin

class Plugin(Plugin):
    name = 'URL'
    version = 0.1
    description = 'Search URL'

    def get_info(self, target_url):
        """ Given target URL returns urls ip
            returns dict
        """
        context = {
            'ip': socket.gethostbyname(target_url)
        }
        return context

    def main(self, hz):
        target = hz.interface.get_input("Target URL: ", '[URL]', hz.curr_path)
        if target == 'back': return {}
        return self.get_info(target)

    def print_info(self, hz, context, tables):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [item, context[item]] )
        hz.interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    def get_context(self, args):
        return self.get_info(args[0])

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS url (
        id integer PRIMARY KEY AUTOINCREMENT,
        ip text );
        '''