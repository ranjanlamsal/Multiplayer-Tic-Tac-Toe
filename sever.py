import socket
import threading

game_board = { '1': '   ', '2': '   ', '3': '   ',
               '4': '   ', '5': '   ', '6': '   ',
               '7': '   ', '8': '   ', '9': '   '}

board_space = []
for key in game_board:
    board_space.append(key)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind the socket to a public host, and a well-known port
sock.bind((host, port))

# Listen for incoming connections
sock.listen(2)
print('Waiting for a connection...')

# Keep track of connected clients
clients = []


def printBoard(board):
    print('\t'+ board['1'] + '|' + board['2'] + '|' + board['3'])
    print('\t'+ '---+---+---')
    print('\t'+ board['4'] + '|' + board['5'] + '|' + board['6'])
    print('\t'+ '---+---+---')
    print('\t'+ board['7'] + '|' + board['8'] + '|' + board['9'])


def handle_client(conn, player):
    # wait for both clients to connect and select their game pieces
    if len(clients) < 2:
        conn.send("Waiting for another player to connect...".encode())
        return
    turn = ''
    while True:
        if player == 1:
            conn.send("Select your choice (O/X)?".encode())
        choice = conn.recv(1024).decode()
        if choice.capitalize() == 'X':
            turn = 'X'
            break
        elif choice.capitalize() == 'O':
            turn = 'O'
            break
        else:
            conn.send("Invalid input".encode())
            continue

    count = 0

    while True:
        printBoard(game_board)
        if player == 1:
            conn.send(f"It's your turn, Player( {turn} ). Move to which place?".encode())
        move = conn.recv(1024).decode()
        try:
            if game_board[move] == '   ':
                game_board[move] = f" {turn} "
                count += 1
            else:
                conn.send("That place is already filled.\nMove to which place?".encode())
                continue
        except:
            conn.send("Invalid input!!!!".encode())
            continue

        if count >= 5:
            if game_board['7'] == game_board['8'] == game_board['9'] != '   ':  # across the top
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break

            elif game_board['4'] == game_board['5'] == game_board['6'] != '   ':  # across the middle
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break

            elif game_board['1'] == game_board['2'] == game_board['3'] != '   ':  # across the bottom
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break

            elif game_board['1'] == game_board['4'] == game_board['7'] != '   ':  # down the left side
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break
            elif game_board['2'] == game_board['5'] == game_board['8'] != '   ':  # down the middle
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break
            elif game_board['3'] == game_board['6'] == game_board['9'] != '   ':  # down the right side
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break
            elif game_board['7'] == game_board['5'] == game_board['3'] != '   ': # diagonal
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break
            elif game_board['1'] == game_board['5'] == game_board['9'] != '   ': # diagonal
                printBoard(game_board)
                conn.send("\nGame Over.\n".encode())
                conn.send(f" **** {turn} won. ****".encode())
                break
            else:
                if count == 9:
                    conn.send("\nGame Over.\n".encode())
                    conn.send("It's a Tie!!".encode())
                    break

try:
    while True:
        # wait for a connection
        conn, addr = sock.accept()
        print(f'Connected by {addr}')
        
        # add the new client to the clients list
        clients.append(conn)
        
        # create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(conn, len(clients)))
        client_thread.start()

except KeyboardInterrupt:
    # catch keyboard interruption and close the socket
    print("Keyboard interrupt detected. Closing the port...")
    sock.close()