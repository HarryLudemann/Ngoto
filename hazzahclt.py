import os   # for clearing console
import sys  # for exiting
import logging 
import traceback
# logging.basicConfig(encoding='utf-8', level=logging.DEBUG) # filename='example.log', 
import json # storing config values
from os.path import exists # check config file exists
from hazzah import osint # import osint module

class hazzahclt(osint):
    class bcolors:
        """ Stores colours """
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    current_pos = "[Hazzah]"
    current_workplace = "None" # Name
    workplace = None # current workplace object
    file_path ='configuration/workplace/' # workplace file path

    plugins = [] # list of plugins
    def add_plugin(self, plugin):
        self.plugins.append(plugin)
    def get_plugins(self):
        return self.plugins

    # UI Methods
    def logo(self):
        bcolors = self.bcolors()
        print(f'''{bcolors.BOLD}{bcolors.HEADER}
     _   _                    _     
    | | | |                  | |    
    | |_| | __ _ __________ _| |__  
    |  _  |/ _` |_  /_  / _` | '_ \ 
    | | | | (_| |/ / / / (_| | | | |
    \_| |_/\__,_/___/___\__,_|_| |_|      
        {bcolors.ENDC}''')

    def options(self):
        self.logo()
        bcolors = self.bcolors()
        options = f'{bcolors.BOLD}\n0. Exit'
        for index, plugin in enumerate(self.plugins):
            options += f'\n{index+1}. {plugin.name}'
        print(options + f'\n\nWorkplace: {self.current_workplace}\n{bcolors.ENDC}')

    def commands(self):
        self.logo()
        print(f'''
    {bcolors.HEADER}[Basic]{bcolors.ENDC}{bcolors.BOLD}
    o/options                   --  Returns osint options
    c/commands                  --  Returns this list of commands
    cls/clear                   --  Clear console
    0/exit                      --  closes program

    {bcolors.HEADER}[Workplace]{bcolors.ENDC}{bcolors.BOLD}
    wp/workshop create (NAME)   --  Creates (NAME) workplace
    wp/workshop join (NAME)     --  Joins (NAME) workplace
    wp/workshop delete (NAME)   --  Deletes (NAME) workplace
    wp/workshop leave           --  Leave current workplace
        {bcolors.ENDC}''')

    # Workplace command method
    def workplace_command(self, options):
        """ determines requested wp option, given list of options """
        if len(options) >= 2:
            if options[1] == 'create':  # create wp
                self.workplace = osint.Wp(self.file_path)
                self.current_workplace = options[2]
                self.workplace.create_workplace(options[2])
                self.output(f"Successfully created {options[2]} workplace")
            elif options[1] == 'join':
                self.workplace = osint.Wp(self.file_path)
                self.current_workplace = options[2]
                self.workplace.run_command(options[2], '')  # test connection to db
                self.output(f"Successfully joined {options[2]} workplace")
            elif options[1] == 'setup':
                query = ''
                for plugin in self.plugins:
                    plugin = plugin()
                    query += '\n' + plugin.create_table()
                self.workplace.run_script(self.current_workplace, query)  # test connection to db
                self.output(f"Successfully setup {self.current_workplace} workplace tables")
            elif options[1] == 'delete':
                file_exists = exists(f"{self.file_path}{options[2]}.sqlite")
                if file_exists:
                    os.remove(f"{self.file_path}{options[2]}.sqlite")
                    self.workplace = None
                    self.current_workplace = "None"
                    logging.info(f"Deleted workplace {options[2]}")
                    self.output(f"Successfully deleted {options[2]} workplace")
                else:
                    logging.warning("Workplace already does not exist")
            elif options[1] == 'leave':  # create wp
                self.workplace = None
                self.current_workplace = ''
                self.output(f"Successfully left workplace")
        else:
            logging.warning("No such command")

    # input output methods
    def output(self, output):
        """ Print Method """
        bcolors = self.bcolors()
        print(f"{bcolors.BOLD} > ", output, f"{bcolors.ENDC}")

    
    def get_input(self, text='', position=''):
        """ Get input method, returns string of input, exits program if input is exit"""
        bcolors = self.bcolors()
        user_input = str( input(f"{bcolors.OKCYAN}{bcolors.BOLD}" + self.current_pos + position + f'{bcolors.ENDC}{bcolors.BOLD} > ' + str(text)) )
        if user_input in ['exit']:  
            sys.exit()
        return user_input

    # main operation function to start
    def main(self):
        context = {}                    # Init dict to store gathered information
        option = self.get_input('')     # Get user selected option eg 1-9
        if option not in ['1', '2', '3', '4', '5']:   # Insure input is 1-5
            option = option.split()
            if not option: # if empty string 
                pass
            elif option[0] in ['wp', 'workplace']:
                self.workplace_command(option)
            elif option[0] in ['o', 'options']:
                self.options()
            elif option[0] in ['c', 'commands']:
                self.commands()
            elif option[0] in ['cls', 'clear']:
                clearConsole()
            elif option[0] in ['0', 'exit']:
                sys.exit()
            else:
                self.output("Unknown command")
        else:   # must be osint function
            plugins = self.get_plugins()
            if int(option[0]) <= len( plugins ):
                # load and call plugin
                plugin = plugins[int(option[0]) - 1]
                plugin = plugin()
                context = plugin.main(self)
                plugin.print_info(context)

                # save to appropriate workplace if within
                if self.workplace:
                    # either adds all vars in context to array, or if item is array creates row of that array
                    values = []
                    added_row = False
                    first_var = True
                    for name in context:
                        if first_var and type(context[name]) == list:
                            added_row = True
                            for item in context[name]:
                                self.workplace.add_row(self.current_workplace, plugin.name, [item])
                        else:
                            values.append(context[name])
                        first_var = False
                    if not added_row:
                        self.workplace.add_row(self.current_workplace, plugin.name, values)

        self.main()


hz = hazzahclt()
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear') # lamba function to clear console

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
        hz.set_virus_total_api(data['API']['TOTAL_VIRUS_API_KEY'])
        hz.set_num_verify_api(data['API']['NUM_VERIFY_API_KEY'])
        hz.set_ip_quality_api(data['API']['IP_QUALITY_API_KEY'])
        hz.set_email_verification_api(data['API']['EMAIL_VERIFICATION_API_KEY'])
else:
    logging.warning("No config.json found")
# load plugins
for file in os.listdir("configuration/plugin/"):
    if file.endswith(".py"):
        mod = __import__('configuration.plugin.' + file[:-3], fromlist=['Plugin'])
        hz.add_plugin( getattr(mod, 'Plugin') )


if __name__ == '__main__':
    bcolors = hz.bcolors()
    try:
        clearConsole()
        hz.options()
        hz.main()
    except Exception as e:
        print(f"{bcolors.ENDC}")
        logging.error(traceback.format_exc())
    finally:
        print(f"{bcolors.ENDC}")
        
 
