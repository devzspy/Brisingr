from pfaw import Fortnite,Platform

account_email = 'Enter your Epic Games email here'
account_password = 'Enter your Epic Games password here'
launch_token = 'Enter your launcher token authorization'
game_token = 'Enter your game token authorization'

fortnite = Fortnite(fortnite_token=game_token, launcher_token=launch_token, password=account_password, email=account_email)

def on_load(bot):
    bot.add_command('fortstatus', status)
    bot.add_command('fortid', fortID)

def on_exit(bot):
    bot.del_command('fortstatus')
    bot.del_command('fortid')

def status(bot, user, channel, args):
    status = fortnite.server_status()

    if status:
        msg = 'Fortnite servers are currently online.'
    else:
        msg = 'Fortnite servers are currently offline.'

    bot.send_msg(channel, msg)

def fortID(bot, user, channel, args):
    if len(args) < 1:
        return

    playername = args[0].lower()

    player = fortnite.player(username=playername)

    msg = player.name + "'s ID is" + player.id

    bot.send_msg(channel, msg)

    
