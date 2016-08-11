import requests
import utility
import xml.etree.ElementTree as ET
from datetime import datetime as DT
import unicodedata

from mod_help import add_entry, del_entry

# TODO: URL-shortener

def on_load(bot):
    bot.add_command('news', get_latest_news)
    add_entry('lolnews', '!lolnews <n>; Shows n-th most recent news article, argument n is optional. Defaults to most recent news.')

def on_exit(bot):
    bot.del_command('news')
    del_entry('lolnews')
    
def get_latest_news(bot, user, channel, args):
    r = requests.get('http://euw.leagueoflegends.com/en/rss.xml')
    items = ET.fromstring(r.text.encode('utf-8')).findall('channel/item')
    
    news = []
    
    for item in items:
        title = item.findtext('title')
        desc = item.findtext('description')
        link = item.findtext('link')
        pub_date = item.findtext('pubDate')
        
        # get rid of HTML junk
        desc = utility.strip_tags(desc)
        
        # format pubDate
        # comes as: Wed, 29 Jun 2016 18:38:05 +0000
        pub_date = DT.strptime(pub_date[:-6], '%a, %d %b %Y %X').strftime('%d.%m.') # [:-6] because python is fucking stupid when it comes to times and dates
        
        news.append((pub_date, title, link, desc))
    
    if len(args) < 1: # default to most recent news
        pub_date, title, link, desc = news[0]
    else:
        try: # check for nonsensical arguments
            int(args[0])
        except ValueError:
            index = 0
        else:
            index = int(args[0])

        if int(index) > len(news):
            msg = 'Only ' + str(len(news)) + ' articles in the feed.'
            bot.send_msg(channel, msg)
            return
        
        try:
            pub_date, title, link, desc = news[index - 1]
        except:
            msg = 'Article not found.'
            bot.send_msg(channel, msg)
            return
    
    msg = '[%s] [%s] %s - %s' % (pub_date, title, link, desc)
    msg = msg.replace('\n', ' ')
    try: # If Unicode, e.g. the Euro-sign, is in the text, get rid of it because Twisted can't handle it
        msg = unicodedata.normalize('NFKD', msg).encode('ascii', 'ignore')
    except TypeError:
        pass
    msg = str(msg)
    bot.send_msg(channel, msg)