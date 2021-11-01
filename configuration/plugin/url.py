import socket
from hazzah import Plugin

class Plugin(Plugin):
    name = 'URL'

    def get_urls_info(self, target_url):
        """ Given target URL returns urls ip
            returns dict
        """
        context = {
            'ip': socket.gethostbyname(target_url)
        }
        return context

    def main(self, hz):
        target = hz.interface.get_input("Target URL: ", '[URL]', hz.current_pos)
        if target == 'back': return {}
        return self.get_urls_info(target)

    def print_info(self, hz, context):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [item, context[item]] )
        hz.interface.output( '\n' + self.Tables().get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS url (
        id integer PRIMARY KEY AUTOINCREMENT,
        ip text );
        '''
    
    




