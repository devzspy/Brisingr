import urllib2
import json

def on_load(bot):
    bot.add_command('status', status)

def on_exit(bot):
    bot.del_command('status')

def status(bot, user, channel, args):
    if len(args) < 1:
        return

    shard = 'http://status.leagueoflegends.com/shards/'

    region = args[0].lower()

    full_url = shard + region

    response = urllib2.urlopen(full_url)

    json_response = response.read()

    incidents = json_response.count("content") - 1

    readable_json = json.loads(json_response)

    try:
        content = str(readable_json['services'][1]['incidents'][0]['updates'][0]['content'].encode('utf8'))
    except:
        content = "There are no reported issues at this time."

    content_replace = content.replace('\r\n', "")

    bot.send_msg(channel, "%s Server Status: %s" % (region.upper(), content_replace))
