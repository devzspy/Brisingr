from lib_riotwatcher import *
from items import items
from champions import champions
import config
import lol_ddragon
import utility

from datetime import timedelta

global api

game_types = {
    'NONE': 'Custom Game',						# Custom games
	'NORMAL': 'Normal 5x5',					# Summoner's Rift unranked games
	'NORMAL_3x3': 'Normal 3x3',				# Twisted Treeline unranked games
	'ODIN_UNRANKED': 'Dominion',			# Dominion/Crystal Scar games
	'ARAM_UNRANKED_5x5': 'ARAM',		# ARAM / Howling Abyss games
	'BOT': 'Coop 5x5',						# Summoner's Rift and Crystal Scar games played against AI
	'BOT_3x3': 'Coop 3x3',					# Twisted Treeline games played against AI
	'RANKED_SOLO_5x5': 'Ranked Solo',			# Summoner's Rift ranked solo queue games
	'RANKED_TEAM_3x3': 'Ranked 3x3',			# Twisted Treeline ranked team games
	'RANKED_TEAM_5x5': 'Ranked 5x5',			# Summoner's Rift ranked team games
	'ONEFORALL_5x5': 'One For All',			# One for All games
	'FIRSTBLOOD_1x1': 'Snowdown Showdown 1x1',			# Snowdown Showdown 1x1 games
	'FIRSTBLOOD_2x2': 'Snowdown Showdown 2x2',			# Snowdown Showdown 2x2 games
	'SR_6x6': 'Hexakill',					# Hexakill games
	'CAP_5x5': 'Team Builder',					# Team Builder games
	'URF': 'Ultra Rapid Fire',						# Ultra Rapid Fire games
	'URF_BOT': 'Coop Ultra Rapid Fire',					# Ultra Rapid Fire games against AI
        'KING_PORO_5x5': 'King Poro',               #King Poro ARAM
        'COUNTER_PICK': 'Nemesis',                  #Nemesis (Pick oponents champs)
        'BILGEWATER_5x5': 'Black Market Brawlers',       #Black Market Brawlers
}

summoner_ids = {

}

summoners = {
    "barrier": "Shields your champion for 115~455 health [95 + (20 x level)] for 2 seconds.",
    "clairvoyance": "Reveals an area of the map for 5 seconds.",
    "clarity": "Restores 40% maximum mana to you and your nearby allies.",
    "cleanse": "Removes all disables and summoner spell debuffs affecting your champion and lowers the duration of incoming disables by 65% for 3 seconds.",
    "exhaust": "Exhausts target enemy champion, reducing their Movement Speed and Attack Speed by 40%, their Armor and Magic Resist by 10, and their damage dealt by 40% for 2.5 seconds.",
    "flash": "Teleports your Champion to target nearby location under your mouse cursor.",
    "ghost": "Your champion passes through any unit and moves 27% faster for 10 seconds.",
    "heal": "Restores 90~345 health [75 + (15 x level)] to your champion and the allied champion nearest to the caster's cursor (or the most wounded ally if no target is near the cursor).\n*Healed champions are debuffed for 35 seconds, causing subsequent Heal casts on them to be 50% less effective.\n*Affected champions gain +30% movement speed for 1 second.",
    "ignite": "Targets a single champion dealing 70~410 true damage [50 + (20 x level)] over 5 seconds.\n*Also reduces the target's healing and regeneration by 50%.\n*Grants vision on target.",
    "smite": "Deals 390~1000 true damage, based on champion level, to a jungle monster, enemy minions, or pets.",
    "teleport": "After 4 seconds, teleports your champion to a non-champion, friendly target. Cooldown is shortened to 240 seconds if you teleport to a turret or if you cancel it by reactivating."
}

def on_load(bot):
    global api
    api = RiotWatcher(config.api_key)
    
    bot.add_command('free', free_to_play)
    bot.add_command('freeweek', free_to_play)
    bot.add_command('f2p', free_to_play)
    
    bot.add_command('summoner', summoner)
    
    bot.add_command('spell', spell)
    bot.add_command('skill', spell)
    
    bot.add_command('lg', last_game)
    bot.add_command('lm', last_game)
    bot.add_command('lastgame', last_game)
    bot.add_command('lastmatch', last_game)
    bot.add_command('last', last_game)
    bot.add_command('lmdetail', last_game_detail)
    bot.add_command('lgdetail', last_game_detail)
    
    bot.add_command('item', item)
    bot.add_command('patch', patch)

def on_exit(bot):
    bot.del_command('free')
    bot.del_command('freeweek')
    bot.del_command('f2p')
    
    bot.del_command('summoner')
    
    bot.del_command('skill')
    bot.del_command('spell')
    
    bot.del_command('lg')
    bot.del_command('lm')
    bot.del_command('lastgame')
    bot.del_command('lastmatch')
    bot.del_command('last')
    
    bot.del_command('item')
    bot.del_command('patch')

def patch(bot, user, channel, args):
    msg = "The bot is displaying info for patch: 6.19.1* (*May not be current, look up latest patch)"
    bot.send_msg(channel, msg)

def get_summoner_id(name, region):
    if name in summoner_ids:
        return summoner_ids[name]
    else:
        r = api.get_summoner(name = name, region = region)['id']
        summoner_ids[name] = r
        return r

def free_to_play(bot, user, channel, args):
    r = api.get_all_champions(free_to_play = True)
    
    names = []
    msg = 'This weeks free rotation: '
    
    for c in r['champions']:
        names.append(champions[c['id']])
    
    for n in names:
        msg += n + ', '
    
    msg = str(msg[:len(msg) - 2])
    bot.send_msg(channel, msg)

def summoner(bot, user, channel, args):
    if len(args) < 1:
        return
 
    choice = args[0].lower()

    #easter egg
    if choice is "D" or choice is "d":
        bot.send_msg(channel, 'Flash on D baby!.')
        return
    
    try:
        msg = summoners[choice]
    except KeyError:
        return
    
    msg = str(msg)
    bot.send_msg(channel, msg)

def last_game(bot, user, channel, args):
    if len(args) < 2:
        return
    id = get_summoner_id(''.join(args[1:]).lower(), args[0].lower())
    region = args[0].lower()
    try:
        r = api.get_recent_games(id,region)['games'][0]
    except:
        bot.send_msg(channel, 'Something went wrong.')
        return
    
    s = r['stats']
    
    if s['win']:
        result = 'WIN'
    else:
        result = 'LOSS'
    
    time = str(timedelta(seconds = s['timePlayed']))
    try:
        k = s['championsKilled']
    except:
        k = 0
    try:
        d = s['numDeaths']
    except:
        d = 0
    try:
        a = s['assists']
    except:
        a = 0
    try:
        mk = s['largestMultiKill']
    except:
        mk = 0

    if mk == 1:
        mk = "Solo Kill"
    elif mk == 2:
        mk = "Double Kill"
    elif mk == 3:
        mk = "Triple Kill"
    elif mk == 4:
        mk = "Quadra Kill"
    elif mk == 5:
        mk = "Penta Kill"
        
    kda = '%s/%s/%s (%s)' % (k, d, a, mk)
    try:
        cs = s['minionsKilled']
    except:
        cs = 0

    try:
        cs_neutral = s['neutralMinionsKilled']
    except:
        cs_neutral = 0

    try:
        gold_earned = str(s['goldEarned'])
    except:
        gold_earned = 'N/A'

    try:
        spell1 = r['spell1']
    except:
        spell1 = 'N/A'

    try:
        spell2 = r['spell2']
    except:
        spell2 = 'N/A'

    try:
        ward_kill = str(s['wardKilled'])
    except:
        ward_kill = 0

    try:
        ward_placed = str(s['wardPlaced'])
    except:
        ward_placed = 0
    
    item_list = []
    items_str = ''
    for i in range(0, 7):
        try:
            item_list.append(s['item' + str(i)])
        except:
            continue
    for item in item_list:
        items_str += items[item] + ', '
    items_str = str(items_str[:len(items_str) - 2])
    
    champ = champions[r['championId']]    
    
    summoners = {
        1: 'Cleanse',
        2: 'Clairvoyance',
        3: 'Exhaust',
        4: 'Flash',
        6: 'Ghost',
        7: 'Heal',
        11: 'Smite',
        12: 'Teleport',
        13: 'Clarity',
        14: 'Ignite',
        17: 'Garrison',
        21: 'Barrier',
        30: 'To the King!',
        31: 'Poro Toss',
        32: 'Mark',
        'N/A': 'Not Available'
    }
            
    summoner_str = summoners[spell1] + ', ' + summoners[spell2]

    champ = champions[r['championId']]    
    
    msg = '[%s] [%s] [%s] [%s] [%s] [Level: %s | Gold Earned: %s] [KDA: %s | CS: %s | Wards Used: %s] [Items: %s] [Summoners: %s]' % (' '.join(args[1:]), game_types[r['subType']], result, time, champ, str(s['level']), gold_earned, kda, str(cs+cs_neutral), ward_placed ,items_str, summoner_str)
        
    msg = str(msg)
    bot.send_msg(channel, msg)

def last_game_detail(bot, user, channel, args):
    if len(args) < 2:
        return
    id = get_summoner_id(''.join(args[1:]).lower(), args[0].lower())
    region = args[0].lower()
    try:
        r = api.get_recent_games(id,region)['games'][0]
    except:
        bot.send_msg(channel, 'Something went wrong.')
        return
    
    s = r['stats']
    
    if s['win']:
        result = 'WIN'
    else:
        result = 'LOSS'
    
    time = str(timedelta(seconds = s['timePlayed']))
    try:
        k = s['championsKilled']
    except:
        k = 0
    try:
        d = s['numDeaths']
    except:
        d = 0
    try:
        a = s['assists']
    except:
        a = 0
    try:
        mk = s['largestMultiKill']
    except:
        mk = 0

    if mk == 1:
        mk = "Solo Kill"
    elif mk == 2:
        mk = "Double Kill"
    elif mk == 3:
        mk = "Triple Kill"
    elif mk == 4:
        mk = "Quadra Kill"
    elif mk == 5:
        mk = "Penta Kill"
        
    kda = '%s/%s/%s (%s)' % (k, d, a, mk)
    try:
        cs = s['minionsKilled']
    except:
        cs = 0

    try:
        cs_neutral = s['neutralMinionsKilled']
    except:
        cs_neutral = 0

    try:
        cs_my_jungle = s['neutralMinionsKilledYourJungle']
    except:
        cs_my_jungle = 0

    try:
        cs_enemy_jungle = s['neutralMinionsKilledEnemyJungle']
    except:
        cs_enemy_jungle = 0

    try:
        gold_earned = str(s['goldEarned'])
    except:
        gold_earned = 'N/A'

    try:
        gold_spent = str(s['goldSpent'])
    except:
        gold_spent = 'N/A'

    try:
        spell1 = r['spell1']
    except:
        spell1 = 'N/A'

    try:
        spell2 = r['spell2']
    except:
        spell2 = 'N/A'

    try:
        ward_kill = str(s['wardKilled'])
    except:
        ward_kill = 0

    try:
        ward_placed = str(s['wardPlaced'])
    except:
        ward_placed = 0
    
    item_list = []
    items_str = ''
    for i in range(0, 7):
        try:
            item_list.append(s['item' + str(i)])
        except:
            continue
    for item in item_list:
        items_str += items[item] + ', '
    items_str = str(items_str[:len(items_str) - 2])


    summoners = {
        1: 'Cleanse',
        2: 'Clairvoyance',
        3: 'Exhaust',
        4: 'Flash',
        6: 'Ghost',
        7: 'Heal',
        11: 'Smite',
        12: 'Teleport',
        13: 'Clarity',
        14: 'Ignite',
        17: 'Garrison',
        21: 'Barrier',
        30: 'To the King!',
        31: 'Poro Toss',
        32: 'Mark',
        'N/A': 'Not Available'
    }
            
    summoner_str = summoners[spell1] + ', ' + summoners[spell2]

    champ = champions[r['championId']]    
    
    msg = '[%s] [%s] [%s] [%s] [%s] [Level: %s] [Gold Earned: %s | Spent: %s] [KDA: %s] [Total CS: %s | Enemy JG: %s | Your JG: %s] [Wards Used: %s | Killed: %s] [Items: %s] [Summoners: %s]' % (' '.join(args[1:]), game_types[r['subType']], result, time, champ, str(s['level']), gold_earned, gold_spent , kda, str(cs+cs_neutral), str(cs_enemy_jungle), str(cs_my_jungle), ward_placed, ward_kill, items_str, summoner_str)
        
    msg = str(msg)
    bot.send_msg(channel, msg)

def item(bot, user, channel, args):
    if len(args) < 1:
        return
    
    r = api.static_get_item_list()
    successful = False
    
    for data in r:
        for d in r.get(data):
            #d = item ID Number
            #r.get(data) = Giant string of items
            try:
                ret = r.get(data).get(d)
                # check if this is the item we're looking for
                if str(ret['name']).lower() == ' '.join(args[:]).lower():
                    #print str(ret['name']).lower()
                    msg = '[' + ret['name'] + '] '
                    msg += ret['description']
                    
                    msg = utility.strip_tags(msg)
                    
                    msg = str(msg)
                    bot.send_msg(channel, msg)
                    
                    successful = True # to avoid error messages
                    break
            except KeyError: # there's some unwanted data in the middle of the response, which we simply ignore
                pass
            
        if successful:
            return

def spell(bot, user, channel, args):
    s = {
        'Q': 0,
        'W': 1,
        'E': 2,
        'R': 3,
        'P': 'N/A',
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
    
    # check if passive is called, it has different data
    if args[1].lower() in ['p', 'passive']:
        data = data['passive']
        msg = '[%s | Passive | %s] %s' % (args[0], data['name'], data['description'])
        msg = utility.strip_tags(msg) # just to be sure
        msg = str(msg)
        bot.send_msg(channel, str(msg))
        return

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
    text = utility.strip_tags(text)
    
    msg = '[%s | %s | %s] [Cost: %s] [CD: %s] [Range: %s] %s' % (args[0], args[1].upper(), data['name'], cost, cd, range_, text)
    
    msg = str(msg)
    bot.send_msg(channel, msg)
