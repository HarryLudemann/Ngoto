# contains function to exit program
from ngoto import CommandBase, output
import sys


class Exit(CommandBase):
    def get_description(self):
        return "Exit program"

    def get_actions(self):
        return ["q", "exit", "0", "&"]

    def perform_action(self, pos, _, logger):
        output("Exiting...")
        logger.save_log()
        logger.info("Exiting ngoto")
        logger.debug('Exiting ngoto', program='Exit')
        sys.exit()
        return pos
