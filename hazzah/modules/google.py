import logging
try:
    from googlesearch import search
except ImportError:
    logging.error("No module named 'google' found")

def google_search(query, types, parameter, max_results=10):
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