import random
from socket import *
import threading

# Set up the socket

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('localhost', 4000))
serversocket.listen(5)

# Function definitions

def handleclient(clientsocket, clientaddress):
	# Receive the client's greeting
	clientgreeting = clientsocket.recv(1024)
	# Send the welcome message to the client
	welcomemessage = "Greetings\r\n"
	clientsocket.send(welcomemessage.encode('ascii'))

	running = 1
	numberofguesses = 0
	# Generate a random number for the client to try and guess
	numbertoguess = generatenumber()
	# Main loop
	while running:
		guess = clientsocket.recv(1024)
		guessstring = guess.decode('ascii')
		print(guessstring)
		# Split the guess string up to get the integer guessed
		guess = int(guessstring.split()[1])
		# Incremenent the counter of the number of guesses
		numberofguesses += 1
		running = 1
		# If the player has guessed correctly
		if (guess == numbertoguess):
			messagetosend = ("Correct\r\n")
			clientsocket.send(messagetosend.encode('ascii'))
			running = 0
		else:
			# Calculate how far the player was away from the actual number
			difference = abs(guess - numbertoguess)
			if difference < 2:
				messagetosend = ("Close\r\n")
			else:
				messagetosend = ("Far\r\n")
			# Send the response to the player
			clientsocket.send(messagetosend.encode('ascii'))
	# Close the connection
	clientsocket.close()
	print("Connection closed.")

def generatenumber():
	return random.randrange(1, 20)

# Main server loop

while 1:
	(clientsocket, clientaddress) = serversocket.accept()
	print("Connection received from: ", clientaddress)
	threading.Thread(target = handleclient, args =  (clientsocket, clientaddress)).start()
	print("Connection passed to new thread. Returning to listening.")
