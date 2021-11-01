# this script is to load configuration and launch the command line tool

import logging
import traceback
import json
import os
from os.path import exists # check config file exists
import hazzah

hz = hazzah.HazzahCLT()
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
    bcolors = hz.interface.bcolors()
    try:
        clearConsole()
        hz.interface.options(hz)
        hz.main()
    except Exception as e:
        print(f"{bcolors.ENDC}")
        logging.error(traceback.format_exc())
    finally:
        print(f"{bcolors.ENDC}")
        