import random
from socket import *
from select import *
import ssl

# Set up the sockets

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('localhost', 4000))
serversocket.listen(5)

adminsocket = socket(AF_INET, SOCK_STREAM)
adminsocket.bind(('localhost', 4001))
adminsocket.listen(5)

# Set up the socket list
activesockets = []
activeadminsockets = []

# Add the serversocket and adminsocket to the active sockets
activesockets.append(serversocket)
activesockets.append(adminsocket)

# Initialise a dictionary storing the number to guess for each client
numberdictionary = {}

# Function definitions

def handleclient(clientsocket):
    # Read the message from the client
    clientmessage = clientsocket.recv(1024).decode('ascii')

    if (clientsocket in activeadminsockets):
        if (clientmessage == 'Hello\r\n'):
            # A new admin has connected!"
            # Send the welcome message to the admin
            welcomemessage = "Admin-Greetings\r\n"
            clientsocket.send(welcomemessage.encode('ascii'))
        elif (clientmessage == "Who\r\n"):
            # The admin wants a list of all currently connected ips
            connectedlist = ""
            for currentsocket in activesockets:
                if (currentsocket != serversocket and currentsocket != adminsocket):
                    connectedlist += str(currentsocket.getpeername()[0]) + " " + str(currentsocket.getpeername()[1]) + "\r\n"

            # Send the completed list
            clientsocket.send(connectedlist.encode('ascii'))
            # Since the admin client has now already sent the only command
            # it can, disconnect it.
            activesockets.remove(clientsocket)
            activeadminsockets.remove(clientsocket)
    else:
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
    return random.randrange(1, 20)

# Main server loop

while 1:
    # Scan for activity on the sockets
    (input, output, error) = select(activesockets, [], [])
    
    # Handle inputs
    for currentsocket in input:
        if (currentsocket == serversocket):
            (clientsocket, clientaddress) = serversocket.accept()
            activesockets.append(clientsocket)
            # print("Connection received from: ", clientaddress)
        elif (currentsocket == adminsocket):
            (newadminsocket, newadminsocketaddress) = adminsocket.accept()
            secureadmin = ssl.wrap_socket(newadminsocket,
                    certfile = "5cc515_server.crt",
                    keyfile = "5cc515_server.key",
                    server_side = True,
                    cert_reqs = ssl.CERT_REQUIRED,
                    ca_certs="5cc515-root-ca.crt")
            activesockets.append(secureadmin)
            activeadminsockets.append(secureadmin)
            # print("Admin connected from: ", newadminsocketaddress)
        else:    
            try:
                handleclient(currentsocket)
            except socket.error:
                # We've lost connection to the client mid-process
                print ("Lost connection to " + currentsocket.getpeename())
                activesockets.remove(currentsocket)
                if clientsocket in numberdictionary:
                    del numberdictionary[clientsocket]
                if clientsocket in activeadminsockets:
                    activeadminsockets.remove(currentsocket)
