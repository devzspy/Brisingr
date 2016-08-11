# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

#TODO: SEPERATE MODULE
from twisted.words.protocols.irc import assembleFormattedText, attributes as A
import requests
import xml.etree.ElementTree as ET

# system imports
import time, sys
import cPickle as pickle
import re

# project imports
import config
import utility
from MessageLogger import *


class IRCBot(irc.IRCClient):
    nickname = config.nickname
    realname = config.realname
    lineRate = config.lineRate
    
    # custom attributes
    global commands, modules#, last_msg_time, last_msg#, regex_commands
    commands = {}
    # last_msg_time = int(time.time())
    # last_msg = ''
    # regex_commands = {}
    
    def __init__(self):
        self.is_silent = False
        self.anti_spam = {} # {'#channel': (time, message),}
    
    # custom methods
    def send_msg(self, channel, message):
        # spam protection
        if self.is_silent:
            return
        
        if channel in self.anti_spam and channel.startswith('#'):
            if time.time() - self.anti_spam[channel][0] >= config.sleeptimer and self.anti_spam[channel][1] != message:
                # send message and log it
                self.msg(channel, message, length = 410)
                self.logger.log('[OUT] [%s] %s' % (channel, message))
                self.anti_spam[channel] = (time.time(), message)
        else:
            # send message and log it
            self.msg(channel, message, length = 410)
            self.logger.log('[OUT] [%s] %s' % (channel, message))
            self.anti_spam[channel] = (time.time(), message)
        
    def send_say(self, channel, message):
        # spam protection
        if self.is_silent:
            return
        
        if channel in self.anti_spam and channel.startswith('#'):
            if time.time() - self.anti_spam[channel][0] >= config.sleeptimer and self.anti_spam[channel][1] != message:
                # send message and log it
                self.msg(channel, message, length = 410)
                self.logger.log('[OUT] [%s] %s' % (channel, message))
                self.anti_spam[channel] = (time.time(), message)
        else:
            # send message and log it
            self.msg(channel, message, length = 410)
            self.logger.log('[OUT] [%s] %s' % (channel, message))
            self.anti_spam[channel] = (time.time(), message)
    
    def load_module(self, module):
        try:
            if all(m != module for m in modules):
                    m = utility.reload_module(module)
                    m.on_load(self)
                    modules.append(module)
        except Exception, module:
                self.logger.log('[ERROR] %s, %s' % (Exception, module))
    
    def unload_module(self, module):
        try:
                m = __import__(module, globals(), locals(), [], -1)
                if module in modules:
                    m.on_exit(self)
                    modules.remove(module)
        except Exception, module:
                self.logger.log('[ERROR] %s, %s' % (Exception, module))
    
    def reload_module(self, module):
        self.unload_module(module)
        self.load_module(module)
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, 'a'))
        self.logger.log('[connected at %s]' %
                        time.asctime(time.localtime(time.time())))
    
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger = MessageLogger(open(self.factory.filename, 'a'))
        self.logger.log('[disconnected at %s]' %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()
    
    # commands & modules
    def add_command(self, trigger, callback):
        self.logger.log('[CMD] command \'%s\' registered to %s' % (trigger, callback))
        commands[trigger.lower()] = callback
        
    def del_command(self, trigger):
        self.logger.log('[CMD] command \'%s\' deleted' % trigger)
        del commands[trigger.lower()]
    
    def add_regex_command(self, trigger, callback):
        self.logger.log('[rCMD] command \'%s\' registered to %s' % (trigger, callback))
        regex_commands[trigger.lower()] = callback
    
    def del_regex_command(self, trigger):
        self.logger.log('[rCMD] command \'%s\' deleted' % trigger)
        del regex_commands[trigger.lower()]
    
    # TODO: ADD AS EXTRA MODULE
    def server_list(self, user, channel):
        map_names = {'map1': 'Moorland Trenches',
                     'map2': 'Keepsake Bay',
                     'map3': 'Old Fort Creek',
                     'map4': 'Fridge Valley',
                     'map5': 'Bootleg Islands',
                     'map6': 'Rattlesnake Crescent',
                     'map7': 'Power Junction',
                     'map8': 'Vigil Island',
                     'map9': 'Black Gold Estuary',
                     'map11': 'Copehill Down',
                     'map12': 'Frozen Canyon',
                     'pvp1': 'Islet of Eflen',
                     'race1': 'Race Track',}

        r = requests.get('http://rwr.runningwithrifles.com/rwr_server_list/get_server_list.php?start=0&size=100')
        root = ET.fromstring(r.text)

        servers = []

        for server in root.iter('server'):
            servers.append({'name': server.find('name').text,
                            'map_id': server.find('map_id').text,
                            'bots': server.find('bots').text,
                            'players': server.find('current_players').text,
                            'max_players': server.find('max_players').text,
                            'version': server.find('version').text,
                            'mode': server.find('mode').text,
                            'description': server.find('comment').text,
                            'location': server.find('country').text,
                            'ip': server.find('address').text,
                            'port': server.find('port').text,})

        servers = [server for server in servers if server['players'] != '0'] # remove empty servers

        for server in servers: # cleanup map_id
            server['map_id'] = server['map_id'].split('/')
            server['map_id'] = server['map_id'][len(server['map_id']) - 1]
            pattern = re.compile('|'.join(map_names.keys()))
            server['map_id'] = pattern.sub(lambda x: map_names[x.group()], server['map_id'])

        all_players = 0 # overall player count

        # overall players
        for server in servers:
            all_players += int(server['players'])

        msg = assembleFormattedText(A.normal['There are currently ', A.bold[str(all_players)], ' players on ', A.bold[str(len(servers))], ' servers.'])

        if channel == self.nickname:
                self.msg(user, msg)
        else:
            self.msg(channel, msg)

        # server list
        for server in servers:
            if int(server['players']) < 10:
                break
                
            if server['description'] == None:
                server['description'] = ''
                
            msg = assembleFormattedText(
                A.normal[
                    A.bold['[%s/%s] %s ' % (server['players'], server['max_players'], server['name'])],
                    '[%s] [%s] %s' % (server['location'], server['map_id'], server['description'])])
            
            if channel == self.nickname:
                self.msg(user, msg)
            else:
                self.msg(channel, msg)
    
    # callbacks for events
    def signedOn(self):
        '''Called when bot has successfully signed on to server.'''
        # auth with Q
        self.msg('Q@CServe.quakenet.org', 'AUTH ' + config.Q_user + ' ' + config.Q_password)
        self.mode(self.nickname, True, 'x')
        
        # load modules
        global modules
        modules = [utility.reload_module(module) for module in config.startup_modules]
        for m in modules:
            try:
                m.on_load(self)
            except:
                self.logger.log('[ERROR] Module %s could not be loaded.' % m)

        # join channels
        for channel in self.factory.channels:
            self.join(channel)
    
    def joined(self, channel):
        '''Called when bot joins a channel.'''
        self.logger.log('[JOIN] %s' % channel)
    
    def left(self, channel):
        '''Calle when bot leaves a channel.'''
        self.logger.log('[PART] %s' % channel)
    
    def privmsg(self, user, channel, msg):
        '''Called when bot receives a message.'''
        user = user.split('!', 1)[0]
        self.logger.log('[IN] [%s] <%s> %s' % (channel, user, msg))
        
        # TODO: seperate module
        if msg.startswith('?server') or msg.startswith('!server'):
            self.server_list(user, channel)
        
        elif msg.startswith(config.trigger): # TODO: make if again
            if msg.split()[0][1:].lower() in commands:
                commands[msg.split()[0][1:].lower()](self, user, channel, msg.split()[1:])
        
        # for cmd in regex_commands:
            # match = re.search(cmd, msg)
            # if match:
                # regex_commands[cmd](self, user, channel, match)
    
    def userJoined(self, user, channel):
        '''Called when user joins a channel.'''
        user = user.split('!', 1)[0]
        self.logger.log('[IN] [%s] %s joined the channel' % (channel, user))
        
    def userLeft(self, user, channel):
        '''Called when user leaves a channel.'''
        self.logger.log('[IN] [%s] %s left the channel' % (channel, user))
        
    def userQuit(self, user, quitMessage):
        '''Called when user disconnects from network.'''
        self.logger.log('[IN] %s quit (%s)' % (user, quitMessage))
        if user in config.admins:
            config.admins[user] = False
        
    def userKicked(self, kickee, channel, kicker, message):
        '''Called when user gets kicked from channel.'''
        self.logger.log('[IN] [%s] %s has been kicked by %s (%s)' % (channel, kickee, kicker, message))
        
    def userRenamed(self, oldname, newname):
        '''Called when user changes their name.'''
        self.logger.log('[IN] %s is now known as %s' % (oldname, newname))
        if oldname in config.admins and config.admins[oldname]:
            del config.admins[oldname]
            config.admins[newname] = True

class IRCBotFactory(protocol.ClientFactory):
    '''A factory for IRCBots.
    
    A new protocol instance will be created each time we connect to the server.'''
    
    def __init__(self, channels, filename):
        self.channels = channels
        self.filename = filename
    
    def buildProtocol(self, addr):
        p = IRCBot()
        p.factory = self
        return p
    
    def clientConnectionLost(self, connector, reason):
        '''If we get disconnected, reconnect to server.'''
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason
        reactor.stop()

if __name__ == '__main__':
    # create factory protocol and application
    f = IRCBotFactory(config.channels, config.logfilename)
    
    # connect factory to this host and port
    reactor.connectTCP(config.host, config.port, f)
    
    # run bot
    reactor.run()
