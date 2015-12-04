from socket import *

# Class to store colour escape codes. General idea from:
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
# Escape codes found at:
# http://ascii-table.com/ansi-escape-sequences.php

class colours:
    DEFAULT = '\033[40;37m' #Black background, White foreground
    TITLEBAR = '\033[44;37m' #Blue background, White foreground
    SYSTEMPROMPTS = '\033[40;36m' #Black background, Cyan foreground
    SERVERRESPONSES = '\033[40;35m' #Black background, Magenta foreground

print (colours.TITLEBAR + "Number Guessing Game V1.0")
print (colours.SYSTEMPROMPTS + "Connecting to server...\n")

# Set up the socket as an Internet facing streaming socket
clientsocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server on port 4000
try:
	clientsocket.connect(('localhost', 4000))
except ConnectionRefusedError:
	print ("The connection was refused.")
	exit(0)
print("connected!\n")
# Send the greeting message to the server, as specified by the requirements
message = "Hello\r\n"
clientsocket.send(message.encode('ascii'))
# Wait for a response, then print said response to the console
response = clientsocket.recv(1024)
print(response.decode('ascii'))

running = 1

while running:
	# Ask for user to guess a number
	guess = input(colours.SYSTEMPROMPTS + "Enter your guess: ")
	# Format the guess, ready to send to the server
	guessstring = "Guess: " + str(guess) + "\r\n"
	# Send the guess
	clientsocket.send(guessstring.encode('ascii'))

	# Wait for the response from the server
	response = clientsocket.recv(1024).decode('ascii')
	print (colours.SERVERRESPONSES + response)

	# Determine if the game is over
	if (response == "Correct\r\n"):
		running = 0

clientsocket.close()
# Reset the colours
print(colours.DEFAULT)
