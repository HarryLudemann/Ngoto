# script contains interface functions

import sys

__author__ = 'Harry Ludemann'
__version__ = '0.1.0'

open_tags = ['[bold]', '[line]', '[cyan]', '[blue]', '[gren]', '[warn]', '[fail]', '[head]']
close_tags = ['[/bold]', '[/line]', '[/cyan]', '[/blue]', '[/gren]', '[/warn]', '[/fail]', '[/head]']
colors = {
        '[head]' : '\033[95m',
        '[blue]' : '\033[94m',
        '[cyan]' : '\033[96m',
        '[gren]' : '\033[92m',
        '[warn]' : '\033[93m',
        '[fail]' : '\033[91m',
        'clear' : '\033[0m',
        '[bold]' : '\033[1m',
        '[line]' : '\033[4m'
        }


class bcolors:
    """ Stores colours """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_text(output):
    final_string: str = ''
    curr_style: list = []
    curr_string: str = ''
    for char in output: 
        curr_string += char
        if len(curr_string) > 5: # if open tag
            for tag in open_tags:
                if tag == (found_tag := curr_string[-6:]):
                    final_string += curr_string.replace(found_tag, colors[found_tag])
                    curr_style.append(tag)
                    curr_string = ''
        if len(curr_string) > 6: # if closing tag
            for tag in close_tags:
                if tag == (found_tag := curr_string[-7:]):
                    final_string += curr_string.replace(found_tag, '')
                    final_string += colors['clear']
                    curr_style.pop()
                    for style in curr_style:
                        final_string += colors[style]
                    curr_string = ''

    final_string += curr_string
    return final_string


def output(output, color_safe=False):
    """ Print Method """
    if not color_safe:
        print(color_text(f"[bold]> {output}[/bold]"))
    else:
        print(color_text(output) )


def get_input(text='', position='', current_position=''):
    """ Input Method """
    user_input = str( input(color_text(f"[cyan][bold]{current_position}{position}[/cyan][/cyan][bold] > {str(text)}")))
    if user_input in ['exit']:  
        sys.exit()
    return user_input


# UI Methods
def logo():
    output(f'''[bold][head]
 _   _             _        
| \ | |           | |       
|  \| | __ _  ___ | |_ ___  
| . ` |/ _` |/ _ \| __/ _ \ 
| |\  | (_| | (_) | || (_) |
|_| \_|\__, |\___/ \__\___/ 
        __/ |               
        |___/                   
    [/bold][/head]''', True)


def options(curr_node): # given Node in plugin and optionally workplace string
    logo()
    index = 1
    options = color_text(f'[bold]\n0. Exit[/bold]')
    for folder in curr_node.get_children(): # print folders
        options += color_text(f'[bold]\n{index}. [cyan]{folder.name}[/cyan][/bold]')
        index += 1
    for plugin in curr_node.get_plugins(): # print plugins
        options += color_text(f'[bold]\n{index}. [cyan]{plugin.name}[/cyan][/bold]')
        index += 1
    output(f'\n[bold]{options}\n[/bold]', True)

def divider():
    print(bcolors.BOLD + '-'*50 + bcolors.ENDC)

def short_log(logs: str) -> None:
    """ print styled logs """
    print(logs)


def commands():
    logo()
    output(f'''
[head][Basic][/head][bold]
o/options                   --  Returns osint options
c/commands                  --  Returns this list of commands
cls/clear                   --  Clear console
b/back                      --  Back out of plugin or folder
0/exit                      --  closes program

[head][Workplace][/head]
wp/workshop create (NAME)   --  Creates (NAME) workplace
wp/workshop join (NAME)     --  Joins (NAME) workplace
wp/workshop delete (NAME)   --  Deletes (NAME) workplace
wp/workshop leave           --  Leave current workplace
    [/bold]''', True)


if __name__ == '__main__':
    output("[bold][gren]test test[/bold][/gren]", True)
