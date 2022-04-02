# this script is to launch command line tool
import logging
import traceback
from ngoto import CLT
from ngoto.util import interface

if __name__ == '__main__':
    ngotoCLT = CLT()
    try:
        ngotoCLT.run_command('clear')
        interface.options(ngotoCLT.getCurrentNode())
        ngotoCLT.main()
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print(f"{interface.bcolors.ENDC}")
        