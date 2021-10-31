import requests

def get_ip_info(target_ip, IP_QUALITY_API_KEY):
    r = requests.get('http://ip-api.com/json/' + target_ip ).json()
    response = requests.get(f"https://ipqualityscore.com/api/json/ip/{IP_QUALITY_API_KEY}/{target_ip}").json()
    context = {
        'query':r['query'],
        'status':r['status'],
        'country':r['country'],
        'countryCode':r['countryCode'],
        'region':r['region'],
        'regionName':r['regionName'],
        'city':r['city'],
        'zip':r['zip'],
        'lat':r['lat'],
        'lon':r['lon'],
        'timezone':r['timezone'],
        'isp':r['isp'],
        'org':r['org'],
        'as':r['as'],

        'success': response['success'],
        'message': response['message'],
        'fraud_score': response['fraud_score'],
        'is_crawler': response['is_crawler'],
        'mobile': response['mobile'],
        'host': response['host'],
        'proxy': response['proxy'],
        'vpn': response['vpn'],
        'tor': response['tor'],
        'active_vpn': response['active_vpn'],
        'active_tor': response['active_tor'],
        'recent_abuse': response['recent_abuse'],
        'bot_status': response['bot_status']
    }
    return context