# Ngoto
[![](https://github.com/HarryLudemann/Ngoto/workflows/pytests/badge.svg)]()
[![version-1.3](https://img.shields.io/badge/version-0.0.20-blue)](https://github.com/Datalux/Osintgram/releases/tag/1.3)
[![GPLv3](https://img.shields.io/badge/license-MIT-blue)](https://img.shields.io/badge/license-GPLv3-blue)
[![Python3](https://img.shields.io/badge/language-Python3-blue)](https://img.shields.io/badge/language-Python3-red)
[![](https://img.shields.io/badge/Built%20with-❤-blue.svg?style=flat-square)]()
[![platforms](https://img.shields.io/badge/platform-windows%20%7C%20linux-blue)](https://github.com/loseys/Oblivion/)

# Warning :warning:

<p align="center"><b>This tool is solely for educational purposes. Developer will not be responsible for any misuse of the tool</b></p>    
    
# Setup:
## Using as Command line tool:
#### 1. Clone Repo:
```
git clone https://github.com/HarryLudemann/Ngoto
```

#### 2. Install Required Modules:
Move into downloaded Ngoto folder then run:
```
pip install -r requirements.txt
```
or
```
pip3 install -r requirements.txt
```

#### 4. Run
Run 'python/python3 main.py' script:
```
python main.py
```
or
```
python3 main.py
```
Which will bring you to the following:

![](.github/LaunchScreen.png)

# Examples:

## Plugin:
```python
from ngoto.util import Plugin, interface
from rich.table import Table # used in this plugin

class Plugin(Plugin):
    name = 'IP'
    version = 0.1
    description = 'Get IP'
    req_modules: list = []
    req_apis: list = []
    parameters: list = []
    os: list = ['Linux', 'Windows', 'MacOS']

    # Returns dict of acquired information, given desired information
    def get_context(self, target_url):
        return {"ip": "192.181.1.1"}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        target = interface.get_input("[URL] Target URL eg. thaturl.com: ")
        context = self.get_context(target)
        return context

    # given context of information prints information
    def print_info(self, context):
        table = Table(title="Ngoto URL Plugin")   
        self.table.add_column("Description", justify="center")
        self.table.add_column("Value", justify="center")
        table.add_row("IP", context['ip'])
        interface.output(self.table)
```
## Command:
```python
# contains function to clear screen
from ngoto.util.command import Command
from ngoto.util.clear import clear_screen

class Clear(Command):

    def get_description(self):
        return "Clear console"

    def get_actions(self):
        return ["cls", "clear"]

    def perform_action(self, *args):
        clear_screen()
        args[2].debug(f'Clearing screen', program='Clear')
        return args[0]
```

## Task:
```python
from ngoto.util.task import Task
from notifier import notify
import psutil
import os

class PCUsage(Task):
    id = "PCUsage"
    delay = 60 # show every 60 seconds
    description = "Notifcation of Computer Usage"
    last_output = ""
    iteration = 0 
    active = True

    def __call__(self) -> bool:
        """ Returns list of first item return information and second of task id"""
        ram_usage = psutil.virtual_memory()[2]
        cpu_usage = psutil.cpu_percent()
        self.last_output = f"RAM used: {ram_usage}\nCPU used: {cpu_usage}"
        self.iteration += 1
        notify("Computer Usage", f"RAM used: {ram_usage}\nCPU used: {cpu_usage}")
        return [f"RAM used: {ram_usage}\nCPU used: {cpu_usage}", self.id]
```
