import os   # for clearing console
import sys  # for exiting
import logging 
logging.basicConfig(encoding='utf-8', level=logging.DEBUG) # filename='example.log', 
import json # storing config values
from hazzah import osint # import osint module
from os.path import exists # check config file exists

class hazzahclt(osint):
    current_pos = "[Hazzah]"
    current_workplace = "None" # Name
    workplace = None # current workplace object
    file_path ='workplace/' # workplace file path

    def workplace_command(self, options):
        """ determines requested wp option, given list of options """
        if len(options) >= 3:
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
            elif options[1] == 'delete':
                file_exists = exists(f"{file_path}{options[2]}.sqlite")
                if file_exists:
                    os.remove(f"{file_path}{options[2]}.sqlite")
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

    def output(self, output):
        """ Print Method """
        print(" > ", output)

    
    def get_input(self, text='', position=''):
        """ Get input method, returns string of input, exits program if input is exit"""
        user_input = str( input(self.current_pos + position + ' > ' + str(text)) )
        if user_input in ['exit']:  
            sys.exit()
        return user_input


    def options(self):
        print(f'''
     _   _                    _     
    | | | |                  | |    
    | |_| | __ _ __________ _| |__  
    |  _  |/ _` |_  /_  / _` | '_ \ 
    | | | | (_| |/ / / / (_| | | | |
    \_| |_/\__,_/___/___\__,_|_| |_|      

    0. Exit
    1. Phone
    2. Email
    3. IP
    4. URL
    5. Google Dorks

    Workplace: {self.current_workplace}
        ''')

    def commands(self):
        print(f'''
     _   _                    _     
    | | | |                  | |    
    | |_| | __ _ __________ _| |__  
    |  _  |/ _` |_  /_  / _` | '_ \ 
    | | | | (_| |/ / / / (_| | | | |
    \_| |_/\__,_/___/___\__,_|_| |_|      

    [Basic]
    o/options                   --  Returns osint options
    c/commands                  --  Returns this list of commands
    cls/clear                   --  Clear console
    0/exit                      --  closes program

    [Workplace]
    wp/workshop create (NAME)   --  Creates (NAME) workplace
    wp/workshop join (NAME)     --  Joins (NAME) workplace
    wp/workshop delete (NAME)   --  Deletes (NAME) workplace
    wp/workshop leave           --  Leave current workplace
        ''')


def main():
    """ Main controlling function """
    context = {}                          # Init dict to store gathered information
    option = hz.get_input('')     # Get user selected option eg 1-9
    if option not in ['1', '2', '3', '4', '5']:   # Insure input is 1-5
        option = option.split()
        if option[0] in ['wp', 'workplace']:
            hz.workplace_command(option)
        elif option[0] in ['o', 'options']:
            hz.options()
        elif option[0] in ['c', 'commands']:
            hz.commands()
        elif option[0] in ['cls', 'clear']:
            clearConsole()
        elif option[0] in ['0', 'exit']:
            sys.exit()
        elif option[0] in ['0', 'test']:
            from configuration.plugin.google import Plugin
        else:
            logging.error("Valid inputs are 1-5")
    else:   # must be osint function
        if option == '1': # phones
            target = hz.get_input("Target phone number: ", '[Phone]')
            context = hz.get_phone_info(target)
        elif option == '2': # emails
            target = hz.get_input("Target email: ", '[Email]')
            context = hz.get_email_info(target)
        elif option == '3': # IP
            target = hz.get_input("Target IP: ", '[IP]')
            context = hz.get_ip_info(target)
        elif option == '4': # URL
            target = hz.get_input("Target URL: ", '[URL]')
            context = hz.get_url_info(target)
        elif option == '5': # Google search
            type = hz.get_input("Search f:file or w:website:", '[Google]')
            target = hz.get_input("Enter query: ", '[Google]')
            if type == 'f':
                files = hz.get_input("Enter file types eg. pdf xlsx docx: ", '[Google]').split()
                maxcount = hz.get_input("Optionally enter max results ", '[Google]')
                context = hz.get_document_search(target, files, maxcount)
            elif type == 'w':
                websites = hz.get_input("Enter websites eg facebook.com twitter.com: ", '[Google]').split()
                maxcount = hz.get_input("Optionally enter max results ", '[Google]')
                context = hz.get_website_search(target, websites, maxcount)

        # Print information
        if option in ['1', '2', '3', '4', '5']:
            for name in context:
                if context[name] == list:
                    for url in context['urls']:
                        hz.output(url)
                else:
                    hz.output(f'{name}: {context[name]}')

            # save to appropraite workplace if within
            if hz.workplace:
                values = []
                for item in context:
                    values.append(context[item])
                if option == '1':
                    hz.workplace.add_row(hz.current_workplace, 'phone', values)
                if option == '2':
                    hz.workplace.add_row(hz.current_workplace, 'email', values)
                if option == '3':
                    hz.workplace.add_row(hz.current_workplace, 'ip', values)
                if option == '4':
                    hz.workplace.add_row(hz.current_workplace, 'url', values)
                if option == '5':
                    for item in context['urls']:
                        hz.workplace.add_row(hz.current_workplace, 'google', [item])
                        # need to optimize adding together
                        #google_values.append( tuple(item) )
                    #hz.workplace.add_muiltple_rows(hz.current_workplace, 'google', google_values)

    main()



file_path = 'workplace/'
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




if __name__ == '__main__':  # Run function if running directly
    clearConsole()
    hz.options()
    main()

    