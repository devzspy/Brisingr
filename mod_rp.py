import random

def on_load(bot):
    bot.add_command('freerp', freerp)

def on_exit(bot):
    bot.del_command('freerp')

def freerp(bot, user, channel, args):
    r1 = random.randrange(0,9)
    r2 = random.randrange(0,9)
    r3 = random.randrange(0,9)
    r4 = random.randrange(0,9)
    r5 = random.randrange(0,9)
    r6 = random.randrange(0,9)
    r7 = random.randrange(0,9)
    r8 = random.randrange(0,9)
    r9 = random.randrange(0,9)
    r10 = random.randrange(0,9)
    r11 = random.randrange(0,9)

    msg = 'Congrats, ' + user + ', here is your free RP code which only you can see: ' + str(r1) + str(r2) + str(r3) + str(r11) + '-' + str(r4) + str(r5) + str(r6) + '-' + str(r7) + str(r8) + str(r9) + str(r10) + ' everyone else sees ***-***-**** do not share your code'

    bot.send_msg(channel, msg)
