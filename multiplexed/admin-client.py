from socket import *
import os

# Class to store colour escape codes. General idea from:
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
# Escape codes found at:
# http://ascii-table.com/ansi-escape-sequences.php

class colours:
    if (os.name != 'nt'):
        # If we're not on Winblows, enable colours
        DEFAULT = '\033[40;37m' #Black background, White foreground
        TITLEBAR = '\033[44;37m' #Blue background, White foreground
        SOCKETDATA = '\033[40;36m' #Black background, Cyan foreground
        SYSTEMPROMPTS = '\033[40;35m' #Black background, Magenta foreground
    else:
        DEFAULT = ''
        TITLEBAR = ''
        SOCKETDATA = ''
        SYSTEMPROMPTS = ''

# Cross platform function to clear the console. Implemented from:
# http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console

def clearscreen():
    # Cross platform method to clear the console. Calls the OS' clear method:
    # 'cls' if on windows, otherwise 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

clearscreen();
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

message = "Who\r\n"
adminsocket.send(message.encode('ascii'))

response = adminsocket.recv(1024).decode('ascii')
connectedusers = response.split('\r\n')
# Remove the extra empty element
del connectedusers[-1]

print ("Users online: " + str(len(connectedusers)))

print ("┌───────────────┬──────┐")
print ("│  IP Address   │ Port │")
print ("├───────────────┼──────┤")

for user in connectedusers:
    ippadding = 15 - len(user.split()[0])
    ippaddingstring = ""
    for i in range (0, ippadding):
        ippaddingstring += " "
    portpadding = 6 - len(user.split()[1])
    portpaddingstring = ""
    for i in range (0, portpadding):
        portpaddingstring += " "

    print(colours.SYSTEMPROMPTS + "│" + 
            colours.SOCKETDATA + user.split()[0] + ippaddingstring + 
            colours.SYSTEMPROMPTS +  "│" + 
            colours.SOCKETDATA + user.split()[1] + portpaddingstring +
            colours.SYSTEMPROMPTS +  "│")

print ("└───────────────┴──────┘")
print (colours.DEFAULT)
# Add a pause for when the program is run on windows
input()
