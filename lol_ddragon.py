import json
import config
import re
import string
import urllib2

normalization_pattern = re.compile('[^a-zA-Z]+') # Only retain alphabeticals

data_location = config.ddragon_location
web_data_location = "http://ddragon.leagueoflegends.com/cdn/6.20.1/data/en_US/"
use_local_cache = config.ddragon_use_local_cache

data_names = {
    "aatrox":   "Aatrox",
    "ahri":     "Ahri",
    "akali":    "Akali",
    "alistar":  "Alistar",
    "amumu":    "Amumu",
    "anivia":   "Anivia",
    "annie":    "Annie",
    "ashe":     "Ashe",
    "aurelionsol": "AurelionSol", "aurelion": "AurelionSol", "sol": "AurelionSol", "aurelion sol": "AurelionSol",
    "azir":     "Azir",
    "bard":     "Bard",
    "blitzcrank":"Blitzcrank", "blitz": "Blitzcrank",
    "brand":    "Brand",
    "braum":    "Braum",
    "caitlyn":  "Caitlyn", "cait": "Caitlyn",
    "cassiopeia":"Cassiopeia", "cass": "Cassiopeia", 
    "chogath":  "Chogath", "cho": "Chogath",
    "corki":    "Corki",
    "darius":   "Darius",
    "diana":    "Diana",
    "drmundo":  "DrMundo", "mundo": "DrMundo",
    "draven":   "Draven",
    "ekko":     "Ekko",
    "elise":    "Elise",
    "evelynn":  "Evelynn", "eve": "Evelynn",
    "ezreal":   "Ezreal", "ez": "Ezreal",
    "fiddlesticks":"Fiddlesticks", "fiddle": "Fiddlesticks",
    "fiora":    "Fiora",
    "fizz":     "Fizz",
    "galio":    "Galio",
    "gangplank":"Gangplank", "gp": "Gangplank",
    "garen":    "Garen",
    "gnar":     "Gnar",
    "gragas":   "Gragas",
    "graves":   "Graves",
    "hecarim":  "Hecarim", "pony": "Hecarim",
    "heimerdinger":"Heimerdinger", "heimer": "Heimerdinger", "donger": "Heimerdinger",
    "illaoi": "Illaoi", "hentai": "Illaoi",
    "irelia":   "Irelia",
    "ivern": "Ivern",
    "janna":    "Janna",
    "jarvaniv": "JarvanIV", "jarvan": "JarvanIV", "j": "JarvanIV",
    "jax":      "Jax",
    "jayce":    "Jayce",
    "jhin":     "Jhin",
    "jinx":     "Jinx",
    "kalista":  "Kalista",
    "karma":    "Karma",
    "karthus":  "Karthus",
    "kassadin": "Kassadin", "kassa": "Kassadin",
    "katarina": "Katarina", "kata": "Katarina",
    "kayle":    "Kayle",
    "kennen":   "Kennen",
    "khazix":   "Khazix", "kha": "Khazix", "bug": "Khazix",
    "kindred": "Kindred", "wolf":"Kindred",
    "kled": "Kled", "skaarl":"Kled",
    "kogmaw":   "KogMaw", "kog": "KogMaw",
    "leblanc":  "Leblanc",
    "leesin":   "LeeSin", "lee": "LeeSin",
    "leona":    "Leona",
    "lissandra":"Lissandra",
    "lucian":   "Lucian",
    "lulu":     "Lulu",
    "lux":      "Lux",
    "malphite": "Malphite", "malph": "Malphite",
    "malzahar": "Malzahar", "malz": "Malzahar",
    "maokai":   "Maokai",
    "masteryi": "MasterYi", "yi": "MasterYi",
    "missfortune":"MissFortune", "mf": "MissFortune",
    "mordekaiser":"Mordekaiser", "morde": "Mordekaiser",
    "morgana":  "Morgana", "morg": "Morgana",
    "nami":     "Nami", "fish": "Nami",
    "nasus":    "Nasus", "susan": "Nasus", "dog": "Nasus", "doge": "Nasus",
    "nautilus": "Nautilus", "naut": "Nautilus",
    "nidalee":  "Nidalee", "nida": "Nidalee", "nid": "Nidalee",
    "nocturne": "Nocturne", "noct": "Nocturne", "noc": "Nocturne",
    "nunu":     "Nunu",
    "olaf":     "Olaf",
    "orianna":  "Orianna", "ori": "Orianna",
    "pantheon": "Pantheon", "panth": "Pantheon",
    "poppy":    "Poppy",
    "quinn":    "Quinn",
    "rammus":   "Rammus",
    "reksai":   "Rek\'Sai",
    "renekton": "Renekton", "renek": "Renekton", "rene": "Renekton",
    "rengar":   "Rengar",
    "riven":    "Riven",
    "rumble":   "Rumble",
    "ryze":     "Ryze",
    "sejuani":  "Sejuani", "sej": "Sejuani",
    "shaco":    "Shaco",
    "shen":     "Shen",
    "shyvanna": "Shyvanna",
    "singed":   "Singed",
    "sion":     "Sion",
    "sivir":    "Sivir",
    "skarner":  "Skarner",
    "sona":     "Sona",
    "soraka":   "Soraka", "raka": "Soraka",
    "swain":    "Swain",
    "syndra":   "Syndra",
    "tahmkench":    "TahmKench", "tahm": "TahmKench", "Tahm Kench":"TahmKench",
    "taliyah": "Taliyah", "tali": "Taliyah",
    "talon":    "Talon",
    "taric":    "Taric",
    "teemo":    "Teemo",
    "thresh":   "Thresh",
    "tristana": "Tristana", "trist": "Tristana",
    "trundle":  "Trundle",
    "tryndamere":"Tryndamere", "trynd": "Tryndamere",
    "twistedfate":"TwistedFate", "tf": "TwistedFate", "Twisted Fate":"TwistedFate",
    "twitch":   "Twitch",
    "udyr":     "Udyr",
    "urgot":    "Urgot",
    "varus":    "Varus",
    "vayne":    "Vayne",
    "veigar":   "Veigar",
    "velkoz":   "Vel\'Koz",
    "vi":       "Vi",
    "viktor":   "Viktor",
    "vladimir": "Vladimir", "vlad": "Vladimir",
    "volibear": "Volibear", "voli": "Volibear",
    "warwick":  "Warwick", "ww": "Warwick",
    "wukong":   "MonkeyKing", "monkeyking":"MonkeyKing",
    "xerath":   "Xerath",
    "xinzhao":  "XinZhao", "xin": "XinZhao", "Xin Zhao":"XinZhao",
    "yasuo":    "Yasuo",
    "yorick":   "Yorick",
    "zac":      "Zac",
    "zed":      "Zed",
    "ziggs":    "Ziggs",
    "zilean":   "Zilean", "zil": "Zilean",
    "zyra":     "Zyra",
}

def normalize_name(name):
    return data_names[normalization_pattern.sub('', name).lower()]

def get_champion(name):
    name = normalize_name(name)

    if use_local_cache:
        with open(data_location + 'champion/' + name + '.json') as f:
            return json.load(f)

    else:
        response = urllib2.urlopen(web_data_location + "champion/" + name + ".json").read()
        return json.loads(response)

def get_summoner():
    
    if use_local_cache:
        with open(data_location + 'summoner.json') as f:
            return json.load(f)

    else:
        response = urllib2.urlopen(web_data_location + "summoner.json").read()
        return json.loads(response)

