

from ngoto.core.util.node import Node
from ngoto.core.util.logging import Logging
from sys import platform
from ngoto.core import constants as const
from ngoto.core.util.load_plugins import load_plugins


class Ngoto:
    """ Base ngoto class for implementations of ngoto """
    curr_pos: Node = None  # current position in plugin tree
    logger: Logging
    os: str = None  # eg 'Linux', 'Windows', 'MacOS'

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            self.os = "Linux"
        elif platform == "darwin":
            self.os = "MacOS"
        elif platform == "win32":
            self.os = "Windows"

        self.curr_pos = load_plugins(Node('root'), const.plugin_path, self.os)
        self.logger = Logging()
