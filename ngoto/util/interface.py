# script contains interface functions
from rich import print
from rich.console import Console
from rich.style import Style

__author__ = 'Harry Ludemann'
__version__ = '0.1.0'

console : Console = Console()
logo_style = Style(color="blue", blink=True, bold=True)
exit_style = Style(color="blue", blink=False, bold=True)
folder_style = Style(color="yellow", blink=False, bold=True)
plugin_style = Style(color="magenta", blink=False, bold=True)
input_style = Style(color="cyan", blink=False, bold=True)

def output(output, style=Style()):
    console.print(output, style=style, highlight=False)

def get_input(text=''):
    """ Input Method """
    return console.input('[blue][bold]' + text + '[/bold][/blue]')

def logo():
    output(f'''
 ██████   █████                    █████            
░░██████ ░░███                    ░░███             
 ░███░███ ░███   ███████  ██████  ███████    ██████ 
 ░███░░███░███  ███░░███ ███░░███░░░███░    ███░░███
 ░███ ░░██████ ░███ ░███░███ ░███  ░███    ░███ ░███
 ░███  ░░█████ ░███ ░███░███ ░███  ░███ ███░███ ░███
 █████  ░░█████░░███████░░██████   ░░█████ ░░██████ 
░░░░░    ░░░░░  ░░░░░███ ░░░░░░     ░░░░░   ░░░░░░  
                ███ ░███                            
               ░░██████                                           
''', logo_style)


def options(curr_node): # given Node in plugin and optionally workplace string
    logo()
    index = 1
    for folder in curr_node.get_children(): # print folders
        output(f'{index}. {folder.name}', style=folder_style)
        index += 1
    for plugin in curr_node.get_plugins(): # print plugins
        output(f'{index}. {plugin.name}', style=plugin_style)
        index += 1
    # output(f'\n{options}\n')

def commands():
    logo()
    output(f'''
[Basic]
o/options                   --  Returns osint options
c/commands                  --  Returns this list of commands
cls/clear                   --  Clear console
b/back                      --  Back out of plugin or folder
0/exit                      --  closes program

[Workplace]
wp/workshop create (NAME)   --  Creates (NAME) workplace
wp/workshop join (NAME)     --  Joins (NAME) workplace
wp/workshop delete (NAME)   --  Deletes (NAME) workplace
wp/workshop leave           --  Leave current workplace
''')


if __name__ == '__main__':
    output("test test")
