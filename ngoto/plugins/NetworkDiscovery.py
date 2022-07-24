from ngoto.util import Plugin, Logging, interface
from rich.table import Table # used in this plugin
from rich.style import Style # used in this plugin



class Plugin(Plugin):
    name = 'Network Discovery'
    version = 0.1
    description = 'Network Discovery Tool'
    req_modules: list = ['Scapy']
    req_apis: list = []
    logger: Logging = None
    parameters: list = []
    os: list = ['Linux', 'MacOS']

    table: Table = None # used in this plugin 
    title_style = Style(color="blue", blink=False, bold=True) # used in this plugin
    border_style = Style(color="black", blink=False, bold=True) # used in this plugin
    header_style = Style(color="black", blink=False, bold=True) # used in this plugin

    # Returns dict of acquired information, given desired information
    def get_context(self, ip):
        import scapy.all as scapy  
        arp_req_frame = scapy.ARP(pdst = ip)

        broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
        result = []
        for i in range(0,len(answered_list)):
            client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
            result.append(client_dict)

        return result

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        target = interface.get_input("[Network Discovery] Target IP: ")
        if target in ['back', 'b']: return {}
        logger.info(f'Discovering Network...', program='Network Discovery')
        context = self.get_context(target)
        return context

    # given context of information prints information
    def print_info(self, context):
        return
        # self.table = Table(title="Ngoto URL Plugin", title_style=self.title_style, border_style = self.border_style)   
        # self.table.add_column("Description", justify="center", header_style=self.header_style)
        # self.table.add_column("Value", justify="center", header_style=self.header_style)
        # for item in context:
        #     if type(context[item]) != list:
        #         self.table.add_row(item, context[item], style=self.title_style)
        # interface.output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return
        # return '''
        # CREATE TABLE IF NOT EXISTS url (
        # id integer PRIMARY KEY AUTOINCREMENT,
        # ip text );
        # '''

if __name__ == '__main__':
    Plugin().get_context('192,168.56.1')