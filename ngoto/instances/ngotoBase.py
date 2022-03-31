__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2021'

from ngoto.util import Node
import logging, os, json, pathlib
from os.path import exists 

class NgotoBase:
    """ Main abstract class, contains api info and tree information """
    clearConsole = lambda _: os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
    api_keys: dict = {} # dict of api keys
    root: Node # root of plugin tree
    config_path: str = '../configuration/'
    workplace_path: str = ''
    plugin_path = '../configuration/plugin/'

    def add_api(self, name: str, key: str):
        """ Add api by name and key """
        self.api_keys[name] = key
    def get_api(self, name: str) -> str:
        """ returns api string of name """
        return self.api_keys[name]

    def set_path(self, path_name: str, path: str): 
        """ Given path name eg. (config, workplace or plugin) sets given path """
        if path_name == 'CONFIG': self.config_path = path
        elif path_name == 'WORKPLACE': self.workplace_path = path
        elif path_name == 'PLUGIN': self.plugin_path = path

    def check_dirs(self):
        """ check and create required folders """
        if not exists(self.config_path):
            os.mkdir(self.config_path)
        if not exists(self.workplace_path):
            os.mkdir(self.workplace_path)
        if not exists(self.plugin_path):
            os.mkdir(self.plugin_path)

    def load_config(self) -> None:
        """ loads config vars from config.json, then calls load plugins command and sets to self.root """
        try: 
            path = f"{pathlib.Path(__file__).parent.resolve()}\\{self.config_path}config.json".replace('ngoto\\', '')
            with open(path) as json_data_file:
                data = json.load(json_data_file)
                # load apis
                for name in data['API']:
                    self.add_api(name, data['API'][name])
                # load paths
                for name in data['PATHS']:
                    self.set_path(name, data['PATHS'][name])
                self.check_dirs()
        except Exception as e:
            logging.error(e)
        # load plugins into tree
        self.root = self.load_plugins(Node('root'), self.plugin_path)
        self.curr_pos = self.root

    def load_plugins(self, curr_node: Node, file_path: str) -> Node:
        """ Recursive function to traverse plugin directory adding each folder as node to tree and each plugin to node"""
        for file in os.listdir(file_path): 
            if file.endswith(".py"):    # if python script
                mod = __import__(file_path.replace('/', '.') + file[:-3], fromlist=['Plugin'])
                plugin = getattr(mod, 'Plugin')()
                curr_node.add_plugin( plugin )
            elif '__pycache__' not in file: # if folder
                new_node = Node(file + '/') # create node of folder
                new_node = self.load_plugins(new_node, file_path + file + '/') # add children to node
                curr_node.add_child( new_node )
        return curr_node

    def check_modules(self, node: Node) -> None:
        """ recursive function to check all plugins have required modules """
        success: str = [] # list of installed modules
        for plugin in node.get_plugins():
            success.extend(plugin.check_requirements())
        for child in node.get_children():
            self.check_modules(child)
        for module in success:
            self.interface.output(module)
