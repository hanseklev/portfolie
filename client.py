import socket
import utils
from printcolors import colors
import select 
import sys
from user import Bot, User, Chuck, Cathy
import threading

args = utils.getCommandLineArguments(True)

PORT = args[0]
IP =  '127.0.0.1' #127.0.0.1' #127.0.0.1' #
USERNAME = args[2]
ishuman = args[3]
free_for_all = True

if ishuman:
    user = User(USERNAME)
elif USERNAME == 'Chuck':
    user = Chuck(USERNAME)
elif USERNAME == 'Cathy':
    user = Cathy(USERNAME)
else: 
    user = Bot(USERNAME)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((IP, PORT))
    client.setblocking(0)
    client.send(user.getname().encode())
except socket.error as e:
    print(f'{colors.FAIL}Unable to connect..either the server is not running, or you have wrong port/IP' + colors.ENDC)
    quit()

def formatname(msg):
    text = str(msg)
    if (text.find(':') == -1):
         return text
    arr = text.split(":", 2)
    return str(f"{colors.FAIL}{arr[0]}: {colors.ENDC}{arr[1]}")

def prettifymessage(name, msg):
    if name == 'INFO':
        return str(f"{colors.WARNING}{msg}"+colors.ENDC)
    if name == 'HOST':
        return f"{colors.WARNING}{name}{colors.ENDC}: {msg}"

    return f"{colors.OKCYAN}{name}{colors.ENDC}: {msg}"



isrunning = True
response = ''

while isrunning:
    inputs = [sys.stdin ,client]
    read, write, _, = select.select(inputs, [], [], 5)
    response_msg = ''

    for s in read:
        if s is client:
            data = s.recv(1024)
            if not data:
                isrunning = False
                break
            else:
                parsed_msg = utils.parsedata(data)
                if len(parsed_msg) == 2: 
                    [name, msg] = parsed_msg
                    if name == 'HOST':             #Bots only responds to the hosts actions by default
                        response_msg = msg
                        print(prettifymessage(name, msg))
                    else:
                        if free_for_all and name != 'INFO':
                            response_msg = msg
                        print(prettifymessage(name, msg))
                else:
                    pass
                    #print('weir')
                    #print(parsed_msg[0])

        if ishuman:
            if select.select([sys.stdin,],[],[],0.0)[0]:
                response = sys.stdin.readline().strip()
            else:                               # If there is no input the program jumps to the top and checks for input
                continue                        # this way the user is not blocking incoming messages while typing
        else:
            if response_msg != '':
                response = user.respond(response_msg)
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