# still needs to be flushed out

from ngoto.core.util import Node, Plugin
from ngoto.core.ngoto import Ngoto 

class Module(Ngoto):
    """ Module class, contains Module specific methods """
    def get_plugin(self, name: str, node: Node) -> Plugin:
        """ recursive method given plugins name returns plugin, returns None if not found """
        for plugin in node.get_plugins():
            if plugin.name == name:
                return plugin 
        for child in node.get_children():
            return self.get_plugin(name, child)
        
    def get_plugin_context(self, plugin_name: str, args: list) -> dict:
        """ Get context from plugin, given plugin name & list of args """
        return self.get_plugin(plugin_name, self.curr_pos).get_context(*args)

    def add_plugin(self, plugin: Plugin) -> None:
        """ Add plugin to current node """
        self.curr_pos.add_plugin(plugin)