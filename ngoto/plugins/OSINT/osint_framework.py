# this script loads the osint framework as tree from their github json file
# the main method allowing to traverse the load tree


from ngoto.core.util.plugin import Plugin
from ngoto.core.util.logging import Logging
from ngoto.core.util.interface import output, get_input
import requests, os, webbrowser

class Plugin(Plugin):
    class Node:
        """ Node of each item in OSINT framework tree """
        def __init__(self, name: str, type: str, url: str= None):
            self.name: str = name
            if url: self.url = url
            self.type: str = type
            self.children: list = [] # list of children nodes
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


    name = 'OSINT Framework'
    version = 0.1
    description = 'Search OSINT Framework'
    req_modules: list = []
    req_apis: list = []
    root: Node = None # Root Node
    logger: Logging = None
    parameters: list = []
    os: list = ['Linux', 'Windows', 'MacOS']

    
    def load_nodes(self):
        """ Loads nodes from the server into tree """
        framework_json_url = 'https://raw.githubusercontent.com/lockfale/OSINT-Framework/master/public/arf.json'
        r = requests.get(framework_json_url)
        return self.load_nodes_helper(r.json())

    def load_nodes_helper(self, json):
        """ Recursive function to load nodes, given children of node """
        if json['type'] == 'folder':
            node = self.Node(name=json['name'], type=json['type'])
            for child in json['children']:
                loaded_child = self.load_nodes_helper(child)
                loaded_child.set_parent(node)
                node.add_child( loaded_child )
        else:
            node = self.Node(name=json['name'], type=json['type'], url=json['url'])
        return node

    def run_tree(self, node):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
        child_count: str = 0
        output('0. Exit')
        for index, child in enumerate(node.get_children()):
            output(f'{str(index + 1)}. ' + child.get_name())
            child_count = index
        print('\n')
        option = get_input()
        if option in ['b', 'back', '0', 'q']: # move back in dir
            if node.has_parent:
                self.run_tree(node.get_parent())
            else:
                pass # stop
        elif option.isdigit(): 
            if int(option) <= child_count + 1:
                sel_child = node.get_child(int(option)-1)
                if sel_child.type == 'folder':
                    self.run_tree(sel_child)
                else:
                    self.logger.info('Opening url' + sel_child.url, program='OSINT Framework')
                    webbrowser.open(sel_child.url)
                    self.run_tree(node)
            else: # option out of bounds
                output('Option out of bounds')
                self.logger.warning('Option out of bounds', program='OSINT Framework')
                self.run_tree(node)
        else:
            self.logger.warning('Invalid option', program='OSINT Framework')
            output('Invalid option')


    # Returns dict of acquired information, given desired information
    def get_context(_):
        return {}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        logger.info('Starting OSINT Framework', program='OSINT Framework')
        logger.debug('Loading Nodes', program='OSINT Framework')
        try:  
            root = self.load_nodes()
        except Exception as e:
            import traceback, sys
            logger.error(f'Error loading nodes: {e}', program='OSINT Framework')
            traceback.print_exc(file=sys.stdout)
            return {}
        logger.debug('Showing Tree', program='OSINT Framework')
        self.run_tree(root)
        logger.info('Exited OSINT Framework', program='OSINT Framework')
        return {}

    # given context of information prints information
    def print_info(*_):
        pass



