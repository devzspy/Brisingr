import requests

def on_load(bot):
    bot.add_command('streams', streams)

def on_exit(bot):
    bot.del_command('streams')
    
def streams(bot, user, channel, args):
    payload = {'game': 'League of Legends', 'limit': '5'}
    r = requests.get('https://api.twitch.tv/kraken/streams', params = payload)

    data = r.json()['streams']
    
    msg = 'Top 5 LoL Streams online right now: '
    
    for stream in data:
        msg += stream['channel']['url'] + ' - ' + str(stream['viewers']) + ' viewers | '

    msg = str(msg[:len(msg) - 2])
    
    bot.send_msg(channel, msg)
