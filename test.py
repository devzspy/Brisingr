from lib_riotwatcher import *
import config

api = RiotWatcher(config.api_key)

r = api.get_all_champions()
f = open('champions.txt', 'a')

for c in r['champions']:
    f.write("%s: '%s',\n" % (c['id'], api.static_get_champion(c['id'])['name']))

f.close()

# r = api.static_get_item_list()

# f = open('items.txt', 'a')

# for i in r['data']:
    # f.write('%s: "%s",\n' % (r['data'][i]['id'], r['data'][i]['name']))
# f.close()