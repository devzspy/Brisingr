# system imports
import time

# project imports
import config

class MessageLogger:
    global print_to_console
    print_to_console = config.print_to_console

    def __init__(self, file):
        self.file = file
    
    def log(self, message):
        '''Write a message to the file.'''
        timestamp = time.strftime('[%H:%M:%S]', time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()
        
        if print_to_console:
            print '%s %s' % (timestamp, message)
    
    def close(self):
        self.file.close()