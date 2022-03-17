import socket
import pygame

pygame.init()

SCR_WIDTH = 1000
SCR_HEIGHT = 1000
BOARD_COLS = 7
BOARD_ROWS = 6

screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))

pygame.display.set_caption("4 In a Row")
screen.fill((229,252,194))
pygame.display.flip()

def DrawBoard(screen):
    rect_width = 10
    canvas_left_offset = 300
    canvas_right_offset = 300

    canvas_width = SCR_WIDTH - canvas_left_offset
    canvas_height = SCR_HEIGHT - canvas_right_offset

    canvas = pygame.Surface((canvas_width, canvas_height)).convert()
    canvas.fill((255, 255, 255))
    
    rect_space = (canvas_width - rect_width * (BOARD_COLS + 1)) / BOARD_COLS

    for x in range(BOARD_COLS + 1):
        rectangle = pygame.Rect(x * (rect_space + rect_width), 0, rect_width, canvas_height)
        pygame.draw.rect(canvas, (0, 0, 0), rectangle)
    
    rect_space = (canvas_height - rect_width * (BOARD_ROWS +1)) / BOARD_ROWS

    for y in range(BOARD_ROWS + 1):
        rectangle = pygame.Rect(0, y * (rect_space + rect_width), canvas_width, rect_width)
        pygame.draw.rect(canvas, (0, 0, 0), rectangle)
    
    screen.blit(canvas , (canvas_left_offset / 2, canvas_right_offset / 2))
    pygame.display.flip()

def main():
    DrawBoard(screen , None)
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