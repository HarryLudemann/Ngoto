import hashlib
import requests

def get_file_scan(target_name, target_files, target_string, VIRUS_TOTAL_API_KEY):
    print("Dashboard: Scanning File")
    context = {}
    # upload file
    params = dict(apikey=VIRUS_TOTAL_API_KEY)
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=target_files, params=params)
    # Get Report
    sha256_hash = hashlib.sha256(target_string).hexdigest()         # create sha256 hash of file
    params = dict(apikey=VIRUS_TOTAL_API_KEY, resource=sha256_hash)
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    while response.status_code == 0: # continuously check until report is made
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    if response.status_code == 200:
        result=response.json()
        failed = [] # list of dicts of anti malware that are reporting malware
        for key in result['scans']:
            if result['scans'][key]['detected']:
                failed.append({'Service': key, 'Failure': result['scans'][key]['result']})
        context['failed'] = failed
        context['ran'] = True
        context['target'] = target_name
    return context