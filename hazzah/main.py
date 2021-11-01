# script contains two main classes:
# OSINT (controls osint modules and api keys)  
# HazzahCLT (Controls Command line tool interface)

from hazzah.modules.utilities import Workplace, Plugin, Table, Interface
from hazzah.modules import plugins
from os.path import exists # check config file exists
import logging
import sys
import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear') # lamba function to clear console

class OSINT:
    """ Contains API information aswell as OSINT modules """
    __version__ = '0.0.3'
    VIRUS_TOTAL_API_KEY = ''
    IP_QUALITY_API_KEY = ''
    NUM_VERIFY_API_KEY = ''
    EMAIL_VERIFICATION_API_KEY = ''

    # api key setters
    def set_virus_total_api(self, api_key):
        self.VIRUS_TOTAL_API_KEY = api_key
    def set_ip_quality_api(self, api_key):
        self.IP_QUALITY_API_KEY = api_key
    def set_num_verify_api(self, api_key):
        self.NUM_VERIFY_API_KEY = api_key
    def set_email_verification_api(self, api_key):
        self.EMAIL_VERIFICATION_API_KEY = api_key

    class Wp(Workplace):
        """Inherits workplace functions accessable from osint module"""
        def __init__(self, filepath='/workplace'):
            self.set_filepath(filepath)

    class Plugins(Plugin):
        """Inherits plugin functions accessable from osint module"""
        def __init__(self):
            pass

    class Interface(Interface):
        """Inherits plugin functions accessable from osint module"""
        def __init__(self):
            pass

    # # getters
    def get_ip_info(self, target_ip):
        if not self.IP_QUALITY_API_KEY:
            logging.error('IP Quality API key not set')
            return {}
        else:
            return plugins.get_ip_info(target_ip, self.IP_QUALITY_API_KEY)

    def get_phone_info(self, target_phone):
        if not self.NUM_VERIFY_API_KEY:
            logging.error('Num Verify API key not set')
            return {}
        return plugins.get_phone_info(target_phone, self.NUM_VERIFY_API_KEY)

    def get_email_info(self, target_email):
        return plugins.get_email_info(target_email, self.EMAIL_VERIFICATION_API_KEY)

    def get_url_info(self, target_url):
        return plugins.get_urls_info(target_url)

    def get_url_scan(self, target_url):
        if not self.VIRUS_TOTAL_API_KEY:
            logging.error('VirusTotal API key not set')
        return plugins.get_url_scan(target_url, self.VIRUS_TOTAL_API_KEY)

    def get_file_scan(self, target_name, target_files, target_string):
        if not self.VIRUS_TOTAL_API_KEY:
            logging.error('VirusTotal API key not set')
            return {}
        else:
            return plugins.get_file_scan(target_name, target_files, target_string, self.VIRUS_TOTAL_API_KEY)

    def get_website_search(self, query, websites, max_results=10):
        """Passed query, list of file types and optionally int of max results wanted"""
        return plugins.google_search(query, websites, 'site:', int(max_results))

    def get_document_search(self, query, filetypes, max_results=10):
        """Passed query, list of file types and optionally int of max results wanted"""
        return plugins.google_search(query, filetypes, 'filetype:', int(max_results))
    
class HazzahCLT(OSINT):
    """ Command line tool class """
    current_pos = "[Hazzah]"
    current_workplace = "None" # Name
    workplace = None # current workplace object
    file_path ='configuration/workplace/' # workplace file path
    interface = OSINT.Interface()

    plugins = [] # list of plugins
    def add_plugin(self, plugin):
        self.plugins.append(plugin)
    def get_plugins(self):
        return self.plugins

    # Workplace command method
    def workplace_command(self, options):
        """ determines requested wp option, given list of options """
        if len(options) >= 2:
            if options[1] == 'create':  # create wp
                self.workplace = OSINT.Wp(self.file_path)
                self.current_workplace = options[2]
                self.workplace.create_workplace(options[2])
                self.interface.output(f"Successfully created {options[2]} workplace")
            elif options[1] == 'join':
                self.workplace = OSINT.Wp(self.file_path)
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
                clearConsole()
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
                plugin.print_info(self, context)

                if self.workplace: # save if within workplace
                    self.save_to_workplace(context, plugin.name)

        self.main()