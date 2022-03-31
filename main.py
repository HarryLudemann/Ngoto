# this script is to launch command line tool
import logging
import traceback
from ngoto.instances.clt import CLT

if __name__ == '__main__':
    hz = CLT()
    try:
        hz.load_config()
        hz.clearConsole()
        hz.interface.options(hz.root)
        hz.main()
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print(f"{hz.interface.bcolors.ENDC}")
        