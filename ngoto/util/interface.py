# script contains interface functions

import sys

__author__ = 'Harry Ludemann'
__version__ = '0.1.0'

class ColourText:
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

    open_tags = ['[bold]', '[line]', '[cyan]', '[blue]', '[gren]', '[warn]', '[fail]', '[head]']
    close_tags = ['[/bold]', '[/line]', '[/cyan]', '[/blue]', '[/gren]', '[/warn]', '[/fail]', '[/head]']

    def color_text(self, output):
        final_string: str = ''
        curr_style: list = []
        curr_string: str = ''
        for char in output: 
            curr_string += char
            if len(curr_string) > 5: # if open tag
                for tag in self.open_tags:
                    if tag == (found_tag := curr_string[-6:]):
                        final_string += curr_string.replace(found_tag, self.colors[found_tag])
                        curr_style.append(tag)
                        curr_string = ''
            if len(curr_string) > 6: # if closing tag
                for tag in self.close_tags:
                    if tag == (found_tag := curr_string[-7:]):
                        final_string += curr_string.replace(found_tag, '')
                        final_string += self.colors['clear']
                        curr_style.pop()
                        for style in curr_style:
                            final_string += self.colors[style]
                        curr_string = ''

        final_string += curr_string
        return final_string

        

class Interface(ColourText):
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

    def output(self, output, color_safe=False):
        """ Print Method """
        if not color_safe:
            print(self.color_text(f"[bold]> {output}[/bold]"))
        else:
            cl = ColourText()
            print(cl.color_text(output) )

    def get_input(self, text='', position='', current_position=''):
        """ Input Method """
        user_input = str( input(self.color_text(f"[cyan][bold]{current_position}{position}[/cyan][/cyan][bold] > {str(text)}")))
        if user_input in ['exit']:  
            sys.exit()
        return user_input

    # UI Methods
    def logo(self):
        self.output(f'''[bold][head]
     _   _             _        
    | \ | |           | |       
    |  \| | __ _  ___ | |_ ___  
    | . ` |/ _` |/ _ \| __/ _ \ 
    | |\  | (_| | (_) | || (_) |
    |_| \_|\__, |\___/ \__\___/ 
            __/ |               
           |___/                   
        [/bold][/head]''', True)

    def options(self, curr_node, curr_workplace:str = 'N/A'): # given Node in plugin and optionally workplace string
        self.logo()
        index = 1
        options = self.color_text(f'[bold]\n0. Exit[/bold]')
        for folder in curr_node.get_children(): # print folders
            options += self.color_text(f'[bold]\n{index}. [cyan]{folder.name}[/cyan][/bold]')
            index += 1
        for plugin in curr_node.get_plugins(): # print plugins
            options += self.color_text(f'[bold]\n{index}. [cyan]{plugin.name}[/cyan][/bold]')
            index += 1
        self.output(f'\n[bold]Workplace: {curr_workplace}\n{options}\n[/bold]', True)

    def commands(self):
        self.logo()
        self.output(f'''
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
    ui = Interface()
    ui.output("[bold][gren]test test[/bold][/gren]", True)
