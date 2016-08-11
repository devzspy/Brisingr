def on_load(bot):
    bot.add_command('lmgtfy', lmgtfy_lookup)

def on_exit(bot):
    bot.del_command('lmgtfy')
    
def lmgtfy_lookup(bot, user, channel, args):
    if len(args) < 1:
        return

    lookup = ' '.join(args)
    
    replacement = lookup.replace(" ", "+")

    msg = 'http://lmgtfy.com/?q='
    msg += replacement
    
    bot.send_msg(channel, msg)
