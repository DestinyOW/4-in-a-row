import socket


class Board:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]

    def GetBoardData(self):
        boardstring = ""

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                boardstring += str(self.board[row][column]) + ' '
            boardstring += '\n'
        
        return boardstring

    def AddToBoard(self, id, col):
        if not 0 <= col < 7:
            return -1

        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = id
                return row

        return -1

    def CheckIfWin(self):
        # vertical win
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] == row[i+1] == row[i+2] == row[i+3] != 0:
                    return row[i]

        # horizontal win
        for col in zip(*self.board):
            for i in range(len(col) - 3):
                if col[i] == col[i+1] == col[i+2] == col[i+3] != 0:
                    return col[i]

        for row in range(len(self.board) - 3):
            for col in range(row - 3):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != 0:
                    return self.board[row][col]

        for row in range(len(self.board) - 3, len(self.board)):
            for col in range(row - 3):
                if self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3] != 0:
                    return self.board[row][col]

        return 0


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((self.ip, self.port))

        self.board = Board()
        self.first_player_turn = True

    def ConnectPlayers(self):
        self.soc.listen(2)

        self.player1 = self.soc.accept()[0]
        self.player2 = self.soc.accept()[0]

        self.player1.send('1'.encode())
        self.player2.send('2'.encode())

    def GameLoop(self):
        while True:
            if self.first_player_turn:
                col = int(self.player1.recv(1024).decode())
                print("Got from player1", col)
                row = self.board.AddToBoard(1, col)

                while row == -1:
                    self.player1.send('-1'.encode())
                    print("Sending player1", -1)
                    col = int(self.player1.recv(1024).decode())
                    print("Got from player1", col)
                    row = self.board.AddToBoard(1, col)

                self.player1.send(str(row).encode())
                print("Sending player1", row)

                win = self.board.CheckIfWin()
                if win != 0:
                    self.player1.send(('-2,' + str(win)).encode())
                    self.player2.send(('-2,' + str(win)).encode())
                    quit()
                else:
                    self.player2.send((str(col) + ',' + str(row)).encode())
                    print('Sending player2', (str(col) + ',' + str(row)))
            else:
                col = int(self.player2.recv(1024).decode())
                row = self.board.AddToBoard(2, col)

                while row == -1:
                    self.player2.send('-1'.encode())
                    col = int(self.player2.recv(1024).decode())
                    row = self.board.AddToBoard(2, col)

                
                self.player2.send(str(row).encode())
                print("Sending player2", row)

                win = self.board.CheckIfWin()
                if win != 0:
                    self.player1.send(('-2,' + str(win)).encode())
                    self.player2.send(('-2,' + str(win)).encode())
                else:
                    self.player1.send((str(col) + ',' + str(row)).encode())  
            
            self.first_player_turn = not self.first_player_turn
            print(self.board.GetBoardData())


def main():
    server = Server('127.0.0.1', 42069)
    server.ConnectPlayers()
    server.GameLoop()

if __name__ == '__main__':
    main()
