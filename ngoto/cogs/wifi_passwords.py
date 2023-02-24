from ngoto import plugin, output, Table, Style
from subprocess import check_output, CalledProcessError

title_style = Style(color="blue", blink=False, bold=True)
border_style = Style(color="black", blink=False, bold=True)
header_style = Style(color="black", blink=False, bold=True)


def get_info() -> list:
    return {"data": check_output(
        ['netsh', 'wlan', 'show', 'profiles'], shell=False).decode(
        'utf-8', errors="backslashreplace").split('\n')}


def print_info(context):
    table = Table(
        title="Ngoto Wifi Passwords Plugin",
        title_style=title_style,
        border_style=border_style)
    table.add_column("Profile Name", style=header_style)
    table.add_column("Password", style=header_style)
    for i in context['data']:
        if "All User Profile" not in i:
            continue
        profile = i.split(":")[1][1:-1]
        try:
            for line in check_output(
                ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                shell=False).decode(
                    'utf-8', errors="backslashreplace").split('\n'):
                if "Key Content" in line:
                    table.add_row(profile, line.split(":")[1])
                    break
        except CalledProcessError:
            table.add_row(i, "ENCODING ERROR")
    output(table)


class URL():
    """ Get saved wifi passwords """
    @classmethod
    @plugin(name='Wifi Passwords', desc='Get saved wifi passwords',
            folder='Passwords')
    def url(self, logger):
        logger.info(
            'Getting Wifi Passwords',
            program='Wifi Passwords')
        info = get_info()
        logger.info(
            'Successfully Got Wifi Passwords',
            program='Wifi Passwords')
        print_info(info)
        return True


def setup():
    return URL()
