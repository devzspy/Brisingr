import config

def on_load(bot):
    bot.add_command('load', load)
    bot.add_command('unload', unload)
    bot.add_command('reload', reload)
    bot.add_command('join', join)
    bot.add_command('leave', leave)
    bot.add_command('silence', silent)
    bot.add_command('auth', auth)

def on_exit(bot):
    bot.del_command('load')
    bot.del_command('unload')
    bot.del_command('reload')
    bot.del_command('join')
    bot.del_command('leave')
    bot.del_command('silence')
    bot.del_command('auth')

def is_admin(user):
    if user in config.admins and config.admins[user]:
        return True
    else:
        return False

def load(bot, user, channel, args):
    if len(args) < 1:
        return
    
    if is_admin(user):
        bot.load_module(args[0])
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)

def unload(bot, user, channel, args):
    if len(args) < 1:
        return
    
    if is_admin(user):
        bot.unload_module(args[0])
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)

def reload(bot, user, channel, args):
    if len(args) < 1:
        return
    
    if is_admin(user):
        bot.reload_module(args[0])
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)

def join(bot, user, channel, args):
    if len(args) < 1:
        return
    
    if is_admin(user):
        bot.join(args[0])
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)
        
def leave(bot, user, channel, args):
    if len(args) < 1:
        args.append(channel)
    
    if is_admin(user):
        bot.leave(args[0])
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)

def silent(bot, user, channel, args):
    if is_admin(user):
        if not bot.is_silent:
            msg = 'Okay, I\'ll shut up.'
            bot.send_msg(channel, msg)
            bot.is_silent = True
        else:
            bot.is_silent = False
            msg = 'Hooray! I can talk again!'
            bot.send_msg(channel, msg)
    else:
        msg = 'You are not allowed to do this.'
        bot.send_msg(channel, msg)

def auth(bot, user, channel, args):
    if len(args) < 1:
        return
    
    if user in config.admins and args[0] == config.password:
        config.admins[user] = True
        msg = 'You have successfully authed.'
        bot.send_msg(user, msg)
    elif user not in config.admins:
        msg = 'You are not allowed to do this.'
        bot.send_msg(user, msg)
    elif args[0] != config.password:
        msg = 'Wrong password.'
        bot.send_msg(user, msg)
