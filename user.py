import random
import re
import datetime
import time
from printcolors import colors
import api
import json

GREETINGS = ['hello', 'hi!', 'whassuup??', 'howdy!', 'yo']


class Client:
    def __init__(self, name):
        self.name = str(name)
        self.count = 0
        
    def getname(self):
        return self.name


class User(Client):
    def __init__(self, name):
        Client.__init__(self, name)

    def respond(self, inputmsg):
        return input(f"{colors.OKBLUE}{self.name}: "+colors.ENDC)
    

class Bot (Client):
    def __init__(self, name):
        Client.__init__(self, name)
        self.memory = []
        self.count = 0
        self.wildcards_used = 0
        self.favorite = {}
        self.meaning = {}
        self.favorite['movie'] = {"synonyms": ['movies', 'tv-shows', 'movie'], "items": ['The terminator', 'WALL-E', 'Blade Runner', 'RoboCop', 'Westworld', 'Mr. Robot']}
        self.favorite['artist'] = { "synonyms": ['artist', 'music', 'band', 'bands', 'artists'], "items": ['Daft Punk', '30 Seconds To Mars', 'Rivers & Robots', 'Kraftwerk', 'Röyksopp'] }
        self.favorite['food'] = {"synonyms": ['eat', 'food', 'dinner', 'meal'], "items":['Fishballs', 'Fishcakes', 'Fish-sticks', 'Fish-pudding', 'Dry-fish']}
        self.meaning['good'] = ['nice', 'extraordinary', 'cosy', 'really good', 'out of this world']
        self.meaning['bad'] = ['despicable', 'really bad', 'not good']
        self.topics = ['music', 'food', 'the internet', 'not cats', 'something interesting']



    def load(self, path):
        f = open(path)
        data = json.load(f)

    def _run(self):
        while True:
            userinput = input()
            if (userinput == 'bye'):
                break
            print(self.respond(userinput))
    

    def respond(self, input):
        #self.count += 1
        #print('count', self.count)
        if self.count > 4:
            return 'bye'

        if not input:
            return ''
        [inputtype, keyword] = self._analyzeinput(input.lower())
        print(inputtype, keyword)
        if inputtype =='NEW CONN':
            connectedbotname = input.split()[0]
            return f'Welcome to our midst {connectedbotname}'
        elif inputtype == 'QUESTION':
            if keyword != '':
                meaning = self.meaning['good']
                return str(f"I really think {keyword} is {random.choice(meaning)}")
            return 'Not sure'
        elif inputtype == 'MOOD':
            return 'I dont know.. i guess i feel rather good today'
        elif inputtype == 'FAVORITE':
            fav_index = ''
            #iterates trough possible phrasings of different things, and returns the index
            for fav in self.favorite:          
                for syn in self.favorite[fav]:
                    for item in self.favorite[fav]["synonyms"]:
                        if keyword == item:
                            fav_index = fav
                            break

            if fav_index != "":
                key = self.favorite[fav_index]["items"]
                return str(f"I really like {random.choice(key)}")
            else:
                return "I can't answer that unfortunately, but I like many other things!"
        elif inputtype == 'TIME':
            return str(f"The time is {str(time.strftime('%H:%M:%S', time.gmtime(12345)))}")
        elif inputtype == 'WILDCARD':
            self.wildcards_used += 1
            if self.wildcards_used > 2:
                return ''
            return random.choice(['Yeah', 'I guess', 'Agree'])
        elif inputtype == "SUGGESTION":
            return str(f"We could talk about {random.choice(self.topics)}")
        if inputtype == 'CONNECTION':
            return 'Welcome'  
        if inputtype == "GREETING":
            return random.choice(GREETINGS)

        

    def greet(self):
        GREETINGS = ['Hello', 'Hi!', 'Whassuup??', 'Howdy!', 'Yo']
        return random.choice(GREETINGS)


    def _getkeyword(self, pre, text):
        words = text.split(" ")
        #Checks if the keyword is in the beginning of the sentence
        typical = ['is', 'do', 'are', 'type', 'kind']
        i = 0
        for _ in words:
            if words[i] == 'what' and words[i + 1] not in typical:
                keywords = words[i + 1].strip()
                return keywords
            i = i + 1

        text = text.replace("?", "")
        keywords = text.split(pre, 1)
        if len(keywords) > 1:
            keywords = keywords[1]
            keywords = keywords.strip()
        else:
            keywords = keywords[0]
        return keywords

    def _responsepayload(self, inputtype, keyword = ''):
        return [inputtype, keyword]

    def _analyzeinput(self, text):
        if text.find("joined the room") != -1:
            return self._responsepayload('NEW CONN', text)
        if text in GREETINGS:
            return self._responsepayload("GREETING")
        if "?" in text or "what" in text: #if input is a question
            if "time" in text:
                return self._responsepayload('TIME')
            if "random" in text or "on your mind" in text:
                return self._responsepayload('RANDOM')
            if "how are you" in text or "how about you" in text:
                return self._responsepayload('MOOD')
            if "do you like to" in text:
                key = self._getkeyword("to", text)
                return self._responsepayload("FAVORITE", key)
            if "favorite" in text:
                key = self._getkeyword("favorite", text)
                return self._responsepayload("FAVORITE", key)
            if "think about" in text:
                key = self._getkeyword("about", text)
                return self._responsepayload("QUESTION", key)
            if "talk about" in text or "suggestions" in text:
                return self._responsepayload("SUGGESTION")
            else:
                key = self._getkeyword("what", text)
                return self._responsepayload("QUESTION", key)
        else:
            return self._responsepayload("WILDCARD")



class Chuck(Bot):
    def __init__(self, name):
        Bot.__init__(self, name)
    
    def respond(self, input):
        self.count += 1
        if self.count > 4:
            return 'bye'

        if not input:
            return ''
        inputtype = self.analyzeinput(input)

        if inputtype =='NEW CONN':
            connectedbotname = input.split()[0]
            return f'Welcome to our midst {connectedbotname}'
        elif inputtype == 'QUESTION':
            return 'Not sure'

        elif inputtype == 'TIME':
            return str(f"The thime is {datetime.now().time()}")
        elif inputtype == 'WILDCARD':
            return f"I dont know about that.. but {api.get_chuck_norris_joke()}"
        if inputtype == 'CONNECTION':
            return 'Welcome'  

class Cathy(Bot):
    def __init__(self, name):
        Bot.__init__(self, name)
    
    def respond(self, input):
        self.count += 1
        if self.count > 4:
            return 'bye'

        if not input:
            return ''
        inputtype = self.analyzeinput(input)
        time.sleep(random.randint(2, 6))

        if inputtype =='NEW CONN':
            connectedbotname = input.split()[0]
            return f'Welcome to our midst {connectedbotname}'
        elif inputtype == 'QUESTION':
            return 'Not sure'

        elif inputtype == 'TIME':
            return str(f"The thime is {datetime.now().time()}")
        elif inputtype == 'WILDCARD':
            return f"Did you actually knew that {api.get_cat_fact()}"
        if inputtype == 'CONNECTION':
            return 'Welcome'  

