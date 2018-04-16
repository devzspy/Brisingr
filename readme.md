## Authors
* SasCologne
* FalconSpy
* Boreaas
* BeamofLove
* FichteFoll

## Changelog
http://www.falconspy.org/irc-lol-bot-changelog/

## Requirements
* Python 2.7
* Twisted Matrix Library(https://twistedmatrix.com/trac/)

## Configurations
* Riot API Key
* Google Search API Key
* QuakeNet Auth Name and Password
* Bot Administrator password
* See the config.py for the rest!

## Commands
### League of Legends Commands
* !lm/!lg/!lastmatch/!lastgame [BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR] [Summoner name]
* !lmdetail/!lgdetail [BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR] [Summoner name]
* !summoner [flash/teleport/ignite/smite....]
* !spell/!skill [champion name] [q,w,e,r,p]
* !item [Insert Item name]
* !status [BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR]
* !streams  - Displays the top 5 steams for League of Legends on twitch
* !insult [Name of User]
* !google [Insert search query]
* !lmgtfy [Insert search query for lazy user]
* !patch - displays the patch LoL patch the bot is using
* !version - displays the bots version
* !lolnews [n] - Shows Nth most recent news article on LoL site (N is optional)
* !freerp - Just jokingly  outputs a code to the channel. Doesn't actually do anything

### Fortnite Commnads
* !fortstatus - Outputs the server status
* !fortid username - Outputs the player ID of the username supplied

## Admin Commands
* !auth [Auth password]
* !silence - The bot will stop responding to user commands (Type a second time to allow it to respond)
* !join #channel
* !leave #channel
* !load module_name
* !unload module_name
* !reload module_name