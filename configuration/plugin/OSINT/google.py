from ngoto import Plugin
import logging
try:
    from googlesearch import search
except ImportError:
    logging.warning("No module named 'google' found, cannot use google dorking/search")

class Plugin(Plugin):
    name = 'Google'
    version = 0.1
    description = 'Google Search'
    requirements = 'googlesearch python module'

    def get_context(self, query, types, parameter, max_results=10):
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
        type = hz.interface.get_input("Search f:file or w:website: ", '[Google]', hz.curr_path)
        if type == 'back': return {}
        target = hz.interface.get_input("Enter query: ", '[Google]', hz.curr_path)
        if target == 'back': return {}
        if type == 'f':
            files = hz.interface.get_input("Enter file types eg. pdf xlsx docx: ", '[Google]', hz.curr_path).split()
            if files == 'back': return {}
            maxcount = hz.interface.get_input("Optionally enter max results: ", '[Google]', hz.curr_path)
            if maxcount == 'back': return {}
            return self.get_info(target, files, 'filetype:', int(maxcount))
        elif type == 'w':
            websites = hz.interface.get_input("Enter websites eg facebook.com twitter.com: ", '[Google]', hz.curr_path).split()
            if websites == 'back': return {}
            maxcount = hz.interface.get_input("Optionally enter max results: ", '[Google]', hz.curr_path)
            if maxcount == 'back': return {}
            return self.get_info(target, websites, 'site:', int(maxcount))

    def print_info(self, hz, context, tables):
        col_names = ['URL']
        col_values = []
        longest_url = 0
        for item in context['urls']:
            col_values.append( [item] )
            if len(item) > longest_url:
                longest_url = len(item)
        col_widths = [longest_url]
        hz.interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS google (
        id integer PRIMARY KEY AUTOINCREMENT,
        url text );
        '''