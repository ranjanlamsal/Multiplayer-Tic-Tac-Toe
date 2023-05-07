import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False

        self.counter  = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()
        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_client, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_client, args=(client,)).start()
        
    def check_valid_move(self, move):
        if self.board[int(move[0])][int(move[1])] == " ":
            return True
        else:
            return False
    
    def handle_client(self, client):
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row, column): ")
                if self.check_valid_move(move.split(",")):
                    self.apply_move(move.split(","), self.you)
                    self.turn = self.opponent
                    client.send(move.encode("utf-8"))
                else:
                    print("Invalid move.")
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.apply_move(data.decode("utf-8").split(","), self.opponent)
                    self.turn = self.you
        client.close()

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player

        self.print_board()

        if self.check_win():
            if self.winner == self.you:
                print("You win!")
                exit()
            
            elif self.winner == self.opponent:
                print("You lose!")
                exit()
        else:
            if self.counter ==9:
                print("Tie game.")
                exit()

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                self.winner = self.board[i][0]
                self.game_over = True
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                self.winner = self.board[0][i]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False
    
    def print_board(self):
        for i in range(3):
            print(" | ".join(self.board[i]))
            if i != 2:
                print("----------")

game = TicTacToe()
game.host_game("localhost", 9999)
