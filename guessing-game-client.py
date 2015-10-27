from socket import *

print ("Number Guessing Game V1.0\n\n")
print ("Connecting to server...\n")

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
	guess = input("\nEnter your guess: ")
	# Format the guess, ready to send to the server
	guessstring = "Guess: " + str(guess)
	# Send the guess
	clientsocket.send(guessstring.encode('ascii'))

	# Wait for the response from the server
	response = clientsocket.recv(1024).decode('ascii')
	print (response)

	# Determine if the game is over
	if (response == "Correct"):
		running = 0

clientsocket.close()
