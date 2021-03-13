import socket
import utils
from printcolors import colors
import select 
import sys
from user import Bot, User
import threading


args = utils.getCommandLineArguments(True)
PORT = args[0]
IP = '192.168.0.6' #args[1]
USERNAME = args[2]
ishuman = args[3]

MSGLEN = 1024

def getuserinput():
    return input(f"{colors.OKBLUE}{USERNAME}: "+colors.ENDC)


if ishuman:
    user = User(USERNAME)
    inputthread = threading.Thread(target=getuserinput).start()

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
    if name == 'INFO' or name == 'HOST':
        return f"{colors.WARNING}{name}{colors.ENDC}: {msg}\n"

    return f"{colors.OKCYAN}{name}{colors.ENDC}: {msg}\n"




def closesession():
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    quit()

recv_message = ''
isrunning = True
response = ''

while isrunning:
    inputs = [sys.stdin ,client]
    read, write, _, = select.select(inputs, [], [], 5)

    for s in read:
        if s is client:
            data = s.recv(1024)
            if not data:
                isrunning = False
                break
            else:
                parsedmsg = utils.parsedata(data)
                if len(parsedmsg) == 2:
                    [name, msg] = parsedmsg
                    if name == 'INFO':
                        sys.stdout.write(f"{colors.WARNING}{msg}\n"+colors.ENDC)
                    else:
                        recv_message = msg
                        sys.stdout.write(prettifymessage(name, msg))
                else:
                    recv_message = parsedmsg[0]
                    sys.stdout.write(parsedmsg[0])
                sys.stdout.flush()

        #checks if the user is typing something, 
        if ishuman:
            if select.select([sys.stdin,],[],[],0.0)[0]:
                response = sys.stdin.readline().strip()
                #sys.stdin.flush()
            else:
                continue
        if not ishuman and recv_message != '':
            response = user.respond(recv_message)
            print(prettifymessage(USERNAME, response))

        if response == 'bye':
            client.send(response.encode()) 
            client.shutdown(socket.SHUT_RDWR)
        else:
            client.send(response.encode()) 

client.close()
print('Closing app..')
quit() 