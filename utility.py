import imp

def reload_module(name):
    f = imp.find_module(name)
    m = imp.load_module(name, f[0], f[1], f[2])
    return m
    
# HTML Tags Stripper
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    html = html.replace('<br />', ' ')
    html = html.replace('<br/>', ' ')
    html = html.replace('<br>', ' ')
    
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# / HTML Tags Stripper