def on_load(bot):
    bot.add_command('trigger', example)

def on_exit(bot):
    bot.del_command('trigger')
    
def example(bot, user, channel, args):
    msg = 'This is an example.'
    bot.send_msg(channel, msg)