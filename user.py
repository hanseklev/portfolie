import random
import re
from datetime import datetime, time
import time
from printcolors import colors

class Client:
    def __init__(self, name):
        self.name = str(name)
        self.count = 0
        
    def getname(self):
        return self.name

    

class Bot (Client):
    def __init__(self, name):
        Client.__init__(self, name)

    def respond(self, input):
        self.count += 1
        #print('count', self.count)
        if self.count > 4:
            return 'bye'

        if not input:
            return ''
        inputtype = self.analyzeinput(input)
        time.sleep(random.randint(3, 6))

        if inputtype =='NEW CONN':
            connectedbotname = input.split()[0]
            return f'Welcome to our midst {connectedbotname}'
        elif inputtype == 'QUESTION':
            return 'Not sure'
        elif inputtype == 'TIME':
            return str(f"The thime is {datetime.now().time()}")
        elif inputtype == 'WILDCARD':
            return 'Hmm. but did you know that?'
        if inputtype == 'CONNECTION':
            return 'Welcome'  

    def greet(self):
        GREETINGS = ['Hello', 'Hi!', 'Whassuup??', 'Howdy!', 'Yo']
        return random.choice(GREETINGS)


    def analyzeinput(self, input):
        if input.find("joined the room") != -1:
            return 'NEW CONN'
        elif input.find("?") != -1: #if input is a question
            if re.search('time', input, re.IGNORECASE): 
                return 'TIME'
            else:
                return 'QUESTION'
        else:
            return 'WILDCARD'


class User(Client):
    def __init__(self, name):
        Client.__init__(self, name)

    def respond(self, inputmsg):
        return input(f"{colors.OKBLUE}{self.name}: "+colors.ENDC)
