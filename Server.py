import socket

class Board:
    def __init__(self):
        self.board = [[0]*7 for x in range(6)]  

    def getboarddata(self):
        boardstring = ""
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                boardstring += str(self.board[row][column]) + ' '
            boardstring += '\n'
        return  boardstring
    
    def addtoboard(self,player,column):
        if 0 > column or column>=7:
            return False
        for row in range(len(self.board)-1, -1 , -1):
            if self.board[row][column] == 0:
                self.board[row][column] = player
                return True 
        return False

    def checkifwin(self):
        winner = 0
        for row in self.board:
            for i in range(len(row)-3):
                if row[i] == row[i+1] == row[i+2] == row[i+3] != 0:
                    return row[i] 
                    
        for col in zip(*self.board):
            for i in range(len(col)-3):
                if col[i] == col[i+1] == col[i+2] == col[i+3] != 0:
                    return col[i] 

        for row in range(len(self.board)-3):
            for col in range(row-3):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != 0:
                    return self.board[row][col]

        for row in range(len(self.board)-3, len(self.board)):
            for col in range(row-3):
                if self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3] != 0:
                    return self.board[row][col]
        return 0

class Player:
    def __init__(self,addr, conn, ID):
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
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = Board()
        self.soc.bind((self.ip,self.port))
    
    def StartGame(self):
        self.soc.listen(2)
        conn1, addr1 = self.soc.accept()
        conn2, addr2 = self.soc.accept()

        self.player1 = Player(addr1, conn1, 1)
        self.player2 = Player(addr2, conn2, 2)

        self.player1.conn.send(str(self.player1.ID).encode())
        self.player2.conn.send(str(self.player2.ID).encode())

        self.GameLoop()

    def GameLoop(self):
        while self.board.checkifwin() == 0 and '0' in self.board.getboarddata():
            if self.turn == self.player1.ID:
                data = int(self.player1.conn.recv(1024).decode())
                if not self.board.addtoboard(self.player1.ID, data):
                    self.player1.conn.sendall("FALSE".encode())
                    continue
            
            else:
                data = int(self.player2.conn.recv(1024).decode())
                if not self.board.addtoboard(self.player2.ID, data):
                    self.player2.conn.sendall("FALSE".encode())
                    continue
                
            if self.board.checkifwin() == 0 and '0' in self.board.getboarddata():
                self.player1.conn.sendall(self.board.getboarddata().encode())
                self.player2.conn.sendall(self.board.getboarddata().encode())
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
    game.StartGame()


if __name__ == '__main__':
    main()
