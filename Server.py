import socket


class Board:
    def __init__(self):
        self.board = [[0]*7 for _ in range(6)]  

    def GetBoardData(self):
        boardstring = ""

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                boardstring += str(self.board[row][column]) + ' '
            boardstring += '\n'
        
        return boardstring
    
    def AddToBoard(self,player,column):
        if column < 0 or column >= 7:
            return -1
        for row in range(len(self.board)-1, -1 , -1):
            if self.board[row][column] == 0:
                self.board[row][column] = player
                return row
        return -1

    def CheckIfWin(self):
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] == row[i+1] == row[i+2] == row[i+3] != 0:
                    return row[i] 

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

class Player:
    def __init__(self, addr, conn, ID):
        self.addr = addr
        self.conn = conn
        self.ID = ID

class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.turn = 1
        self.port = 42069
        self.ip = '127.0.0.1'
        self.board = Board()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((self.ip,self.port))
    
    def ConnectPlayers(self):
        self.soc.listen(2)
        conn1, addr1 = self.soc.accept()
        conn2, addr2 = self.soc.accept()

        self.player1 = Player(addr1, conn1, 1)
        self.player2 = Player(addr2, conn2, 2)

        self.player1.conn.send(str(self.player1.ID).encode())
        self.player2.conn.send(str(self.player2.ID).encode())


    def GameLoop(self):
        while self.board.CheckIfWin() == 0 and '0' in self.board.GetBoardData():
            if self.turn == self.player1.ID:
                data = int(self.player1.conn.recv(1024).decode())
                row = self.board.AddToBoard(self.player1.ID, data)

                while row == -1:
                    self.player1.conn.sendall("FALSE".encode())
                    data = int(self.player1.conn.recv(1024).decode())
                    row = self.board.AddToBoard(self.player1.ID, data)
            else:
                data = int(self.player2.conn.recv(1024).decode())
                row = self.board.AddToBoard(self.player2.ID, data)
                
                while row == -1:
                    self.player2.conn.sendall("FALSE".encode())
                    data = int(self.player2.conn.recv(1024).decode())
                    row = self.board.AddToBoard(self.player2.ID, data)
                
            if self.board.CheckIfWin() == 0 and '0' in self.board.GetBoardData():
                self.player1.conn.sendall(str(row).encode())
                self.player2.conn.sendall(str(row).encode())
                self.turn = self.player1.ID + self.player2.ID - self.turn
        
        if self.board.checkifwin() == 1: 
            self.player1.conn.sendall("WIN".encode())
            self.player2.conn.sendall("LOSE".encode())
        elif self.board.checkifwin() == 2: 
            self.player1.conn.sendall("LOSE".encode())
            self.player2.conn.sendall("WIN".encode())
        else:
            self.player1.conn.sendall("TIE".encode())
            self.player2.conn.sendall("TIE".encode())


def main():
    game = Game()
    game.ConnectPlayers()
    game.GameLoop()

if __name__ == '__main__':
    main()
