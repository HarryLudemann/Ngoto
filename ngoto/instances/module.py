# still needs to be flushed out

__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

from ngoto.util import Node, Plugin
from ngoto.util.ngotoBase import NgotoBase 

class Module(NgotoBase):
    """ Module class, contains Module specific methods """
    def __init__(self):
        self.curr_pos: Node = self.getCurrentNode() # load plugins into tree

    def get_plugin(self, name: str, node: Node) -> Plugin:
        """ recursive method given plugins name returns plugin, returns None if not found """
        for plugin in node.get_plugins():
            if plugin.name == name:
                return plugin 
        for child in node.get_children():
            return self.get_plugin(name, child)
        
    def get_plugin_context(self, plugin_name: str, args: list) -> dict:
        """ Get context from plugin, given plugin name & list of args """
        return self.get_plugin(plugin_name, self.root).get_context(*args)