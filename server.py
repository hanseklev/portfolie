import socket
import time
import utils
from printcolors import colors
import select
import errno
import random
import queue

args = utils.getCommandLineArguments()

PORT = args[0]
IP = socket.gethostbyname(socket.gethostname()) #'192.168.0.6'
threads = 0 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((IP, PORT))
server.listen()
print(f"{colors.OKGREEN}Server is running on port {PORT}" + colors.ENDC)

inputs = [server]
outputs = []
msg_queues = {}
clientnames = []
HOST_ACTIONS = ['What should we talk about?', 'How are y\'all doing?', 'What are you thinking about today?']


def sendtoothers(conn, msg):
    name = utils.getnamefromconn(conn, clientnames)
    for c in clientnames:
         if c["conn"] is not conn:
            try:
                c["conn"].send(utils.addnametodata(name, msg))
            except socket.error as e:
                print('socket error: ', e)
            except IOError as e:
                if e.errno == errno.EPIPE:
                    print('PIPE error')
                print('Something went wrong..', e)        

def broadcast(msg, isinfo = False):
    msg_type = 'INFO' if isinfo else 'HOST' #Inform the client if it's a request or info from the host
    for c in inputs:
        if c is not server:
            c.send(utils.addnametodata(msg_type, msg))

def addclient(client, name):
    inputs.append(client)
    clientnames.append({'name': name, 'conn': client})
    msg_queues[client] = queue.Queue()         
    msg = str(f"{colors.OKBLUE}{name} joined the room"+colors.ENDC)       
    broadcast(msg.encode(), isinfo=True)
    print(msg)

def removeclient(conn):
    client = utils.getclientfromconn(conn, clientnames)
    name = client["name"]
    print(f"{name} logged off")
    inputs.remove(conn)
    del msg_queues[conn]
    clientnames.remove(client)
    conn.close()
    broadcast(str(f"{colors.WARNING}{name} logged off"+colors.ENDC).encode(), isinfo=True)



def gethostaction():
    return random.choice(HOST_ACTIONS)


print('Waiting for more users..')

while len(inputs) < 3:
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 5)
    
    for s in readable:
        if s is server:
            client, address = server.accept()
            client.setblocking(0)
            name = client.recv(1024).decode()
            addclient(client, name)
"""
print(f"{colors.WARNING}Let the chatting begin :-)"+colors.ENDC)
msg_queues[server].put(utils.addnametodata("INFO", "Let the chatting begin:)"))
if server not in outputs:
    outputs.append(server)
"""

print(f"{colors.WARNING}Let the chatting begin :-)"+colors.ENDC)

def add_host_suggestion():
    if server not in outputs:
        outputs.append(server)
        msg_queues[server].put(utils.addnametodata('HOST', gethostaction()))



while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:
        if s is server:
            client, address = server.accept()
            client.setblocking(0)
            name = client.recv(1024).decode()
            addclient(client, name)

        else:
            data = s.recv(1024)
            if not data:
                if s in outputs:
                    outputs.remove(s)
                removeclient(s)
            else:
                msg_queues[s].put(data)
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
    
    #msg_queues[server].put(random.choice(HOST_ACTIONS).encode())
    for s in exceptional:
        if s in outputs:
            outputs.remove(s)
        removeclient(s)
    
    #If all connections is closed, the server terminates
    if (len(inputs) == 1 and len(outputs) == 0):
        print('Server shutting down in 3 seconds..')
        time.sleep(3)
        break
    
server.close()
print(f'{colors.WARNING}Server shutting down'+colors.ENDC)
quit()
