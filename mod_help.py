global commands
commands = {}

def on_load(bot):
    bot.add_command('help', bothelp)
    bot.add_command('admins', adminhelp)
    bot.add_command('adurna', bothelp)
    bot.add_command('version', version)

def on_exit(bot):
    bot.del_command('help')
    bot.del_command('admins')
    bot.del_command('adurna')
    bot.del_command('version')

def bothelp(bot, user, channel, args):
    msg = 'This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.'
    msg += '\nCreated by SasCologne, boreeas, and FalconSpy. Hosted by FalconSpy'
    msg += '\nThe following commands are available: lg, lm, lastgame, lastmatch, summoner, spell, streams, detect, status, patch, version and lmgtfy'
    msg += '\nSyntax: !lm/lg <region> <summoner>, !summoner <flash>, !spell <champion> <q,w,e,r>, !lmgtfy <search string>,!item <Item Name> (Case Sensitive), !streams (display top 5 streamers), !detect <sentence> (displays language spoken), !status <region>, !patch, !version'


    
    for cmd in commands:
        msg += '\n' + commands.get(cmd)
    
    bot.send_msg(user, msg)

def adminhelp(bot, user, channel, args):
    msg = '\nThe following commands are available for admins: silence, join, leave'
    
    for cmd in commands:
        msg += '\n' + commands.get(cmd)
    
    bot.send_msg(user, msg)

def version(bot, user, channel, args):
    msg = 'This bot is currently running version: 2.3 - for the latest version visit: http://www.falconspy.org/category/projects/irc-league-of-legends-bot/'
    bot.send_msg(user, msg)

def add_entry(trigger, text):
    global commands
    commands[trigger.lower()] =  text

def del_entry(trigger):
    global commands
    del commands[trigger.lower()]
