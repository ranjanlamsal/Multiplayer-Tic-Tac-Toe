import socket

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# set the port number to match the server's port
port = 9999

# connect the socket to the server's IP address and port
sock.connect((host, port))

# receive the initial message from the server
message = sock.recv(1024).decode()
print(message)

# send a message to the server to choose X or O
choice = input()
sock.send(choice.encode())

# loop to play the game
while True:
    # receive the game board from the server and print it
    board = sock.recv(1024).decode()
    print(board)

    # check if the game is over
    if "Game Over." in board:
        break

    # if it's the player's turn, ask for their move and send it to the server
    if "your turn" in board:
        move = input()
        sock.send(move.encode())

# receive the final message from the server and print it
message = sock.recv(1024).decode()
print(message)

# close the socket
sock.close()
