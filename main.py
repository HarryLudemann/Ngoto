# this script is to launch the command line tool
import logging
import traceback
from os.path import exists # check config file exists
import hazzah


if __name__ == '__main__':
    hz = hazzah.HazzahCLT()
    try:
        hz.load_config()
        hz.clearConsole()
        hz.interface.options(hz)
        hz.main()
    except Exception as e:
        print(f"{hz.interface.bcolors.ENDC}")
        logging.error(traceback.format_exc())
    finally:
        print(f"{hz.interface.bcolors.ENDC}")
        