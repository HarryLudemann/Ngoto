# script contains two main classes:
# OSINT (controls osint modules and api keys)  
# HazzahCLT (Controls Command line tool interface)

from hazzah.utilities import Workplace, Interface, Table
from os.path import exists # check config file exists
import logging
import sys
import os
import json

class OSINT:
    """ Contains API information aswell as OSINT modules """
    __version__ = '0.0.15'
    clearConsole = lambda self: os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
    plugins = [] # list of plugins
    api_keys = {} # dict of api keys

    def add_api(self, name, key):
        self.api_keys[name] = key
    def get_api(self, name):
        return self.api_keys[name]
    
    def add_plugin(self, plugin):
        self.plugins.append(plugin)
    def get_plugins(self):
        return self.plugins
    def get_plugin(self, name):
        for plugin in self.get_plugins():
            if plugin.name == name:
                return plugin

class Hazzah(OSINT):
    """ Module class """
    modules= ['Email', 'IP', 'URL', 'Google', 'Phone']

    def __init__(self):
        import requests
        if not exists('configuration/'):
            os.mkdir('configuration/')
        if not exists('configuration/plugin/'):
            os.mkdir('configuration/plugin/')
            
            for module in self.modules:
                r = requests.get('https://raw.githubusercontent.com/HarryLudemann/Hazzah-OSINT/main/configuration/plugin/' + module.lower() + '.py')
                with open(f'configuration/plugin/{module.lower()}.py', 'w') as f:
                    f.write(r.text)
        # load plugins
        for file in os.listdir("configuration/plugin/"):
            if file.endswith(".py"):
                mod = __import__('configuration.plugin.' + file[:-3], fromlist=['Plugin'])
                self.add_plugin( getattr(mod, 'Plugin') )

    def get_plugin_context(self, plugin_name, args):
        """ Get context from plugin, given plugin name & list of args """
        return self.get_plugin(plugin_name)().get_context(args)

class HazzahCLT(OSINT):
    """ Command line tool class """
    current_pos = "[Hazzah]"
    current_workplace = "None" # Name
    workplace = None # current workplace object
    file_path ='configuration/workplace/' # workplace file path
    interface = Interface()

    def load_config(self):
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
        # load plugins
        for file in os.listdir("configuration/plugin/"):
            if file.endswith(".py"):
                mod = __import__('configuration.plugin.' + file[:-3], fromlist=['Plugin'])
                self.add_plugin( getattr(mod, 'Plugin') )

    # Workplace command method
    def workplace_command(self, options):
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

    def save_to_workplace(self, context, plugin_name):
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
    def main(self):
        context = {}                  
        option = self.interface.get_input('', '', self.current_pos)
        if option not in ['1', '2', '3', '4', '5']:   # if option is command not plugin/module
            option = option.split()
            if not option: # if empty string 
                pass
            elif option[0] in ['wp', 'workplace']:
                self.workplace_command(option)
            elif option[0] in ['o', 'options']:
                self.interface.options(self)
            elif option[0] in ['c', 'commands']:
                self.interface.commands()
            elif option[0] in ['cls', 'clear']:
                self.clearConsole()
            elif option[0] in ['0', 'exit']:
                sys.exit()
            else:
                self.interface.output("Unknown command")
        else:   # must be osint function
            plugins = self.get_plugins()
            if int(option[0]) <= len( plugins ):
                # load and call plugin
                plugin = plugins[int(option[0]) - 1]
                plugin = plugin()
                context = plugin.main(self)
                plugin.print_info(self, context, Table())

                if self.workplace: # save if within workplace
                    self.save_to_workplace(context, plugin.name)

        self.main()