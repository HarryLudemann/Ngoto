from ngoto.core.util.interface import output, get_input
from ngoto.core.decorators import plugin
from ngoto.core.util.rich.table import Table
from ngoto.core.util.rich.style import Style
import socket

title_style = Style(color="blue", blink=False, bold=True)
border_style = Style(color="black", blink=False, bold=True)
header_style = Style(color="black", blink=False, bold=True)


def get_ip(self, target_url):
    try:
        ip = socket.gethostbyname(target_url)
    except socket.gaierror:
        self.logger.error(
            f'Could not get IP for URL {target_url}, socket.gaierror ',
            program='OSINT URL')
        ip = "Unknown - socket.gaierror"
    return ip


def print_info(url, ip):
    table = Table(
        title="Ngoto URL Plugin",
        title_style=title_style,
        border_style=border_style)
    table.add_column(
        "URL",
        justify="center",
        header_style=header_style)
    table.add_column(
        "IP",
        justify="center",
        header_style=header_style)
    table.add_row(url, ip)
    output(table)


class URL():
    """ Get IP for URL """
    @classmethod
    @plugin(name='URL', desc='Get IP for URL', folder='OSINT')
    def url(self, logger):
        self.logger = logger
        target = get_input("[URL] Target URL eg. thaturl.com: ")
        if target in ['back', 'b']:
            return {}
        logger.info(f'Getting IP for URL {target}', program='OSINT URL')
        ip = get_ip(self, target)
        logger.info(
            f'IP for URL {target} is {ip}',
            program='OSINT URL')
        print_info(target, ip)
        return True


def setup():
    return URL()
