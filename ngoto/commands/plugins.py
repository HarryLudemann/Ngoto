# contains function to check plugins modules are installed
from ngoto.core.util.command import Command 
from ngoto.core.util.interface import output

class Plugins(Command):
    def check_modules(self, node) -> None:
        """ recursive function to check all plugins have required modules """
        success: str = [] # list of installed modules
        for plugin in node.get_plugins():
            success.extend(plugin.check_requirements())
        for child in node.get_children():
            self.check_modules(child)
        for module in success:
            output(module)

    def get_description(self):
        return "Check required modules are installed"

    def get_actions(self):
        return ['p', 'plugins']

    def perform_action(self, *args):
        args[2].debug(f'Checking plugins modules', program='Plugins')
        self.check_modules(args[0])
        return args[0]
