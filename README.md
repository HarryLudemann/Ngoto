# Ngoto
[![version-1.3](https://img.shields.io/badge/version-0.0.20-blue)](https://github.com/Datalux/Osintgram/releases/tag/1.3)
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](https://img.shields.io/badge/license-GPLv3-blue)
[![Python3](https://img.shields.io/badge/language-Python3-blue)](https://img.shields.io/badge/language-Python3-red)
[![](https://img.shields.io/badge/Built%20with-❤-blue.svg?style=flat-square)]()
[![](https://github.com/harryludemann/ngoto/workflows/pytests/badge.svg)]()
[![platforms](https://img.shields.io/badge/platform-windows%20%7C%20linux-blue)](https://github.com/loseys/Oblivion/)

# Warning :warning:

<p align="center"><b>This tool is solely for educational purposes. Developer will not be reponsible for any misuse of the tool</b></p>    
    

# Features:
* Currently 5 inbuilt plugins (Email, Phone, IP, URL, Google)  
* Easily create/add plugins.
* Use as command line tool or as module.
* Easily create/store received data into workplaces/databases

# Command line tool commands:
    o/options                   --  Returns osint options
    c/commands                  --  Returns this list of commands
    cls/clear                   --  Clear console
    back                        --  back out of plugin
    0/exit                      --  closes program

    wp/workshop create (NAME)   --  Creates (NAME) workplace
    wp/workshop join (NAME)     --  Joins (NAME) workplace
    wp/workshop delete (NAME)   --  Deletes (NAME) workplace
    wp/workshop leave           --  Leave current workplace
# Setup:
## Using as Command line tool:
#### 1. Clone Repo:
```
git clone https://github.com/HarryLudemann/Hazzah-OSINT
```
#### 2. Optionally add API keys
Within the configuration folder contains a config.json as shown below, fill in API key if you require that function.
* **NUM_VERIFY_API_KEY**: for phone plugin
* **IP_QUALITY_API_KEY**: for ip plugin
* **EMAIL_VERIFICATION_API_KEY**: for email plugin
```json
{
    "API": {
        "NUM_VERIFY_API_KEY": "",
        "IP_QUALITY_API_KEY": "",
        "EMAIL_VERIFICATION_API_KEY": ""
        },
    "PATHS": {
        "WORKPLACE": "configuration/workplace/",
        "PLUGIN": "configuration/plugin/"
        }
}

```
#### 3. Run
Run the main.py script, which will bring you to the following:
```
     _   _             _
    | \ | |           | |
    |  \| | __ _  ___ | |_ ___
    | . ` |/ _` |/ _ \| __/ _ \
    | |\  | (_| | (_) | || (_) |
    |_| \_|\__, |\___/ \__\___/
            __/ |
           |___/

Workplace: None

0. Exit
1. Phone
2. Email
3. IP
4. URL
5. Google Dorks
```

## Using Ngoto as module:
#### 1. Install PIP Module:
```
pip install ngoto
```
#### 2. Import and Initialize:
```python
from ngoto import Module # import the osint class from the hazzah module

# initialize the osint class and set my desired functions API's keys (Below are fake API keys)
hz = Module()
```
#### 3. Example Calling Functions:
```python
print( hz.get_plugin_context('IP', ['142.250.71.78', 'ai6aofcKK1zF87XUMPzoN1s8Nx07r5Rr']) )
```
##### Result:
```
{
   "query":"142.250.71.78",
   "status":"success",
   "country":"Australia",
   "countryCode":"AU",
   "region":"NSW",
   "regionName":"New South Wales",
   "city":"Sydney",
   "zip":"1001",
   "lat":-33.8688,
   "lon":151.209,
   "timezone":"Australia/Sydney",
   "isp":"Google LLC",
   "org":"Google LLC",
   "as":"AS15169 Google LLC",
   "success":true,
   "message":"Success",
   "fraud_score":75,
   "is_crawler":false,
   "mobile":false,
   "host":"syd15s17-in-f14.1e100.net",
   "proxy":true,
   "vpn":true,
   "tor":false,
   "active_vpn":false,
   "active_tor":false,
   "recent_abuse":false,
   "bot_status":false
}
```

## Create Plugin:
### Import Plugin Module:
Install ngoto module.
```
pip install ngoto
```
Import Plugin from ngoto, create a class named Plugin inheriting from Plugin class. eg.
```python
from ngoto import Plugin
class Plugin(Plugin):
    name = ''
``` 

     
### Functions:
There are 5 functions to complete:  
* get_info - given any required args, returns dict 
* main - given hazzahclt object contains api keys, returns dicts   
* print_info - given context, prints information
* create_table - returns string of sql query to match context   
* get_context - given list of args, returns dict

### Example Plugin:
```python
# Script returns ip of given url
import socket
from ngoto import Plugin

class Plugin(Plugin):
    name = 'URL'
    version = 0.1
    description = 'Search URL'

    # Returns dict of acquired information, given desired information
    def get_context(self, target_url):
        context = {
            'ip': socket.gethostbyname(target_url)
        }
        return context

    # main function to handle input, then calls and return get_context method
    def main(self, hz):
        target = hz.interface.get_input("Target URL: ", '[URL]', hz.curr_path)
        if target in ['back', 'b']: return {}
        return self.get_context(target)

    # given context of information prints information
    def print_info(self, hz, context, tables):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [item, context[item]] )
        hz.interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    # holds sqlite3 create table query to store information
    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS url (
        id integer PRIMARY KEY AUTOINCREMENT,
        ip text );
        '''
```
