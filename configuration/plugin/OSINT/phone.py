import requests
from ngoto import Plugin
import logging

class Plugin(Plugin):
    name = 'Phone'
    version = 0.1
    description = 'Search Phone'
    requirements = 'Num Verify API Key'

    def get_context(self, target_phone, NUM_VERIFY_API_KEY):
        r = requests.get(f"http://apilayer.net/api/validate?access_key={NUM_VERIFY_API_KEY}&number={target_phone } ").json()
        context = {
            'valid': r['valid'],
            'number': r['number'],
            'local_format': r['local_format'],
            'international_format': r['international_format'],
            'country_prefix': r['country_prefix'],
            'country_code': r['country_code'],
            'country_name': r['country_name'],
            'location': r['location'],
            'carrier': r['carrier'],
            'line_type': r['line_type'],
        }
        return context

    def main(self, hz):
        target = hz.interface.get_input("Target phone: ", '[Phone]', hz.curr_path)
        if target == 'back': return {}
        return self.get_info(target, hz.get_api('NUM_VERIFY_API_KEY'))

    def print_info(self, hz, context, tables):
        col_widths = [25, 50]
        col_names = ['Description', 'Value']
        col_values = []
        for item in context:
            if type(context[item]) != list:
                col_values.append( [str(item), str(context[item])] )
        hz.interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS phone (
        id integer PRIMARY KEY AUTOINCREMENT,
        valid text,
        number text,
        local_format text,
        international_format text,
        country_prefix text,
        country_code text,
        country_name text,
        location text,
        carrier text,
        line_type text );
        '''