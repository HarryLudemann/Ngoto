__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2021'

from ngoto.util import Node
from ngoto import constants as const
import os

class NgotoBase:
    """ Main abstract class, contains api info and tree information """
    curr_pos: Node = None # current position in plugin tree

    def getCurrentNode(self) -> Node:
        """ returns current node """
        if not self.curr_pos:
            self.curr_pos = self.load_plugins(Node('root'), const.plugin_path)
        return self.curr_pos

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

