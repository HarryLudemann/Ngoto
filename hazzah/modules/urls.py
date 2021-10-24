import socket


def get_urls_info(target_url):
    """ Given target URL returns urls ip
        returns dict
     """
    context = {
        'ip': socket.gethostbyname(target_url)
    }
    return context


def get_url_scan(target_url, VIRUS_TOTAL_API_KEY):
    """ Scans url for malware 
        return dict
    """
    context = {}
    import requests
    # Dashboard: Scanning URL
    api_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = dict(apikey=VIRUS_TOTAL_API_KEY, url=target_url)
    response = requests.post(api_url, data=params)
    # Dashboard: Getting Report
    api_url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = dict(apikey=VIRUS_TOTAL_API_KEY, resource=target_url, scan=0)
    response = requests.get(api_url, params=params)
    while response.status_code == 0: # continously check until report is made
        response = requests.get(api_url, params=params)
    if response.status_code == 200:
        result=response.json()
        print('Failed Tests: ', result['positives'], '\n')
        failed = []
        for key in result['scans']:
            if result['scans'][key]['detected']:
                failed.append({'Service': key, 'Failure': result['scans'][key]['result']})
        context['failed'] = failed
        context['ran'] = True
        context['target'] = target_url
    return context