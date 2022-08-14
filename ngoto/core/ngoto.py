

from ngoto.core.util.node import Node
from ngoto.core.util.logging import Logging
import os
from sys import platform
from ngoto.core import constants as const 

class Ngoto:
    """ Base ngoto class for implementations of ngoto """
    curr_pos: Node = None # current position in plugin tree
    logger: Logging
    os: str = None # eg 'Linux', 'Windows', 'MacOS'

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            self.os = "Linux"
        elif platform == "darwin":
            self.os = "MacOS"
        elif platform == "win32":
            self.os = "Windows"

        self.curr_pos = self.load_plugins(Node('root'), const.plugin_path) # load plugins
        self.logger = Logging()

    def setLoggerLevel(self, level: str) -> None:
        """ Set logger level """
        self.logger.setLevel(level)

    def load_plugins(self, curr_node: Node, file_path: str) -> Node:
        """ Recursive function to traverse plugin directory adding each folder as node to tree and each plugin to node"""
        for file in os.listdir(file_path): 
            if file.endswith(".py"):    # if python script
                mod = __import__(file_path.replace('/', '.') + file[:-3], fromlist=['Plugin'])
                plugin = getattr(mod, 'Plugin')()
                if self.os in plugin.os:
                    curr_node.add_plugin( plugin )
            elif '__pycache__' not in file: # if folder
                new_node = Node(file + '/') # create node of folder
                new_node = self.load_plugins(new_node, file_path + file + '/') # add children to node
                curr_node.add_child( new_node )
        return curr_node
