import socket
#import pygame

#pygame.init()

#SCR_WIDTH = 1000
#SCR_HEIGHT = 1000

#screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
#pygame.display.set_caption("4 In a Row")
#screen.fill((229,252,194))
#pygame.display.flip()


def main():
    ip = '127.0.0.1'
    port = 42069
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((ip,port))
    ID = soc.recv(1024).decode()
    if ID == "1": 
        data = input("Enter a move: \n")
        soc.sendall(data.encode())
        board = soc.recv(1024).decode()
        print(board)
    while True:
        board = soc.recv(1024).decode()
        if board == "WIN":
            print("you win!")
            soc.close()
            break
        elif board == "LOSE":
            print("you lose!")
            soc.close()
            break
        elif board == "TIE":
            print("TIE!")
            soc.close()
            break
        print(board)
        board = "FALSE"
        while board == "FALSE":
        
            data = input("Enter a move: \n")
            soc.sendall(data.encode())
            board = soc.recv(1024).decode()
        
        if board == "WIN":
            print("you win!")
            soc.close()
            break
        elif board == "LOSE":
            print("you lose!")
            soc.close()
            break
        elif board == "TIE":
            print("TIE!")
            soc.close()
            break
        print(board)
        







if __name__ == '__main__':
    main()