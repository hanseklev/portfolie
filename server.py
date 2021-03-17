import socket
import time
import utils
from utils import colors
import select
import errno
import random
import queue

args = utils.getCommandLineArguments()

PORT = args[0]
IP = socket.gethostbyname(socket.gethostname())
MIN_CONN = args[1]
host_is_passive = args[2]

print(colors.WARNING + "\n******* STARTING UP THE BOTINATOR 2000 *******\n" + colors.ENDC)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((IP, PORT))
server.listen()
print(f"{colors.GREEN}Server is running on port {PORT}\nIP: {IP}" + colors.ENDC)

inputs = [server]
outputs = []
msg_queues = {}
client_list = []
HOST_GREETINGS= ["How are you feeling?", "How are you all doing?", "What are you thinking about today?"]
reponse_memory = []
host_memory = []

#ensures that all clients has responded before broadcast new messsage
clients_finished = 0 

def get_ice_breaker(word):
    breakers = [f"What is your favorite {word}?", f"What do you think about {word}?", "Tell me a joke or something", "Do you have any plans for the day?", f"Who wants to get together and put on a {word}?", "What time is it?"]
    return random.choice(breakers)

def sendtoothers(conn, msg):
    name = getnamefromconn(conn, client_list)
    for c in client_list:
        if c["conn"] is not conn:
            try:
                c["conn"].send(addnametodata(name, msg))
            except socket.error as e:
                print(colors.WARNING+"Oops socket error:\n" + colors.ENDC, e)
            except IOError as e:
                if e.errno == errno.EPIPE:
                    print(colors.WARNING+f"{name} broke a pipe.. :({e.errno}"+ colors.ENDC)
                print(colors.FAIL+"Something went wrong.." + colors.ENDC, e)   


def broadcast(msg, isinfo = False):
    time.sleep(0.5)
    host_memory.append(msg)
    msg_type = "INFO" if isinfo else "HOST"
    for c in inputs:
        if c is not server:
            try:
                c.send(addnametodata(msg_type, msg))
            except BrokenPipeError:
                print(colors.WARNING+"Broke a pipe.. :("+ colors.ENDC)



def addclient(client, name):
    inputs.append(client)
    client_list.append({"name": name, "conn": client})
    msg_queues[client] = queue.Queue()         
    msg = str(f"{colors.BLUE}{name} joined the room"+colors.ENDC)       
    broadcast(msg.encode(), isinfo=True)
    print(msg)


def removeclient(conn):
    client = getclientfromconn(conn, client_list)
    name = client["name"]
    print(f"{name} logged off")
    inputs.remove(conn)
    if s in outputs:
        outputs.remove(s)
    del msg_queues[conn]
    client_list.remove(client)
    conn.close()
    broadcast(str(f"{colors.WARNING}{name} logged off"+colors.ENDC).encode(), isinfo=True)


def broadcast_greeting():
    broadcast(random.choice(HOST_GREETINGS))


def broadcast_from_memory():
    time.sleep(1)
    keyword = ""
    last_msg = host_memory[-1]
    if last_msg in HOST_GREETINGS:
        broadcast("That's nice to hear. What should we talk about today?")
    msg = ""

    #host iterates through last sendt messages, to hopefully find something to spin on
    for i in range(len(reponse_memory)):
        [inputtype, keyword] = utils.analyzeinput(reponse_memory[-i])
        if keyword != "":
            break
    if keyword != "":
        if inputtype == "SUGGESTION":
            msg = str(f"What is your favorite {keyword}?")
        msg = str(f"Let's talk some more about {keyword}")
        broadcast(msg)
    else:
        broadcast(get_ice_breaker(random.choice(utils.TOPICS)))
    reponse_memory.clear()


def addnametodata(name, msg):
    try:
        msg = msg.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    return str(name+utils.DELIMITER+msg).encode()


def getclientfromconn(conn, clients):
    for c in clients:
        if c["conn"] is conn:
            return c


def getnamefromconn(conn, clients):
    for c in clients:
        if c["conn"] is conn:
            return c["name"]


# Loop that handles the inital connection, don"t register messages sendt, just connections.
# Moves on to the main loop when the minimum connection requirement is set
print(f"Waiting for {MIN_CONN} more connections")
while len(inputs) - 1 < MIN_CONN:
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 10)
    
    for s in readable:
        if s is server:
            client, address = server.accept()
            client.setblocking(False)
            time.sleep(0.2)
            name = client.recv(1024).decode()
            addclient(client, name)
        else:
            data = s.recv(1024)
            if not data:
                if s in outputs:
                    outputs.remove(s)
                removeclient(s)


print(f"{colors.WARNING}Let the chatting begin :-)"+colors.ENDC)
if host_is_passive:
    broadcast("Welcome to the chat-room!\nI am just gonna sit back and watch..enjoy!", isinfo=False)
else:
    broadcast_greeting()


while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:
        if s is server:
            client, address = server.accept()
            client.setblocking(0)
            name = client.recv(1024).decode()
            addclient(client, name)

        else:
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                print(f"{colors.WARNING}socket disconnected badly..\nBut we are swimming on!"+colors.ENDC)

            if not data:
                removeclient(s)
            else:
                msg_queues[s].put(data)
                reponse_memory.append(data.decode())
                if s not in outputs:
                    outputs.append(s)

    for s in writable:
        if (len(outputs) == 0):
            break
        try:
            next_msg = msg_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            sendtoothers(s, next_msg)

    
    for s in exceptional:
        removeclient(s)

    #Checks if all bots have responded to last host-message
    if not host_is_passive and len(outputs) == 0:
        clients_finished += 1
        if clients_finished == len(client_list) and len(inputs) > 1:
            print('** Throwing out a new ice breaker **')
            broadcast_from_memory()
            clients_finished = 0
    
    #if a single bot is left alone the host comes to the rescue
    if len(inputs) == 2 and len(outputs) == 0: 
        broadcast("It's lonely isn't it? It's okay..you kan look at my butt")

    #If all connections is closed, the server terminates
    if (len(inputs) == 1 and len(outputs) == 0):
        print("\nServer shutting down in 3 seconds..")
        time.sleep(3)
        break
    
server.close()
print(f"{colors.WARNING}Server shutting down"+colors.ENDC)
quit()
