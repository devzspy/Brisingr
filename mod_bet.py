import string
import re
import MySQLdb

'''
    Currently a work in progress.
    
    Changelog for my own sanity
    ---------------------------
    April 18th 2017 - Started to write the script
    April 19th 2017 - Finished CheckPoints function. Added some high level pseudo code to map out what's needed.
                      Further defined how command syntax should look
'''

def on_load(bot):
    bot.add_command('add', addGame)
    bot.add_command('delete', delGame)
    bot.add_command('end', endGame)
    bot.add_command('bet', userBet)
    bot.add_command('checkpoints', checkPoints)

def on_exit(bot):
    bot.del_command('add')
    bot.del_command('delete')
    bot.del_command('end')
    bot.del_command('bet')
    bot.del_command('checkpoints')

def openDatabase():
    try:
        db = MySQLdb.connect(host="IP_ADDRESS",  # your host, usually localhost
                             user="DB_USERNAME",  # your username
                             passwd="DB_USERNAME_PASSWORD",  # your password
                             db="DB_NAME")  # name of the data base

        return db
    except:
        return
    
def addGame(bot, user, channel, args):      #Add a game for people to bet on
'''
    !addgame team1 team2

    Add a game. Reserved for admins?
'''
    msg = 'This is an example.'
    bot.send_msg(channel, msg)

def delGame(bot, user, channel, args):      #This is to delete a game if it was misadded
'''
    !delgame team1 team2

    Just here incase a game is misadded with the wrong teams etc. Reserved for admins?
'''
    msg = 'This is an example.'
    bot.send_msg(channel, msg)

def endGame(bot, user, channel, args):      #This is to end betting
'''
    !endgame team1/team2

    This will then "pop" the game out of the queue and pull the next game to the top of the stack.
    It will then allow !bet to just bet on the newest game rather than doing !bet game team points

    Reserved for admins

    Take the current game, curGame.remove essentially. Then give user points that guessed correct winning team. Remove points from
    people that guessed the incorrect winning team. Update all points accordingly.
    
'''
    msg = 'This is an example.'
    bot.send_msg(channel, msg)

def userBet(bot, user, channel, args):      #user places bet, checks points against db
'''
    !bet team points

    This should check the current game to see if the team exists. If not return error.
    Once the user has placed there bet, populate a dictionary/hash with all of the information to keep track.
    Check to see if the user even has points to bet. If not give them 50 (half the register cost)
'''
    try:
        db = openDatabase()

        cursor = db.cursor()

        user_exist_check = cursor.execute("SELECT nickname FROM leagueoflegends WHERE nickname='%s'" % user)
        if user_exist_check == 0:
            db.close()
            msg = "%s, you are currently not registered in the database. Please type !register to become eligible for betting." % user
            bot.send_msg(channel, msg)
        elif user_exist_check == 1:
            #insert code here
            msg = 'This is an example.'
            bot.send_msg(channel, msg)
    except:
        return

def checkPoints(bot, user, channel, args):      #Let's the users check how many points they have
'''
    !checkpoints - Queries the DB to check how many points the user has. Pretty self-explanatory.
    
'''
    try:
        db = openDatabase()

        cursor = db.cursor()
        
        user_exist_check = cursor.execute("SELECT nickname FROM leagueoflegends WHERE nickname='%s'" % user)
        if user_exist_check == 0:
            db.close()
            msg = "%s, you are currently not registered in the database. Please type !register to become eligible for betting." % user
            bot.send_msg(channel, msg)
        elif user_exist_check == 1:
            points = cursor.execute("SELECT points FROM leagueoflegends WHERE nickname='%s'" % user)
            msg = "%s: has %s points" % (user,points)
            bot.send_msg(channel, msg)
    except:
        return
