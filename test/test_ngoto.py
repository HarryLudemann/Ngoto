import requests

def test_download():
    """ Test method to test downloading of plugins from github dir """
    modules = []
    url = 'https://github.com/HarryLudemann/Hazzah-OSINT/tree/main/configuration/plugin'
    open_tag = '<span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title="'
    r = requests.get(url)
    for line in r.text.split('\n'):
        if open_tag in line:
            modules.append(line.replace(open_tag, '').split('"', 1)[0].strip())

    assert len(modules) >= 1 # currently 5 plugins
