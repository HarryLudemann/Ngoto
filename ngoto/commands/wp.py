# contains function to handle workplace commands
from ngoto.util.command import Command  
from ngoto.util import interface, Workplace
from ngoto import constants as const
import os
from os.path import exists

class Wp(Command):
    workplace: Workplace = None

    # Workplace command method
    def workplace_command(self, options: list) -> None:
        """ 
        determines requested workplace option, given list of options 
        if create, create workplace named option[2]
        elif join, join workplace named option[2] 
        elif setup, loop over all plugins creating the suggested table
        elif delete, deletes option[2] workplace
        elif leave, leaves current workplace
        else prints 'no such command
        """
        if len(options) >= 2:
            if options[1] == 'create':  # create wp
                self.workplace = Workplace(const.workplace_path, options[2])
                self.workplace.create_workplace(options[2])
                interface.output(f"Successfully created {options[2]} workplace")
            elif options[1] == 'join':
                self.workplace = Workplace(const.workplace_path, options[2])
                self.workplace.run_command(options[2], '')  # test connection to db
                interface.output(f"Successfully joined {options[2]} workplace")
            elif options[1] == 'setup':
                query = ''
                for plugin in self.plugins:
                    plugin = plugin()
                    query += '\n' + plugin.create_table()
                self.workplace.run_script(self.workplace.name, query)  # test connection to db
                interface.output(f"Successfully setup {self.workplace.name} workplace tables")
            elif options[1] == 'delete':
                file_exists = exists(f"{const.workplace_path}{options[2]}.sqlite")
                if file_exists:
                    os.remove(f"{const.workplace_path}{options[2]}.sqlite")
                    self.workplace = None
                    # logging.info(f"Deleted workplace {options[2]}")
                    interface.output(f"Successfully deleted {options[2]} workplace")
                # else:
                    # logging.warning("Workplace already does not exist")
            elif options[1] == 'leave':  # create wp
                self.workplace = None
                interface.output(f"Successfully left workplace")
        # else:
        #     logging.warning("No such command")

    def getDescription(self):
        return "Command to handle workplace commands"

    def getActions(self):
        return ['wp', 'workplace']

    def performAction(self, *args):
        self.workplace_command(args[1])
        return args[0]
