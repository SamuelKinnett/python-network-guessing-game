import random
from socket import *
from select import *

# Set up the socket

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('localhost', 4000))
serversocket.listen(5)

# Set up the socket list
activesockets = []

# This stores a dictionary of the currently connected ip addresses
connectedips = {}
connectedips[serversocket] = -1

# Add the server socket to the list of active sockets
activesockets.append(serversocket)

# Initialise a dictionary storing the number to guess for each client
numberdictionary = {}
numberdictionary[serversocket] = -1

# Function definitions

def handleclient(clientsocket):
    # Read the message from the client
    clientmessage = clientsocket.recv(1024).decode('ascii')

    if (clientmessage == 'Hello\r\n'):
        # A new client has connected!
        # Send the welcome message to the client
        welcomemessage = "Greetings\r\n"
        clientsocket.send(welcomemessage.encode('ascii'))

        # Now let's generate a number for the client
        numbertoguess = generatenumber()
        # Then add it to the dictionary
        numberdictionary[clientsocket] = numbertoguess
    else:
        # The client has sent a guess
        # Split the guess string up to get the integer guessed
        guess = int(clientmessage.split()[1])
		
        # If the player has guessed correctly
        if (guess == numberdictionary[clientsocket]):
            messagetosend = ("Correct\r\n")
            clientsocket.send(messagetosend.encode('ascii'))
			
            # Remove the socket from the active socket list
            activesockets.remove(clientsocket)
            del numberdictionary[clientsocket]
            del connectedips[clientsocket]
            clientsocket.close()
        else:
            # Calculate how far the player was away from the actual number
            difference = abs(guess - numberdictionary[clientsocket])
            if difference < 2:
                messagetosend = ("Close\r\n")
            else:
                messagetosend = ("Far\r\n")
            # Send the response to the player
            clientsocket.send(messagetosend.encode('ascii'))

def generatenumber():
    return random.randrange(1, 10)

# Main server loop

while 1:
    # Scan for activity on the sockets
    (input, output, error) = select(activesockets, [], [])
    print(activesockets)
    # Handle inputs
    for currentsocket in input:
        if (currentsocket == serversocket):
            (clientsocket, clientaddress) = serversocket.accept()
            activesockets.append(clientsocket)
            connectedips[clientsocket] = clientaddress
            print("Connection received from: ", clientaddress)
        else:
            handleclient(currentsocket)
