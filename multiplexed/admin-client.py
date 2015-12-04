from socket import *

class colours:
    DEFAULT = '\033[40;37m' # Black background, White foreground
    TITLEBAR = '\033[44;37m' # Blue background, White foreground
    SYSTEMPROMPTS = '\033[40;35m' # Black background, Magenta foreground
    SOCKETDATA = '\033[40;36m' # Black background, Cyan foreground

print (colours.TITLEBAR + "Number Guessing Game Admin Client V1.0")
print (colours.SYSTEMPROMPTS + "Connecting to server...\n")

# Set up the socket as an Internet facing streaming socket
adminsocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server on port 4001
try:
    adminsocket.connect(('localhost', 4001))
except ConnectionRefusedError:
    print ("The connection was refused.")
    exit(0)
print("connected!\n")
# Send the greeting message to the server
message = "Hello\r\n"
adminsocket.send(message.encode('ascii'))
# Wait for a response, then print said response to the console
response = adminsocket.recv(1024)
print(response.decode('ascii'))

print ("┌────────────────────┐")
print ("│ Connected Clients: │")
print ("├────────────────────┤")

message = "Who\r\n"
adminsocket.send(message.encode('ascii'))

response = adminsocket.recv(1024).decode('ascii')
connectedusers = response.split('\r\n')

for user in connectedusers:
    padding = 19 - len(user)
    paddingstring = ""
    for i in range (0, padding):
        paddingstring += " "
    print(colours.SYSTEMPROMPTS + "│ " + colours.SOCKETDATA +  user + paddingstring + colours.SYSTEMPROMPTS +  "│")

print ("└────────────────────┘")
print (colours.DEFAULT)
