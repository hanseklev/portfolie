import socket
import utils
from utils import colors
import select 
import sys
from User import Bot, User
import time, random

args = utils.getCommandLineArguments(True)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

[ PORT, IP, USERNAME, ishuman, response_limit, free_for_all ] = args

if ishuman:
    user = User(USERNAME)
else: 
    user = Bot(USERNAME)
    user.load('bot-data.json')

try:
    client.connect((IP, PORT))
    client.setblocking(False)
    client.send(user.getname().encode())
except socket.error as e:
    print(f'{colors.FAIL}Unable to connect..either the server is not running, or you have wrong port/IP' + colors.ENDC)
    quit()
else:
    print(colors.WARNING + f"\n******* WELCOME {USERNAME} THE BOTINATOR 2000 *******\n" + colors.ENDC)


def formatname(msg):
    text = str(msg)
    if (text.find(':') == -1):
         return text
    arr = text.split(":", 2)
    return str(f"{colors.FAIL}{arr[0]}: {colors.ENDC}{arr[1]}")

def parsedata(msg):
    decoded_msg = msg
    try:
        decoded_msg = msg.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    return str(decoded_msg).split(utils.DELIMITER)


def prettifymessage(name, msg):
    if name == 'INFO':
        return str(f"{colors.WARNING}{msg}"+colors.ENDC)
    if name == 'HOST':
        return f"{colors.WARNING}{name}{colors.ENDC}: {msg}"
    if name == USERNAME:
        return f"{colors.BLUE}You{colors.ENDC}: {msg}"
    else:
        return f"{colors.CYAN}{name}{colors.ENDC}: {msg}"


isrunning = True
response = ''

while isrunning:
    inputs = [sys.stdin, client]
    read, write, _, = select.select(inputs, [], [], 10)
    response_msg = ''

    for s in read:
        if s is client:
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                print(colors.FAIL+"Something bad happened, try to reconnect"+colors.ENDC)
                isrunning = False
                break
            if not data:
                isrunning = False
                break
            else:
                parsed_msg = parsedata(data)
                if len(parsed_msg) == 2: 
                    [name, msg] = parsed_msg
                    if name == 'HOST':             #Bots only responds to the hosts actions by default
                        response_msg = msg
                        print(prettifymessage(name, msg))
                    else:
                        if free_for_all and name != 'INFO':
                            response_msg = msg
                        print(prettifymessage(name, msg))

        if ishuman:
            if select.select([sys.stdin,],[],[],0.0)[0]:
                response = sys.stdin.readline().strip()
            else:                               # If there is no input the program jumps to the top and checks for input
                continue                        # this way the user is not blocking incoming messages while typing
        else:
            if response_msg != '':
                time.sleep(random.randint(200, 350)/100)  # Add some delay to the bot response to prevent mayhem
                response = user.respond(response_msg)
                if response == '':
                    continue
                print(prettifymessage(USERNAME, response))
            else:
                continue

        if response == 'bye':
            client.send(response.encode()) 
            client.shutdown(socket.SHUT_RDWR)
        else:
            client.send(response.encode()) 

client.close()
print('Closing app..')
quit() 