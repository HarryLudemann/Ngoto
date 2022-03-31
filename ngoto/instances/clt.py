
# Script contains functions to handle the clt input output paired with utils instance class

__author__ = 'Harry Ludemann'
__version__ = '0.0.20'
__license__ = 'GPLv3' 
__copyright__ = 'Copyright of Harry Ludemann 2022'

from ngoto.util import Workplace, Interface, Table, Node
from ngoto.instances.ngotoBase import NgotoBase 
import logging, sys, os
from os.path import exists 

class CLT(NgotoBase):
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
            elif p, plugins, returns required modules for installed plugins
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
                self.clearConsole()
                self.interface.options(self.curr_pos, self.workpace_name)
            elif option[0] in ['c', 'commands', 'h', 'help']:
                self.interface.commands()
            elif option[0] in ['b', 'back', '&']: # !backing out of plugin is within plugin!
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
                self.check_modules(self.curr_pos)
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
                else: # if a plugin that returns no context print options
                    self.clearConsole()
                    self.interface.options(self.curr_pos, self.workpace_name)
            else:
                self.interface.output(f"Plugin not found\n{self.curr_pos.name}\n{self.curr_pos.num_plugins}")

            if self.workplace: # save if within workplace
                if context:
                    self.save_to_workplace(context, plugin.name)

        self.main()