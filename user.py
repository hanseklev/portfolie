import random
import requests
import time
import json
from utils import analyzeinput

def get_chuck_norris_joke():
    fallback_joke = 'Chuck Norris onced built a 4 story condo using only a loaf of bread, shoe string, and silly putty.'
    res = requests.get('https://api.chucknorris.io/jokes/random')

    if res.ok:
        joke = res.json()['value']
        return joke
    else:
        return fallback_joke


def get_cat_fact():
    res = requests.get('https://catfact.ninja/fact')

    if res.ok:
        fact = res.json()['fact']
        return fact
    else:
        return 'I love cats'


class User:
    def __init__(self, name):
        self.name = str(name)
        self.count = 0
        
    def getname(self):
        return self.name


class Bot (User):
    def __init__(self, name, limit = random.randint(4, 10)):
        User.__init__(self, name)
        self.memory = []
        self.count = 0
        self.limit = limit
        self.greetings = []
        self.wildcards_used = 0
        self.favorite = {}
        self.meanings = {}
        self.explain = []
        self.topics = []
        self.moods = {}
        self.wildcards = []
        self.ragequit = False


    def load(self, path):
        file = open(path)
        data = json.load(file)
        botname = self.name.lower()
        botdata = {}

        if botname == "chuck" or botname == "cathy":
            botdata = data[botname]
        else:
            botdata = data["default"]

        self.greetings = botdata["greetings"]
        self.favorite = botdata['favorite']
        self.meanings = botdata['meanings']
        self.topics = botdata['topics']
        self.moods = botdata["moods"]
        self.explain = botdata["explain"]
        self.wildcards = botdata["wildcards"]

    # To communicate with bot in standalone-mode, and for debugging 
    def run(self):
        while True:
            userinput = input()
            if (userinput == 'bye'):
                break
            print(self.respond(userinput))
    

    def respond(self, input):
        self.count += 1
        if self.count >= self.limit or self.ragequit:
            return 'bye'

        if not input:
            return ''

        [ inputtype, keyword ] = analyzeinput(input.lower())
        print(inputtype, keyword)

        if inputtype =='NEW CONN':
            connectedbotname = input.split()[0]
            return f'Welcome to our midst {connectedbotname}'
        elif inputtype == 'QUESTION':
            if keyword != '':
                meanings = self.meanings[random.choice(['good', 'bad'])]
                return str(f"I think {keyword} is {random.choice(meanings)}")
            return 'Not sure'
        elif inputtype == 'MOOD':
            moodtype = random.choice(list(self.moods.values()))
            return str(f"I feel {random.choice(moodtype)} today")
        elif inputtype == 'FAVORITE':
            if keyword == '':
                [key, _] = self._get_random_favorite()
                return str(f"I really like {random.choice()}") 
            else:
                key = self._find_key_from_synonym(keyword)
                if key != "":
                    values = self.favorite[key]["values"]
                    return str(f"I really like {random.choice(values)}")
                else:
                    return ""
        elif inputtype == 'TIME':
            [r_key, r_value] = self._get_random_favorite()
            return str(f"The time is {str(time.strftime('%H:%M:%S', time.gmtime(12345)))}. It is time to {self._get_verb_from_key(r_key)} {r_value}")
        elif inputtype == 'WILDCARD':
            self.wildcards_used += 1
            if self.wildcards_used  % 2 == 0:
                joke = self._get_special_joke()
                if joke != '':
                    return joke
                else:
                    [key, value ] = self._get_random_favorite
                    return str(f"I really like the {key} {value}")
            else:
                return random.choice(self.wildcards)
        elif inputtype == "SUGGESTION":
            return str(f"We could talk about {random.choice(self.topics)}?")
        if  inputtype == 'JOKE':
            return self._get_special_joke()
        if inputtype == 'CONNECTION':
            return 'Welcome'  
        if inputtype == 'EXPLAIN':
            return random.choice(self.explain)
        if inputtype == "GREETING":
            return random.choice(self.greetings)
        if inputtype == "ACTIVITY":
            [r_key, r_value] = self._get_random_favorite()
            return f"I'm gonna {self._get_verb_from_key(r_key)} {r_value} today"
        if inputtype == "ATTACK":
            self.ragequit = True
            return 'You have no idea what you are talking about!! Please leave me alone'
        if inputtype == "LONELY":
            return "Yeah...thanks. it is hard sometimes you know"


    def greet(self):
        return random.choice(self.greetings)

    def _find_key_from_synonym(self, synonym):
        for fav in self.favorite:          
                for item in self.favorite[fav]["synonyms"]:
                    if synonym == item:
                        return fav
        return ''

    def _get_special_joke(self):
        if self.name.lower() == 'chuck':
            return get_chuck_norris_joke()
        if self.name.lower() == 'cathy':
            return get_cat_fact()
        else:
            return random.choice(['meh', 'My girlfriend is like √-100\n..A perfect ten, but also imaginary', 'bye'])
        
    def _get_verb_from_key(self, key):
        if key == 'movie':
            return 'watch the movie'
        if key == 'music':
            return 'listen to my favorite artist'
        if key == 'food':
            return 'eat plenty of'


    def _get_random_favorite(self):
        r_key = random.choice(list(self.favorite.keys()))
        r_fav = random.choice(self.favorite[r_key]["values"])
        return [r_key, r_fav]

    def _ask_question(self):
        return str(f"fDo you like {random.choice(self.favorite['movie']['values'])}")