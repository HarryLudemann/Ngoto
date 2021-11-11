# script contains two main classes:
# OSINT (controls osint modules and api keys)  
# HazzahCLT (Controls Command line tool interface)

from ngoto.utilities import Workplace, Interface, Table, Node
from os.path import exists # check config file exists
import logging
import sys
import os
import json

from ngoto.utilities.plugin import Plugin


class Ngoto:
    """ Main abstract class, contains api info and tree information """
    __version__ = '0.0.17'
    clearConsole = lambda self: os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
    api_keys = {} # dict of api keys
    root: Node
    curr_position: Node

    def add_api(self, name: str, key: str):
        self.api_keys[name] = key
    def get_api(self, name: str):
        return self.api_keys[name]

    def load_plugins(self, curr_node: Node, file_path: str) -> Node:
        """ Recursive function to traverse plugin directory adding each folder to tree and each plugin to node"""
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
    """ Module class """

    def __init__(self) -> None:
        import requests
        if not exists('configuration/'):
            os.mkdir('configuration/')
        if not exists('configuration/plugin/'):
            os.mkdir('configuration/plugin/')
            
            # get current pre installed plugins into list
            modules = []
            url = 'https://github.com/HarryLudemann/Hazzah-OSINT/tree/main/configuration/plugin'
            open_tag = '<span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title="'
            r = requests.get(url)
            for line in r.text.split('\n'):
                if open_tag in line:
                    modules.append(line.replace(open_tag, '').split('"', 1)[0].strip())

            # download plugins
            for module in modules:
                r = requests.get('https://raw.githubusercontent.com/HarryLudemann/Hazzah-OSINT/main/configuration/plugin/' + module.lower())
                with open(f'configuration/plugin/{module.lower()}.py', 'w') as f:
                    f.write(r.text)
        # load plugins
        self.root = self.load_plugins(Node('root'), "configuration/plugin/")
        self.curr_position = self.root

    def get_plugin(self, name: str, node: Node) -> Plugin:
        """ recursive method given plugins name returns plugin, returns None if not found """
        for plugin in node.get_plugins():
            if plugin.name == name:
                return plugin 
        for child in node.get_children():
            self.get_plugin(name, child)
        
    def get_plugin_context(self, plugin_name, args):
        """ Get context from plugin, given plugin name & list of args """
        return self.get_plugin(plugin_name, self.root).get_context(args)

class CLT(Ngoto):
    """ Command line tool class """
    current_pos = "[Ngoto]"
    current_workplace = "None" # Name
    workplace = None # current workplace object
    file_path ='configuration/workplace/' # workplace file path
    interface = Interface()

    def load_config(self) -> None:
        """ Loads plugins from plugins directory """
        # check Configuration, workplace and plugins folder exist else create
        if not exists('configuration/'):
            os.mkdir('configuration/')
        if not exists('configuration/workplace/'):
            os.mkdir('configuration/workplace/')
        if not exists('configuration/plugin/'):
            os.mkdir('configuration/plugin/')
        # load config file of api keys and set
        if exists('configuration/config.json'):
            with open("configuration/config.json") as json_data_file:
                data = json.load(json_data_file)
                for name in data['API']:
                    self.add_api(name, data['API'][name])
        else:
            logging.warning("No config.json found")
  
        self.root = self.load_plugins(Node('root'), "configuration/plugin/")
        self.curr_position = self.root

    # recursive function to print tree
    def print_tree(self, node: Node, indent: str = '') -> None:
        for plugin in node.get_plugins():
            self.interface.output(f'{indent}{plugin.name} - {plugin.version} - {plugin.description}')
        for child in node.get_children():
            self.print_tree(child, indent + '   ')

    # Workplace command method
    def workplace_command(self, options: list) -> None:
        """ determines requested wp option, given list of options """
        if len(options) >= 2:
            if options[1] == 'create':  # create wp
                self.workplace = Workplace(self.file_path)
                self.current_workplace = options[2]
                self.workplace.create_workplace(options[2])
                self.interface.output(f"Successfully created {options[2]} workplace")
            elif options[1] == 'join':
                self.workplace = Workplace(self.file_path)
                self.current_workplace = options[2]
                self.workplace.run_command(options[2], '')  # test connection to db
                self.interface.output(f"Successfully joined {options[2]} workplace")
            elif options[1] == 'setup':
                query = ''
                for plugin in self.plugins:
                    plugin = plugin()
                    query += '\n' + plugin.create_table()
                self.workplace.run_script(self.current_workplace, query)  # test connection to db
                self.interface.output(f"Successfully setup {self.current_workplace} workplace tables")
            elif options[1] == 'delete':
                file_exists = exists(f"{self.file_path}{options[2]}.sqlite")
                if file_exists:
                    os.remove(f"{self.file_path}{options[2]}.sqlite")
                    self.workplace = None
                    self.current_workplace = "None"
                    logging.info(f"Deleted workplace {options[2]}")
                    self.interface.output(f"Successfully deleted {options[2]} workplace")
                else:
                    logging.warning("Workplace already does not exist")
            elif options[1] == 'leave':  # create wp
                self.workplace = None
                self.current_workplace = ''
                self.interface.output(f"Successfully left workplace")
        else:
            logging.warning("No such command")

    def save_to_workplace(self, context: dict, plugin_name: str) -> None:
        """ Saves context dict to given plugins name table in current workplace if any
        either adds all vars in context to array, or if item is array creates row of that array """
        values = []
        added_row = False
        first_var = True
        for name in context:
            if first_var and type(context[name]) == list:
                added_row = True
                for item in context[name]:
                    self.workplace.add_row(self.current_workplace, plugin_name, [item])
            else:
                values.append(context[name])
            first_var = False
        if not added_row:
            self.workplace.add_row(self.current_workplace, plugin_name, values)

    # main operation function to start
    def main(self) -> None:
        context = {}                  
        option = self.interface.get_input('', '', self.current_pos)
        if not option.isdigit() or option == '0':   # if option is command not plugin/module
            option = option.split()
            if not option: # if empty string 
                pass
            elif option[0] in ['wp', 'workplace']:
                self.workplace_command(option)
            elif option[0] in ['o', 'options']:
                self.interface.options(self.current_workplace, self.curr_position)
            elif option[0] in ['c', 'commands']:
                self.interface.commands()
            elif option[0] in ['b', 'back']:
                if self.curr_position.has_parent:
                    self.curr_position = self.curr_position.get_parent()
                    self.clearConsole()
                    self.interface.options(self.current_workplace, self.curr_position)
                else:
                    self.interface.output("You are already in root")
            elif option[0] in ['cls', 'clear']:
                self.clearConsole()
            elif option[0] in ['0', 'q', 'exit']:
                sys.exit()
            elif option[0] in ['p', 'plugins']:
                self.print_tree(self.curr_position)
            else:
                self.interface.output("Unknown command")
        else:   # must be osint function
            # load and call plugin or go into folder
            if int(option)-1 < self.curr_position.num_children: # if folder
                self.curr_position.get_child(int(option)-1).set_parent(self.curr_position)
                self.curr_position = self.curr_position.get_child(int(option)-1)
                self.clearConsole()
                self.interface.options(self.current_workplace, self.curr_position)
            elif int(option)-1 < self.curr_position.num_children + self.curr_position.num_plugins: # if plugin
                plugin = self.curr_position.get_plugin( int(option[0]) - self.curr_position.num_children - 1)
                context = plugin.main(self)
                if context:
                    plugin.print_info(self, context, Table())
            else:
                self.interface.output(f"Plugin not found\n{self.curr_position.name}\n{self.curr_position.num_plugins}")

            if self.workplace: # save if within workplace
                if context:
                    self.save_to_workplace(context, plugin.name)

        self.main()