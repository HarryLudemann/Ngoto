# Hazzah-OSINT 0.0.14
# Warning :warning:

<p align="center"><b>This tool is solely for educational purposes. Developer will not be reponsible for any misuse of the tool</b></p>    
    

# Features:
* Currently 5 inbuilt plugins (Email, Phone, IP, URL, Google)  
* Easily create/add plugins.
* Use as command line tool or as module.
* Easily create/store received data into workplaces/databases

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
    "EMAIL_VERIFICATION_API_KEY": "",
    "NUM_VERIFY_API_KEY": "",
    "IP_QUALITY_API_KEY": ""
}
```
#### 3. Run
Run the main.py script, which will bring you to the following:
```
 _   _                    _
| | | |                  | |
| |_| | __ _ __________ _| |__        
|  _  |/ _` |_  /_  / _` | '_ \       
| | | | (_| |/ / / / (_| | | | |      
\_| |_/\__,_/___/___\__,_|_| |_|      

Workplace: None

0. Exit
1. Phone
2. Email
3. IP
4. URL
5. Google Dorks
```

## Using Hazzah-OSINT as module:
#### 1. Install PIP Module:
```
pip install hazzah-osint
```
#### 2. Import and Initialize:
```python
from hazzah import osint # import the osint class from the hazzah module

# initialize the osint class and set my desired functions API's keys (Below are fake API keys)
hz = hazzah.Hazzah()
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
Install hazzah-osint module.
```
pip install hazzah-osint
```
Import Plugin from hazzah, create a class named Plugin inheriting from Plugin class. eg.
```python
from hazzah import Plugin
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
import requests
from hazzah import Plugin

class Plugin(Plugin):
    name = 'Email'

    def get_info(self, target_email, api_key):
        r = requests.get(f'https://emailverification.whoisxmlapi.com/api/v1?apiKey={api_key}&emailAddress=' + target_email ).json()
        if 'emailAddress' in r:   
            context = {
                'emailAddress': r['emailAddress'],
                'formatCheck': r['formatCheck'],
                'smtpCheck': r['smtpCheck'],
                'dnsCheck': r['dnsCheck'],
                'freeCheck': r['freeCheck'],
                'disposableCheck': r['disposableCheck'],
                'catchAllCheck': r['catchAllCheck'],
                'mxRecords': r['mxRecords'],
                'auditCreatedDate': r['audit']['auditCreatedDate'],
                'auditUpdatedDate': r['audit']['auditUpdatedDate'],
            }
            return context
        else:
            logging.error("Get email info failed api call")
            return {}

    def main(self, hz):
        target = hz.interface.get_input("Target email: ", '[Email]', hz.current_pos)
        if target == 'back': return {}
        return self.get_info(target, hz.get_api('EMAIL_VERIFICATION_API_KEY'))

    def print_info(self, hz, context):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [str(item), str(context[item])] )

        hz.interface.output( '\n' + self.Tables().get_table(col_names, col_widths, col_values) )

    def get_context(self, args):
        return self.get_info(args[0], args[1])

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS email (
        id integer PRIMARY KEY AUTOINCREMENT,
        emailAddress text,
        formatCheck text,
        smtpCheck text,
        dnsCheck text,
        freeCheck text,
        disposableCheck text,
        catchAllCheck text,
        mxRecords text,db
        auditCreatedDate text,
        auditUpdatedDate text);
        '''
```
