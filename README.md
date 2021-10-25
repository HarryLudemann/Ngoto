# Hazzah-OSINT 0.0.3

Lightweight python OSINT tool available as module and command line tool to gather information on a target. Created to simplify a django dashboard, currently a working work in progress.

## Setup:
## Using as Command line tool:
Ensure you have pip install hazzah-osint
#### 1. Install PIP Module:
```
pip install hazzah-osint
```
#### 2. Folder Setup
Download the hazzahclt.py script from the main github directory and place into folder, in the same folder create a config.json file eg. (You only need the API's you require, leave blank if not using)
```json
{
    "TOTAL_VIRUS_API_KEY": "",
    "NUM_VERIFY_API_KEY": "",
    "IP_QUALITY_API_KEY": ""
}
```
#### 3. Run
Run the hazzahclt.py script, which will bring you to the following:
```
 _   _                    _
| | | |                  | |
| |_| | __ _ __________ _| |__        
|  _  |/ _` |_  /_  / _` | '_ \       
| | | | (_| |/ / / / (_| | | | |      
\_| |_/\__,_/___/___\__,_|_| |_|      

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
hz = osint() 
hz.set_ip_quality_api('ai6aofcKK1zF87XUMPzoN1s8Nx07r5Rr')
hz.set_num_verify_api('I2FSZJOB1cTUYclTMLgZdjTjd1wgtyGZ')
hz.set_virus_total_api('9fv3dFjGRPJwrS39Q8eK2YI6ClFnKOHIT3BVwIrbl0yAGpAmoEVerr8TCB5agAGX')
```
#### 3. Example Calling Functions:
```python
context = hz.get_ip_info('172.217.1.206')
for name in context:
    print(f'{name}: {context[name]}')
```
##### Result:
```
query: 172.217.1.206
status: success
country: United States
countryCode: US
region: DC
regionName: District of Columbia
city: Washington
zip: 20068
lat: 38.9072
lon: -77.0369
timezone: America/New_York
isp: Google LLC
org: Google LLC
as: AS15169 Google LLC
success: True
message: Success
fraud_score: 100
is_crawler: False
mobile: False
host: iad66s03-in-f14.1e100.net
proxy: True
vpn: True
tor: False
active_vpn: False
active_tor: False
recent_abuse: True
bot_status: True
```

## API Keys:
<p>Certain function requires API keys, check the list below for the functions and API keys you require.<p>
<table >
  <tr>
    <th>Function</th>
    <th>Definition</th>
    <th>File</th>
    <th>Req. API Key</th>
  </tr>
  <tr>
    <td>get_email_info(target_email)</td>
    <td>Returns dictionary of attained email information</td>
    <td>modules/emails.py</td>
    <td>False</td>
  </tr>
  <tr>
    <td>get_file_scan(target_name, target_files, target_string)</td>
    <td>Returns dictionary of anti virus that detected malware</td>
    <td>modules/files.py</td>
    <td>True - Virus Total</td>
  </tr>
  <tr>
    <td>get_ip_info(target_ip)</td>
    <td>Returns dictionary of attained ip information</td>
    <td>modules/urls.py</td>
    <td>True - IP Quality</td>
  </tr>
  <tr>
    <td>get_phone_info(target_phone)</td>
    <td>Returns dictionary of attained phone number information</td>
    <td>modules/phones.py</td>
    <td>True - Num Verify</td>
  </tr>
  <tr>
    <td>get_urls_info(target_url)</td>
    <td>Returns dictionary of the urls ip address</td>
    <td>modules/urls.py</td>
    <td>False</td>
  </tr>
  <tr>
    <td>get_url_scan(target_url)</td>
    <td>Returns dictionary of anti-malware that detected malware</td>
    <td>modules/urls.py</td>
    <td>True - Virus Total</td>
  </tr>
  <tr>
    <td>get_document_search(query)</td>
    <td>Returns dictionary of url search results</td>
    <td>modules/main.py</td>
    <td>False</td>
  </tr>
  <tr>
    <td>get_website_search(query)</td>
    <td>Returns dictionary of url search results</td>
    <td>modules/main.py</td>
    <td>False</td>
  </tr>
  <tr>
    <td>google_search(query, types, parameter, maxcount)</td>
    <td>Returns dictionary of url search results, given query, list of websites eg ['twitter.com', 'facebook.com'] or ['pdf', 'xlsx] and parameter eg filetype: or site:. optionally maxcount (by default set to 10)</td>
    <td>modules/google.py</td>
    <td>False</td>
  </tr>
  <tr>
    <td>set_ip_quality_api(api_key)</td>
    <td>Sets the IP quality api key</td>
    <td>main.py</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>set_num_verify_api(api_key)</td>
    <td>Sets the Num Verify api key</td>
    <td>main.py</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>set_virus_total_api(api_key)</td>
    <td>Sets the VirusTotal api key</td>
    <td>main.py</td>
    <td>N/A</td>
  </tr>
</table>

# Warning :warning:

<p align="center"><b>This tool is solely for educational purposes. Developer will not be reponsible for any misuse of the tool</b></p>