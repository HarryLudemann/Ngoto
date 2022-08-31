
from ngoto.core.util.node import Node
import os


def load_plugins(curr_node: Node, file_path: str, curr_os: str) -> Node:
    """ Recursive function to traverse plugin directory adding
        each folder as node to tree and each plugin to node"""
    for file in os.listdir(file_path):
        if file.endswith(".py"):    # if python script
            mod = __import__(
                file_path.replace('/', '.') +
                file[:-3], fromlist=['Plugin'])
            plugin = getattr(mod, 'Plugin')()
            if curr_os in plugin.os:
                curr_node.add_plugin(plugin)
        elif '__pycache__' not in file:  # if folder
            new_node = Node(file + '/')  # create node of folder
            new_node = load_plugins(new_node, file_path + file + '/', curr_os)
            curr_node.add_child(new_node)
    return curr_node
