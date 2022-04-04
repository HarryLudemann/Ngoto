# this script is to launch command line tool
from ngoto import CLT

if __name__ == '__main__':
    ngotoCLT = CLT()
    ngotoCLT.setLoggerLevel('CRITICAL')
    ngotoCLT.start()
        