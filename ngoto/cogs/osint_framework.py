from ngoto.core.util.interface import output, get_input
from ngoto.core.decorators import plugin
from ngoto.core.util.rich.table import Table
from ngoto.core.util.rich.style import Style
import requests
import os
import webbrowser

title_style = Style(color="blue", blink=False, bold=True)
border_style = Style(color="black", blink=False, bold=True)
header_style = Style(color="black", blink=False, bold=True)


class Node:
    """ Node of each item in OSINT framework tree """
    def __init__(self, name: str, types: str, url: str = None):
        self.name: str = name
        if url:
            self.url = url
        self.types: str = types
        self.children: list = []  # list of children nodes
        self.parent = None

    def get_name(self) -> str:
        return self.name

    def set_parent(self, parent) -> None:
        """ Set parent node """
        self.parent = parent

    def get_parent(self):
        return self.parent

    @property
    def has_parent(self):
        if self.parent:
            return True
        return False

    def get_children(self) -> list:
        """ Returns list of children nodes """
        return self.children

    def get_child(self, index):
        return self.children[index]

    def add_child(self, child) -> None:
        self.children.append(child)


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


def load_nodes():
    """ Loads nodes from the server into tree """
    framework_json_url = 'https://raw.githubusercontent.com/'
    framework_json_url += 'lockfale/OSINT-Framework/master/public/arf.json'
    r = requests.get(framework_json_url)
    return load_nodes_helper(r.json())


def load_nodes_helper(json):
    """ Recursive function to load nodes, given children of node """
    if json['type'] == 'folder':
        node = Node(name=json['name'], types=json['type'])
        for child in json['children']:
            loaded_child = load_nodes_helper(child)
            loaded_child.set_parent(node)
            node.add_child(loaded_child)
    else:
        node = Node(
            name=json['name'], types=json['type'], url=json['url'])
    return node


def run_tree(node, logger):
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    child_count: str = 0
    output('0. Exit')
    for index, child in enumerate(node.get_children()):
        output(f'{str(index + 1)}. ' + child.get_name())
        child_count = index
    print('\n')
    option = get_input('> ')
    if option in ['b', 'back', '0', 'q']:  # move back in dir
        if node.has_parent:
            run_tree(node.get_parent(), logger)
        else:
            pass  # stop
    elif option.isdigit():
        if int(option) <= child_count + 1:
            sel_child = node.get_child(int(option)-1)
            if sel_child.types == 'folder':
                run_tree(sel_child, logger)
            else:
                logger.info(
                    'Opening url' + sel_child.url,
                    program='OSINT Framework')
                webbrowser.open(sel_child.url)
                run_tree(node, logger)
        else:  # option out of bounds
            output('Option out of bounds')
            logger.warning(
                'Option out of bounds', program='OSINT Framework')
            run_tree(node, logger)
    else:
        logger.warning('Invalid option', program='OSINT Framework')
        output('Invalid option')


class OSINTFramework():
    """ Explore OSINT Framework """
    @classmethod
    @plugin(name='OSINT Framework', desc='Explore OSINT Framework',
            folder='OSINT')
    def osint_framework(self, logger):
        logger.info('Starting OSINT Framework', program='OSINT Framework')
        logger.debug('Loading Nodes', program='OSINT Framework')
        root = load_nodes()
        logger.debug('Showing Tree', program='OSINT Framework')
        try:
            run_tree(root, logger)
        except Exception as e:
            print(e)
        logger.info('Exited OSINT Framework', program='OSINT Framework')
        return True


def setup():
    return OSINTFramework()
