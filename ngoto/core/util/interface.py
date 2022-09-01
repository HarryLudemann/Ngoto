# script contains interface functions
from rich.console import Console
from rich.table import Table  # used in this plugin
from rich.style import Style  # used in this plugin

console: Console = Console()
logo_style = Style(color="blue", blink=False, bold=True)
exit_style = Style(color="blue", blink=False, bold=True)
folder_style = Style(color="yellow", blink=False, bold=True)
plugin_style = Style(color="magenta", blink=False, bold=True)
input_style = Style(color="cyan", blink=False, bold=True)
output_style = Style(color="blue", blink=False, bold=True)
greyed_out_style = Style(color="grey30", blink=False, bold=False)

title_style = Style(color="blue", blink=False, bold=True)
border_style = Style(color="black", blink=False, bold=True)
header_style = Style(color="black", blink=False, bold=True)


def output(output, style=Style()):
    console.print(output, style=style, highlight=False)


def get_input(text=''):
    """ Input Method """
    return console.input('[blue][bold]' + text + '[/bold][/blue]')


def logo():
    output('''
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


def show_options(curr_node):  # given Node in plugin
    logo()
    index = 1
    for folder in curr_node.get_children():  # print folders
        output(f'{index}. {folder.name}', style=folder_style)
        index += 1
    for plugin in curr_node.get_plugins():  # print plugins
        output(f'{index}. {plugin.name}', style=plugin_style)
        index += 1


def show_commands(commands: list):
    table = Table(
        title="Ngoto Commands",
        title_style=title_style,
        border_style=border_style)
    table.add_column("Commands", style=output_style)
    table.add_column("Description", style=output_style)
    for command in commands:
        actions = str(
            command.get_actions()
            ).replace("'", "").replace("[", "").replace("]", "")
        table.add_row(actions, command.get_description())
    table.add_row("t/task d {task_id}/all", "Disable a task")
    table.add_row("t/task e {task_id}/all", "Enable a task")
    table.add_row("t/task delay {task_id}/all {delay}", "Set a task delay")
    output(table)


def show_tasks(tasks: list, thisOS: str):
    table = Table(
        title="Ngoto Tasks",
        title_style=title_style,
        border_style=border_style)
    table.add_column("ID", style=output_style)
    table.add_column("Delay", style=output_style)
    table.add_column("Description", style=output_style)
    table.add_column("Last Output", style=output_style)
    table.add_column("Ran", style=output_style)
    table.add_column("Enabled", style=output_style)
    table.add_column("OS", style=output_style)

    for task in tasks:
        if thisOS in task.os:
            table.add_row(
                task.id,
                str(task.delay),
                task.description,
                task.last_output,
                str(task.iteration),
                str(task.active),
                str(task.os))
        else:
            table.add_row(
                task.id,
                str(task.delay),
                task.description,
                task.last_output,
                str(task.iteration),
                "False",
                str(task.os),
                style=greyed_out_style)
    output(table)
