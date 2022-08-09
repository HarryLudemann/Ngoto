# script contains interface functions
from rich.console import Console
from rich.table import Table # used in this plugin
from rich.style import Style # used in this plugin
from ngoto.util.clear import clear_screen

__author__ = 'Harry Ludemann'
__version__ = '0.1.0'

console : Console = Console()
logo_style = Style(color="blue", blink=False, bold=True)
exit_style = Style(color="blue", blink=False, bold=True)
folder_style = Style(color="yellow", blink=False, bold=True)
plugin_style = Style(color="magenta", blink=False, bold=True)
input_style = Style(color="cyan", blink=False, bold=True)
output_style = Style(color="blue", blink=False, bold=True)

title_style = Style(color="blue", blink=False, bold=True) # used in this plugin
border_style = Style(color="black", blink=False, bold=True) # used in this plugin
header_style = Style(color="black", blink=False, bold=True) # used in this plugin

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

def commands(commands: list):
    table = Table(title="Ngoto Commands", title_style=title_style, border_style=border_style)   
    table.add_column("Commands", style=output_style)
    table.add_column("Description", style=output_style)
    for command in commands:
        actions = str(command.get_actions()).replace("'", "").replace("[", "").replace("]", "")
        table.add_row(actions, command.get_description())
    table.add_row("t/task d {task_id}/all", "Disable a task")
    table.add_row("t/task e {task_id}/all", "Enable a task")
    table.add_row("t/task delay {task_id}/all {delay}", "Set a task delay")
    output(table)

def tasks(tasks: list):
    table = Table(title="Ngoto Tasks", title_style=title_style, border_style=border_style)   
    table.add_column("ID", style=output_style)
    table.add_column("Delay", style=output_style)
    table.add_column("Description", style=output_style)
    table.add_column("Last Output", style=output_style)
    table.add_column("Ran", style=output_style)
    table.add_column("Enabled", style=output_style)

    for task in tasks:
        table.add_row(task.id, str(task.delay), task.description, task.last_output, str(task.iteration), str(task.active))
    output(table)




