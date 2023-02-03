from ngoto import PluginBase, output, Table, Style  # used in this plugin
import subprocess


class Plugin(PluginBase):
    name = 'Wifi Passwords'
    version = 0.1
    description = 'Get stored wifi passwords'
    req_modules: list = []
    req_apis: list = []
    logger = None
    parameters: list = []
    os: list = ['Windows']

    table: Table = None  # used in this plugin
    title_style = Style(color="blue", blink=False, bold=True)
    border_style = Style(color="black", blink=False, bold=True)
    header_style = Style(color="black", blink=False, bold=True)

    def get_context(self) -> list:
        return {"data": subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles']).decode(
                'utf-8',
                errors="backslashreplace").split('\n')}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        logger.info(
            'Getting Wifi Passwords',
            program='Wifi Passwords')
        context = self.get_context()
        logger.info(
            'Successfully Got Wifi Passwords',
            program='Wifi Passwords')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(
            title="Ngoto Wifi Passwords Plugin",
            title_style=self.title_style,
            border_style=self.border_style)
        self.table.add_column("Profile Name", style=self.header_style)
        self.table.add_column("Password", style=self.header_style)
        for i in context['data']:
            if "All User Profile" not in i:
                continue
            profile = i.split(":")[1][1:-1]
            try:
                for line in subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
                        ).decode(
                            'utf-8',
                            errors="backslashreplace"
                                ).split('\n'):
                    if "Key Content" in line:
                        self.table.add_row(profile, line.split(":")[1])
                        break
            except subprocess.CalledProcessError:
                self.table.add_row(i, "ENCODING ERROR")
        output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return ''
