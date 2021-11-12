# This script contains three main classes:

# Ngoto class contains functions & vars used in both children classes
# Module class in child of Ngoto containing functions & vars for modularized version
# CLT class contains functions & vars for Command line tool

__author__ = 'Harry Ludemann'
__maintainer__  = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2021'

from ngoto.utilities import Workplace, Interface, Table, Node, Plugin, workplace
import logging, sys, os, json, requests
from os.path import exists 

class Ngoto:
    """ Main abstract class, contains api info and tree information """
    clearConsole = lambda _: os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
    api_keys = {} # dict of api keys
    root: Node # root of plugin tree
    config_path: str = 'configuration/'
    workplace_path: str = ''
    plugin_path: str = ''

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

class Module(Ngoto):
    """ Module class, contains Module specific methods """
    def __init__(self):
        """ Gets list of plugins from github dir, downloads plugins, loads plugins into tree """
        self.config_path = 'configuration/'
        self.workplace_path ='configuration/workplace/' # workplace file path
        self.plugin_path = 'configuration/plugin/'
        self.check_dirs()
        # load plugins into tree
        self.root = self.load_plugins(Node('root'), self.plugin_path)
        self.curr_pos = self.root

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

class CLT(Ngoto):
    """ Command line tool class, containing CLT specifc methods """
    curr_path: str = "[Ngoto]" # string displayed in input prompt
    curr_pos: Node # current position in plugin tree
    workplace: Workplace = None # current workplace object, set when created or joined workplace
    interface: Interface # controls all interface commands
    def __init__(self):
        self.interface = Interface()

    @property
    def workpace_name(self):
        """ Returns workplace name, if None returns 'N/A'"""
        if self.workplace: return self.workplace.name
        else: return 'N/A'

    def add_position(self, position: str): # add path displayed in cmd input
        """ Add position to current path """
        self.curr_path += '['+ position.replace('/', '') + ']'
    def remove_position(self, position: str): # remove path displayed in cmd input
        """ Remove position from current path """
        self.curr_path = self.curr_path.replace('[' + position.replace('/', '') + ']', '')

    def load_config(self) -> None:
        """ loads config vars from config.json, then calls load plugins command and sets to self.root """
        try: 
            with open(f"{self.config_path}config.json") as json_data_file:
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

    def print_tree(self, node: Node, indent: str = '') -> None:
        """ recursive function to print tree in format """
        for plugin in node.get_plugins():
            self.interface.output(f'{indent}{plugin.name} - {plugin.version} - {plugin.description}')
        for child in node.get_children():
            self.print_tree(child, indent + '   ')

    def save_to_workplace(self, context: dict, plugin_name: str) -> None:
        """ Saves context dict to given plugins names table in current workplace,
        either adds all vars in context to array, or if item is array creates row of that array """
        values = []
        added_row = False
        first_var = True
        for name in context:
            if first_var and type(context[name]) == list: # if first var is list, add all vars in list
                added_row = True
                for item in context[name]:
                    self.workplace.add_row(self.workplace.name, plugin_name, [item])
            else:
                values.append(context[name]) # else add value
            first_var = False
        if not added_row:
            self.workplace.add_row(self.workplace.name, plugin_name, values)

    # Workplace command method
    def workplace_command(self, options: list) -> None:
        """ 
        determines requested workplace option, given list of options 
        if create, create workplace named option[2]
        elif join, join workplace named option[2] 
        elif setup, loop over all plugins creating the suggested table
        elif delete, deletes option[2] workplace
        elif leave, leaves current workplace
        else prints 'no such command
        """
        if len(options) >= 2:
            if options[1] == 'create':  # create wp
                self.workplace = Workplace(self.workplace_path, options[2])
                self.workplace.create_workplace(options[2])
                self.interface.output(f"Successfully created {options[2]} workplace")
            elif options[1] == 'join':
                self.workplace = Workplace(self.workplace_path, options[2])
                self.workplace.run_command(options[2], '')  # test connection to db
                self.interface.output(f"Successfully joined {options[2]} workplace")
            elif options[1] == 'setup':
                query = ''
                for plugin in self.plugins:
                    plugin = plugin()
                    query += '\n' + plugin.create_table()
                self.workplace.run_script(self.workplace.name, query)  # test connection to db
                self.interface.output(f"Successfully setup {self.workplace.name} workplace tables")
            elif options[1] == 'delete':
                file_exists = exists(f"{self.workplace_path}{options[2]}.sqlite")
                if file_exists:
                    os.remove(f"{self.workplace_path}{options[2]}.sqlite")
                    self.workplace = None
                    logging.info(f"Deleted workplace {options[2]}")
                    self.interface.output(f"Successfully deleted {options[2]} workplace")
                else:
                    logging.warning("Workplace already does not exist")
            elif options[1] == 'leave':  # create wp
                self.workplace = None
                self.interface.output(f"Successfully left workplace")
        else:
            logging.warning("No such command")

    def main(self) -> None:
        """ 
        Main CLT command calls functions, controls input, plugin calls and move between folders
        if input not digit or is 0 (must be command)
            if input is empty, pass
            elif wp or workplace, call workplace_command()
            elif o or options, print options eg. plugins, folders
            elif b or back, back out of folder into parent node
            elif cls or clear, clear command prompt
            elif if 0, q or exit, quit python script
            elif p, plugins, print all plugins in tree format
            else print 'unknown command'
        else (Must be plugin call or to move into child folder/node)
            if plugin, call and print plugin
            elif folder, move into child folder/node
            else print 'plugin not found'

            if within workplace, save result to workplace
        """
        context = {}                  
        option = self.interface.get_input('', '', self.curr_path)
        if not option.isdigit() or option == '0':   # if option is command not plugin/module
            option = option.split()
            if not option: # if empty string 
                pass
            elif option[0] in ['wp', 'workplace']:
                self.workplace_command(option)
            elif option[0] in ['o', 'options']:
                self.interface.options(self.curr_pos, self.workpace_name)
            elif option[0] in ['c', 'commands']:
                self.interface.commands()
            elif option[0] in ['b', 'back']: # !backing out of plugin is within plugin!
                if self.curr_pos.has_parent:
                    self.remove_position(self.curr_pos.name) # remove in position cmd
                    self.curr_pos = self.curr_pos.get_parent()
                    self.clearConsole()
                    self.interface.options(self.curr_pos, self.workpace_name)
                else:
                    self.interface.output("You are already in root")
            elif option[0] in ['cls', 'clear']:
                self.clearConsole()
            elif option[0] in ['0', 'q', 'exit']:
                sys.exit()
            elif option[0] in ['p', 'plugins']:
                self.print_tree(self.curr_pos)
            else:
                self.interface.output("Unknown command")
        else:   # must be plugin or into folder
            if int(option)-1 < self.curr_pos.num_children: # move into folder
                self.curr_pos.get_child(int(option)-1).set_parent(self.curr_pos) # set selected node as chosen's nodes parent
                self.curr_pos = self.curr_pos.get_child(int(option)-1) # set chosen node as curr node
                self.clearConsole()
                self.interface.options(self.curr_pos, self.workpace_name)
                self.add_position(self.curr_pos.name) # add folder to position path
            elif int(option)-1 < self.curr_pos.num_children + self.curr_pos.num_plugins: # if plugin
                plugin = self.curr_pos.get_plugin( int(option[0]) - self.curr_pos.num_children - 1) # get chosen plugin
                context = plugin.main(self) # run plugin
                if context: # if context print resulting plugins information
                    plugin.print_info(self, context, Table()) 
            else:
                self.interface.output(f"Plugin not found\n{self.curr_pos.name}\n{self.curr_pos.num_plugins}")

            if self.workplace: # save if within workplace
                if context:
                    self.save_to_workplace(context, plugin.name)

        self.main()