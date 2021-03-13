import argparse


#Function that handles CLI args input for both server and client connection
def getCommandLineArguments(isclient = False):
    ipaddress = ''
    botname = ''
    ishuman = False
    parser = argparse.ArgumentParser()
    parser.add_argument("--port" , "-p", type=int, help="Assign a port")

    if isclient: #add additional arguments for client CLI
        parser.add_argument("--ipaddress" , "-ip",  help="Assign a IP address")
        parser.add_argument("--bot" , "-b",  help="Assign a bot name")
        parser.add_argument("--ishuman", action="store_true", help="Enable this if you want to chat with the bots")

    args = parser.parse_args()
    port = args.port

    if isclient:
        ipaddress = args.ipaddress
        botname = args.bot
        ishuman = args.ishuman

    if (port == None):
        print('You have to provide a port number using the argument -p [PORT] or --port [PORT]')
        exit(2)
    if (isclient and ipaddress == None):
        print('You have to provide a ip-address using the argument -ip [ADDRESS] or --ipaddress [ADDRESS]')
        exit(2)
    if (isclient and botname == None):
        print('You have to assign a bot using the argument -b [NAME] or --bot [NAME]')
        exit(2)

    port = int(port)
    if (isclient):
        return [port, ipaddress, botname, ishuman]

    return [port]

def getclientfromconn(conn, clients):
    for c in clients:
        if c["conn"] is conn:
            return c

def getnamefromconn(conn, clients):
    for c in clients:
        if c["conn"] is conn:
            return c["name"]

def deleteclient(conn, clients):
    for c in clients:
        if c["conn"] is conn:
            print('match')
            clients.remove(c)
            break

DELIMITER = '#$%'

def addnametodata(name ,msg):
    try:
        msg = msg.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    return str(name+DELIMITER+msg).encode()

def parsedata(msg):
    strmsg = msg
    try:
        strmsg = msg.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    msg_arr = str(strmsg).split(DELIMITER)
    return msg_arr

