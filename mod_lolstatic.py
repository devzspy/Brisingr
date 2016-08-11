from twisted.words.protocols.irc import assembleFormattedText, attributes as A
import config
from utility import strip_tags

from mod_help import add_entry as add_help_entry
from mod_help import del_entry as del_help_entry
import lol_ddragon

def on_load(bot):
    bot.add_command('spell', spell)
    bot.add_command('skill', spell)
    add_help_entry('spell', '?spell <champion> <key>; Shows the statistics of the spell.')
    add_help_entry('skill', '?skill <champion> <key>; Shows the statistics of the spell.')

def on_exit(bot):
    bot.del_command('spell')
    bot.del_command('skill')
    del_help_entry('spell')
    del_help_entry('skill')
    
def spell(bot, user, channel, args):
    # msg = 'This is an example.'
    # bot.send_msg(channel, msg, length = 450)
    
    s = {
        'Q': 0,
        'W': 1,
        'E': 2,
        'R': 3,
    }
    
    scalings = {
        'bonusattackdamage': 'Bonus AD',
        'spelldamage': 'AP',
        'attackdamage': 'AD',
        '@stacks': 'per Stack',
        '@dynamic.attackdamage': 'Dyn. AD',
        '@special.dariusr3': '+ 32/50/68 per Stack',
        'health': 'HP',
        'abilitypower': 'AP',
    }
    
    # easteregg
    if len(args) < 1:
        return
        
    if args[0].lower() in ['riottriggs', 'triggs', 'triggs390']:
        bot.send_msg(channel, 'Triggs has no skill.')
        return
    # /easteregg
    
    if len(args) < 2:
        return
        
    args[0] = lol_ddragon.normalize_name(args[0])
    
    data = lol_ddragon.get_champion(args[0])['data'][args[0]]
    passive = data['passive']
    data = data['spells'][s[args[1].upper()]]
    
    cost = data['resource']
    text = data['tooltip']
    effects = data['effectBurn']
    
    for i, e in enumerate(effects):
    
        cost = cost.replace('{{ e' + str(i) + ' }}', str(e))
        text = text.replace('{{ e' + str(i) + ' }}', str(e))
    
    cost = cost.replace('{{ cost }}', data['costBurn'])
    cd = data['cooldownBurn']
    range_ = data['rangeBurn']
    
    for i, a in enumerate(data['vars']):
        scale = ''
        if a['link'] in scalings:
            scale = ' ' + scalings[a['link']]
        text = text.replace('{{ ' + a['key'] + ' }}', str(a['coeff']) + scale)
    text = strip_tags(text)
    
    
    # msg  = '[' + args[0] + ' | ' + args[1].upper() + ' | ' + data['name'] + '] '
    # msg += '[Cost: ' + cost + '] [CD: ' + cd + '] [Range: ' + range_ + '] '
    # msg += '[' + text + ']'
    
    msg = assembleFormattedText(A.normal['[', A.bold[args[0]], ' | ',
                                    A.bold[args[1].upper()], ' | ', A.bold[str(data['name'])], '] [',
                                    A.bold['Cost: '], cost + '] [', A.bold['CD: '],
                                    cd + '] [', A.bold['Range: '], range_ + '] [' + text + ']'])
    
    bot.send_msg(channel, str(msg))