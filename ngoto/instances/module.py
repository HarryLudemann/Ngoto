
__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

from ngoto.util import Node, Plugin
from ngoto.instances.ngotoBase import NgotoBase 
import requests

class Module(NgotoBase):
    """ Module class, contains Module specific methods """
    def __init__(self):
        """ Gets list of plugins from github dir, downloads plugins, loads plugins into tree """
        self.check_dirs()
        # load plugins into tree
        self.root: Node = self.load_plugins(Node('root'), self.plugin_path)
        self.curr_pos: Node = self.root

    def download_plugins(self) -> None:
        """ Download/update all plugins (does not create folders) stores all plugins in plugin dir """
        for url in self.get_plugins_urls():
            r = requests.get(url)
            with open(self.plugin_path + url.replace('https://raw.githubusercontent.com/HarryLudemann/Ngoto/main/configuration/plugin/', ''), 'w') as f:
                f.write(r.text)

    def get_plugins_urls(self, path = 'https://github.com/HarryLudemann/Ngoto/tree/main/configuration/plugin/', modules = []):
        """ Recursive function Given string of plugin directory from github returns list of plugin URLS """
        open_tag = '<span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title="'
        r = requests.get(path)
        for line in r.text.split('\n'):
            if open_tag in line:
                plugin_name = line.replace(open_tag, '').split('"', 1)[0].strip()
                if plugin_name[0].isupper():
                    self.get_plugins_urls(path + plugin_name + '/', modules)
                else:
                    modules.append(path.replace('https://github.com/HarryLudemann/Ngoto/tree', 'https://raw.githubusercontent.com/HarryLudemann/Ngoto') + plugin_name)
        return modules

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