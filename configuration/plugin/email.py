import requests
from hazzah import Plugin
import logging

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