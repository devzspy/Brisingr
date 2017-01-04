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
    "pony": "Hecarim",
    "helicopter": "Hecarim",
    "donger": "Heimerdinger",
    "hentai": "Illaoi",
    "j4": "JarvanIV",
    "bug": "Khazix",
    "k6": "Khazix",
    "wolf": "Kindred", 
    "lamb": "Kindred",
    "skaarl": "Kled",
    "susan": "Nasus",
    "dog": "Nasus",
    "doge": "Nasus",
    "wukong": "MonkeyKing",
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
    key = name_to_key(name)

    if use_local_cache:
        with open(data_location + 'champion/' + key + '.json') as f:
            return json.load(f)

    else:
        url = web_data_location.format(version=patch_version) + "champion/" + key + ".json"
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

    if patch_version != version:
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
