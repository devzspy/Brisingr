import requests
from config import google_search_api_info

from mod_help import add_entry, del_entry

def on_load(bot):
    bot.add_command('google', google)
    add_entry('google', '!google <query>; Shows the first result of this Google Query')

def on_exit(bot):
    bot.del_command('google')
    del_entry('google')

def google(bot, user, channel, args):
    if len(args) == 0:
        bot.send_msg(channel, 'http://www.google.com')
        return
    
    key, cx = google_search_api_info['key'], google_search_api_info['cx']
    url = 'https://www.googleapis.com/customsearch/v1?key=%s&alt=json&googlehost=google.com&lr=lang_en&num=1&safe=high&cx=%s&q=' % (key, cx)
    
    try:
        r = requests.get(url + ' '.join(args))
        
        data = r.json()
        
        bot.send_msg(channel, str(data['items'][0]['link'] + ' - ' + data['items'][0]['title']))
    except:
        bot.send_msg(channel, 'Search Query has failed.')
