from socket import *

print ("Number Guessing Game Admin Client V1.0\n\n")
print ("Connecting to server...\n")

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

print("Connected Clients: ")
message = "Who\r\n"
adminsocket.send(message.encode('ascii'))

response = adminsocket.recv(1024)
print(response.decode('ascii'))
