import goslate
from languages import languages

def on_load(bot):
    bot.add_command('translate', translate)
    bot.add_command('detect', detect)

def on_exit(bot):
    bot.del_command('translate')
    bot.del_command('detect')

def detect(bot, user, channel, args):
    if len(args) < 1:
        return

    gs = goslate.Goslate()
    sentence = ' '.join(args[0:]).lower()

    detection = gs.detect(sentence)

    if str(detection) in languages:
        bot.send_msg(channel, "The language detected was: %s" % languages[str(detection)])
        return
    
def translate(bot, user, channel, args):
    if len(args) < 1:
        return
    gs = goslate.Goslate()

    arg_length = len(args)-1
    
    sentence = ' '.join(args[0:arg_length])
    
    translate = str(args[-1].title())

    if translate in languages.values():
        shorthand = languages.keys()[languages.values().index(translate)]

        shorthand = str(shorthand)

        translated = gs.translate(sentence, shorthand)

        translated = translated.encode('utf8')
        
        if '#FalconSpy' in channel:
            bot.send_msg(channel, translated)

