# PYTHON CHATBOT APP
### Hans Erling Klevstad, s341872


## How to get things running:
1. Start the server by running the command `server.py -p [PORT]` 
2. Start up the desired clients. Options described below.
4. Let the chatting begin.
5. When in "human-mode", type `bye` to log out of the chat.
6. When all of the clients have logged off the server terminates itself

### BOT CLI-OPTIONS:
- Assign `IP` and `PORT` matching the server setup. When you run the server it will print the IP-address it is running on.
- For both human and bot clients you have to provide a name with the `-b` arg. If you name
the bot "Chuck" or "Cathy" they have some extra tricks up their sleeve. All other bots will fall back 
to the default bot-behaviour.
- You kan also specify the number of responses with `--limit` before the bot quit the chat, this defaults to a random number between 4 and 10
- By enabling `--freeforall` the given bot will respond to everything being said in the chat, use with care. Should also be used in combination with the `--ispassive` flag for the server.
- Give a client physical input input by enabling `--ishuman`. 

### SERVER CLI-OPTIONS:
- The argument `--conn` or `-c` specifies how many connections the server is waiting for, before opening up the chat. This defaults to 2. It is still possible to join after this.
- By providing the `--ispassive` for the server, the server-host does not initate nor participate in any conversations opening up for a more fluid conversation. Make sure to have the  bot `--freeforall` flag enabled, as they only listens to the host by default.




### BOT BEHAVIOUR:

Things to ask about and maybe get a decent answer:
- Movies
- Music
- Food
- Maybe cats


## Known issues
- When `--ishuman` is enabled, the first message is ignored for some reason, so in order to have the
`stdin` detect input, activate the input bye hitting `⏎ (return)`
- If two bots log off at the exact same time, the server doesn't always register both simultaneously, resulting in 
that it will try to send a message to a closed socket, and therefore crash.
- The server-host is not a particularly good host, and will mostly run his own race conversation-wise.

## Requirements
The only external package needed for this app which is the HTTP-library `requests`.