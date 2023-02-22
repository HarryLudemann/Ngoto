import socket
from ngoto import PluginBase, Logging, output, get_input, Table, Style


class Plugin(PluginBase):
    name = 'URL'
    version = 0.1
    description = 'Search URL'
    req_modules: list = []
    logger: Logging = None
    parameters: list = []
    os: list = ['Linux', 'Windows', 'MacOS']

    table: Table = None  # used in this plugin
    title_style = Style(color="blue", blink=False, bold=True)
    border_style = Style(color="black", blink=False, bold=True)
    header_style = Style(color="black", blink=False, bold=True)

    @classmethod
    def __get_ip(self, target_url):
        try:
            ip = socket.gethostbyname(target_url)
        except socket.gaierror:
            self.logger.error(
                f'Could not get IP for URL {target_url}, socket.gaierror ',
                program='OSINT URL')
            ip = "Unknown - socket.gaierror"
        return ip

    # Returns dict of acquired information, given desired information
    def get_context(self, target_url):
        return {"ip": 'can only be used with clt'}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        target = get_input("[URL] Target URL eg. thaturl.com: ")
        if target in ['back', 'b']:
            return {}
        logger.info(f'Getting IP for URL {target}', program='OSINT URL')
        context = {'ip': self.__get_ip(target)}
        logger.info(
            f'IP for URL {target} is {context["ip"]}',
            program='OSINT URL')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(
            title="Ngoto URL Plugin",
            title_style=self.title_style,
            border_style=self.border_style)
        self.table.add_column(
            "Description",
            justify="center",
            header_style=self.header_style)
        self.table.add_column(
            "Value",
            justify="center",
            header_style=self.header_style)
        for item in context:
            if not isinstance(context[item], list):
                self.table.add_row(item, context[item], style=self.title_style)
        output(self.table)
