import googlesearch
from hazzah import osint
import logging
try:
    from googlesearch import search
except ImportError:
    logging.warning("No module named 'google' found, cannot use google dorking/search")

class Plugin(osint.Plugins):
    name = 'Google'

    def google_search(self, query, types, parameter, max_results=10):
        """ given query, list of websites eg ['twitter.com', 'facebook.com'] or ['pdf', 'xlsx] and parameter eg filetype: or site:
        returns list of url's """
        if not types: # if types is empty
            logging.error('types var must contain list of requested file types')
            return []
        else:
            formatted_query = f"\"{query}\" {parameter}{types[0]}"
            for type in types[1:]: # iterate skipping first item
                formatted_query += f" OR {parameter}{type}"
            return { 'urls': search(formatted_query, num_results=max_results, lang="en" ) }

    def main(self, hz):
        type = self.get_input("Search f:file or w:website: ", '[Google]')
        if type == 'back': return {}
        target = self.get_input("Enter query: ", '[Google]')
        if target == 'back': return {}
        if type == 'f':
            files = self.get_input("Enter file types eg. pdf xlsx docx: ", '[Google]').split()
            if files == 'back': return {}
            maxcount = self.get_input("Optionally enter max results: ", '[Google]')
            if maxcount == 'back': return {}
            return self.google_search(target, files, 'filetype:', int(maxcount))
        elif type == 'w':
            websites = self.get_input("Enter websites eg facebook.com twitter.com: ", '[Google]').split()
            if websites == 'back': return {}
            maxcount = self.get_input("Optionally enter max results: ", '[Google]')
            if maxcount == 'back': return {}
            return self.google_search(target, websites, 'site:', int(maxcount))

    def print_info(self, context):
        col_names = ['URL']
        col_values = []
        longest_url = 0
        for item in context['urls']:
            col_values.append( [item] )
            if len(item) > longest_url:
                longest_url = len(item)
        col_widths = [longest_url]
        print( '\n' + self.Tables().get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS google (
        id integer PRIMARY KEY AUTOINCREMENT,
        url text );
        '''
    
    




