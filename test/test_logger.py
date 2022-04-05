import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ngoto.util import Logging

def test_logger_add():
    """ Test logger by adding debug message and checking in logs"""
    logger: Logging = Logging()
    logger.debug('debug')
    assert(logger.get_log() == '\n\x1b[0m\x1b[94m[DEBUG]debug\x1b[0m\n')

def test_logger_level():
    """ Checks logger if on lower level message is not in log"""
    logger: Logging = Logging()
    logger.error('info')
    assert(logger.get_log().strip() == '\x1b[0m')
