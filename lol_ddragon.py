import json
import config
import re
import urllib2

data_location = config.ddragon_location
patch_version = None
web_data_location = "http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/"
use_local_cache = config.ddragon_use_local_cache

id_to_name_map = {}
name_to_key_map = {}
custom_aliases = {
    "aurelion": "AurelionSol", 
    "sol": "AurelionSol", 
    "blitz": "Blitzcrank",
    "cait": "Caitlyn",
    "cass": "Cassiopeia", 
    "cho": "Chogath",
    "mundo": "DrMundo",
    "eve": "Evelynn",
    "ez": "Ezreal",
    "fiddle": "Fiddlesticks",
    "gp": "Gangplank",
    "pony": "Hecarim",
    "helicopter": "Hecarim",
    "heimer": "Heimerdinger", 
    "donger": "Heimerdinger",
    "hentai": "Illaoi",
    "jarvan": "JarvanIV", 
    "j4": "JarvanIV",
    "kass": "Kassadin", 
    "kassa": "Kassadin",
    "kata": "Katarina", 
    "kat": "Katarina",
    "kha": "Khazix", 
    "bug": "Khazix",
    "k6": "Khazix",
    "wolf": "Kindred", 
    "lamb": "Kindred",
    "kled": "Kled", 
    "skaarl": "Kled",
    "kog": "KogMaw",
    "lee": "LeeSin",
    "liss": "Lissandra",
    "malph": "Malphite",
    "malz": "Malzahar",
    "yi": "MasterYi",
    "mf": "MissFortune",
    "morde": "Mordekaiser",
    "morg": "Morgana",
    "susan": "Nasus",
    "dog": "Nasus",
    "doge": "Nasus",
    "naut": "Nautilus",
    "nida": "Nidalee", 
    "nid": "Nidalee",
    "noct": "Nocturne",
    "noc": "Nocturne",
    "ori": "Orianna",
    "panth": "Pantheon",
    "renek": "Renekton",
    "rene": "Renekton",
    "sej": "Sejuani",
    "raka": "Soraka",
    "tahm": "TahmKench",
    "tali": "Taliyah",
    "trist": "Tristana",
    "trynd": "Tryndamere",
    "tf": "TwistedFate",
    "vlad": "Vladimir",
    "voli": "Volibear",
    "ww": "Warwick",
    "wukong": "MonkeyKing",
    "xin": "XinZhao",
    "zil": "Zilean",
}

def normalize_name(name):
    # Only retain alphanumerics and lower-case
    return re.sub(r'[^a-zA-Z0-9]+', '', name).lower()

def name_to_key(name):
    # Only retain alphanumerics and lower-case
    name = normalize_name(name)
    if name in name_to_key_map:
        return name_to_key_map[name]
    else:
        return None

def get_champion(name):
    name = normalize_name(name)

    if use_local_cache:
        with open(data_location + 'champion/' + name + '.json') as f:
            return json.load(f)

    else:
        url = web_data_location.format(version=patch_version) + "champion/" + name + ".json"
        print(url)
        response = urllib2.urlopen(url).read()
        return json.loads(response)

def get_summoner():
    if use_local_cache:
        with open(data_location + 'summoner.json') as f:
            return json.load(f)

    else:
        response = urllib2.urlopen(web_data_location.format(version=patch_version)
                                   + "summoner.json").read()
        return json.loads(response)

def set_patch_version(api, version):
    global patch_version

    patch_version = version
    build_name_to_key_map(api)

def build_name_to_key_map(api):
    champions = api.static_get_champion_list()
    name_to_key_map.clear()
    id_to_name_map.clear()

    for champion in champions['data'].values():
        name_to_key_map[normalize_name(champion['name'])] = champion['key']
        id_to_name_map[champion['id']] = champion['name']

    name_to_key_map.update(custom_aliases)
