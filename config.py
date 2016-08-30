nickname = 'Brisingr'
realname = 'LoL IRC Stats Bot'
lineRate = None

sleeptimer = 10

Q_user = 'Q Auth name here'
Q_password = 'A Auth password here'

host = 'irc.quakenet.org'
port = 6667

channels = [
    #'#FalconSpy',
]

startup_modules = [
    'mod_admins',
    'mod_help',
    'mod_lol',
    'mod_insults',
    'mod_lmgtfy',
    'mod_twitch',
    #'mod_translate',
    #'mod_rwr',
    'mod_google',
    'mod_lolnews',
]

admins = {
    'SasCologne': False,
    'FalconSpy': True,
}

password = 'Bot Password Goes here'

trigger = '!'

ddragon_use_local_cache = False
ddragon_location = None

logfilename = 'log.txt'
print_to_console = True

api_key = 'Riot API Key goes here'
google_search_api_info = {'key': 'API Key here', 'cx': 'CX Key here'}
