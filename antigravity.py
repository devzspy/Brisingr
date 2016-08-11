def on_load(bot):
    bot.send_msg('#r/leagueoflegends', 'https://xkcd.com/353/')
    bot.unload_module('antigravity')

def on_exit(bot):
    pass