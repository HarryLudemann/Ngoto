import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ngoto.util import Logging

def test_logger():
    logger: Logging = Logging()
    logger.setLevel('CRITICAL')
    logger.debug('debug')
    print(repr(logger.get_log()))
    assert(logger.get_log() == '\n\x1b[0m\x1b[94m[DEBUG]debug\x1b[0m\n')
