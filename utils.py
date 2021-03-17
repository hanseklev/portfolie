import argparse

DELIMITER = '#$%'
MOOD_WOORDS = ['you feeling', 'you doing', 'you all doing', 'whats up', "what's up", "thinking about"]
GREET_WORDS = ['hey', 'hey!', 'hello', 'hi']
JOKE_WORDS = ['funny', 'joke', 'jokes']
TOPICS = ['music', 'food', 'movie', 'joke', 'activity']

class colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


#Function that handles CLI args input for both server and client connection
def getCommandLineArguments(isclient = False):
    ipaddress = ''

    #bot options
    botname = ''
    response_limit = 5
    ishuman = False
    free_for_all = False

    #host options
    min_conns = 2
    host_is_passive = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--port" , "-p", type=int, help="Assign a port")

    if isclient: #add additional arguments for client CLI
        parser.add_argument("--ipaddress" , "-ip",  help="Assign a IP address")
        parser.add_argument("--bot" , "-b",  help="Assign a bot name")
        parser.add_argument("--limit", "-l", type=int, help="Set a response limit")
        parser.add_argument("--ishuman", action="store_true", help="Enable this if you want to chat with the bots")
        parser.add_argument("--freeforall", action="store_true", help="Enable this if to chat make the bots talk to each other")
    else:
        parser.add_argument("--conn" , "-c", type=int,  help="The minimum number of connections needed to open up the room (defaults to 2)")
        parser.add_argument("--ispassive", action="store_true", help="Prevents the server from engaging and starting conversation")

    args = parser.parse_args()
    port = args.port

    if isclient:
        ipaddress = args.ipaddress
        botname = args.bot
        ishuman = args.ishuman
        response_limit = args.limit
        free_for_all = args.freeforall
    else:
        if args.conn != None: 
            min_conns = args.conn
        host_is_passive = args.ispassive


    if (port == None):
        print('You have to provide a port number using the argument -p [PORT] or --port [PORT]')
        exit(2)
    if (isclient and ipaddress == None):
        print('You have to provide a ip-address using the argument -ip [ADDRESS] or --ipaddress [ADDRESS]')
        exit(2)
    if (isclient and botname == None):
        print('You have to assign a username using the argument -b [NAME] or --bot [NAME]')
        exit(2)

    port = int(port)
    min_conns = int(min_conns)
    if (isclient):
        return [ port, ipaddress, botname, ishuman, response_limit, free_for_all ]
    else:
        return [ port, min_conns, host_is_passive ]

def _getkeyword(pre, text):
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
        if pre == '':
            return words[-1]

        #assumes else it is the last word in the sentence and extracts it
        keywords = text.split(pre, 1)
        if len(keywords) > 1:
            keywords = keywords[1]
            keywords = keywords.strip()
        else:
            keywords = keywords[0]
        return keywords

def _responsepayload(inputtype, keyword = ''):
    return [inputtype, keyword]

#Analyzes the received message and returns the reponse type and a potential keyword
def analyzeinput(text):
    if text.find("joined the room") != -1:
        return _responsepayload('NEW CONN', text)
    if "?" in text or "what" in text:
        if "time" in text:
            return _responsepayload('TIME')
        if "random" in text or "on your mind" in text:
            return _responsepayload('RANDOM')
        if "how are you" in text or "how about you" in text:
            return _responsepayload('MOOD')
        if "favorite" in text:
            key = _getkeyword("favorite", text)
            return _responsepayload("FAVORITE", key)
        if "what do you like" in text:
            return _responsepayload("FAVORITE")
        if "do you like" in text:
            key = _getkeyword("like", text)
            return _responsepayload("FAVORITE", key)
        if "think about" in text:
            key = _getkeyword("about", text)
            return _responsepayload("QUESTION", key)
        if "talk about" in text or "suggestions" in text:
            key = _getkeyword("about", text)
            return _responsepayload("SUGGESTION", key)
        if "up to" in text or "plans for the day" in text or "wants to":
            key = _getkeyword("", text)
            return _responsepayload("ACTIVITY", key)
        if "why" in text:
            return _responsepayload("EXPLAIN")
        else:
            key = _getkeyword("what", text)
            return _responsepayload("QUESTION", key)
    if "not make sense" in text or "doesn't makes sense" in text or "you don't make sense" in text or "dont make sense" in text:
        return _responsepayload("ATTACK")
    if "lonely" in text:
        return _responsepayload("LONELY")
    if  any(word.lower() in text for word in JOKE_WORDS) and "tell" in text:
        return _responsepayload("JOKE")
    if any(word.lower() in text for word in GREET_WORDS):
        return _responsepayload("GREETING")
    else:
        return _responsepayload("WILDCARD")
