import requests
from hazzah import osint
import logging

class Plugin(osint.Plugins):
    name = 'IP'

    def get_ip_info(self, target_ip, IP_QUALITY_API_KEY):
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

    def main(self, hz):
        target = self.get_input("Target IP: ", '[IP]')
        if target == 'back': return {}
        return self.get_ip_info(target, hz.IP_QUALITY_API_KEY)

    def print_info(self, context):
        col_widths = [20, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [str(item), str(context[item])] )
        print( '\n' + self.Tables().get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS ip (
        id integer PRIMARY KEY AUTOINCREMENT,
        query text,
        status text,
        country text,
        countryCode text,
        region text,
        regionName text,
        city text,
        zip text,
        lat text,
        lon text,
        timezone text,
        isp text,
        org text,
        as_ text,
        success text,
        message text,
        fraud_score text,
        is_crawler text,
        mobile text,
        host text,
        proxy text,
        vpn text,
        tor text,
        active_vpn text,
        active_tor text,
        recent_abuse text,
        bot_status text
        );
        '''
    
    




