import os   # for clearing console
import sys  # for exiting
import logging 
import json # storing config values
from hazzah import osint # import osint module
from os.path import exists # check config file exists

hz = osint() # initialize 
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear') # lamba function to clear console
# load config file of api keys and set
has_config = exists('config.json')
if has_config:
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
        hz.set_virus_total_api(data['TOTAL_VIRUS_API_KEY'])
        hz.set_num_verify_api(data['NUM_VERIFY_API_KEY'])
        hz.set_ip_quality_api(data['IP_QUALITY_API_KEY'])
else:
    logging.warning("No config.json found")


def options():
    """ Function that contains the visual menu/options"""
    print('''
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
    ''')

def main():
    """ Main controlling function """
    clearConsole()                      # Clear Console
    options()                           # Print Options
    context = {}                          # Init dict to store gathered information
    option = int(input('\nInput Option: '))    # Get user selected option eg 1-9
    if option not in [0, 1, 2, 3, 4, 5]:   # Insure input is 1-5
        logging.error("Valid inputs are 1-5")
    else:
        if option == 0: # exit
            sys.exit()
        if option == 1: # phones
            target = input("\nEnter target phone number: ")
            context = hz.get_phone_info(target)
        if option == 2: # emails
            target = input("\nEnter target email: ")
            context = hz.get_email_info(target)
        if option == 3: # IP
            target = input("\nEnter target IP: ")
            context = hz.get_ip_info(target)
        if option == 4: # URL
            target = input("\nEnter target URL: ")
            context = hz.get_url_info(target)
        if option == 5: # URL
            type = input("\nSearch f:file or w:website:")
            target = input("\nEnter query: ")
            if type == 'f':
                files = input("\nEnter file types eg. pdf xlsx docx: ").split()
                maxcount = input("\nOptionally enter max results ")
                context = hz.get_document_search(target, files, maxcount)
            elif type == 'w':
                websites = input("\nEnter websites eg facebook.com twitter.com: ").split()
                maxcount = input("\nOptionally enter max results ")
                context = hz.get_website_search(target, websites, maxcount)

        # Print information
        if option in [1, 2, 3, 4]:
            for name in context:
                print(f'{name}: {context[name]}')
        elif option is 5:
            for url in context['urls']:
                print(url)

    # Wait for key press to continue
    input("Press Enter to continue...")
    # Recall Menu
    main()


if __name__ == '__main__':              # Run function if running directly
    main()

    