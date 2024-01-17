import socket
import threading
from tkinter import Tk, Button, messagebox

class TicTacToe:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False

        self.counter = 0

        self.root = Tk()
        self.root.title("Tic Tac Toe")

        self.buttons = [[None, None, None] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = Button(self.root, text="", font=('normal', 20), width=5, height=2,
                                            command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponent = 'X'
        threading.Thread(target=self.handle_connection, args=(client,)).start()

        self.root.mainloop()

    def make_move(self, row, col):
        if not self.game_over and self.turn == self.you and self.check_valid_move([row, col]):
            move = f"{row},{col}"
            self.apply_move(move.split(","), self.you)
            self.turn = self.opponent
            self.update_buttons()
            self.client.send(move.encode('utf-8'))

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.board[i][j]

    def handle_connection(self, client):
        self.client = client
        while not self.game_over:
            if self.turn == self.you:
                pass  # The move is handled in the make_move function
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
                    self.update_buttons()

        client.close()

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.check_if_won()
        if self.winner == self.you:
            messagebox.showinfo("Game Over", "You win!")
            self.root.quit()
        elif self.winner == self.opponent:
            messagebox.showinfo("Game Over", "You lose!")
            self.root.quit()
        else:
            if self.counter == 9:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.root.quit()

    def check_valid_move(self, move):
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
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


game = TicTacToe()
game.connect_to_game('localhost', 12345)
