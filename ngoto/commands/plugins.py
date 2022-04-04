# contains function to check plugins modules are installed
from ngoto.util.command import Command 
from ngoto.util import interface

class Plugins(Command):
    def check_modules(self, node) -> None:
        """ recursive function to check all plugins have required modules """
        success: str = [] # list of installed modules
        for plugin in node.get_plugins():
            success.extend(plugin.check_requirements())
        for child in node.get_children():
            self.check_modules(child)
        for module in success:
            interface.output(module)

    def getDescription(self):
        return "Command to check plugins modules are installed"

    def getActions(self):
        return ['p', 'plugins']

    def performAction(self, *args):
        self.check_modules(args[0])
        return args[0]
