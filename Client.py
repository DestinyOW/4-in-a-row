import socket
from matplotlib.pyplot import close
import pygame


pygame.init()
pygame.display.set_caption("4 In a Row")

SCR_WIDTH = 1000
SCR_HEIGHT = 1000
BOARD_COLS = 7
BOARD_ROWS = 6
BACKGROUND_COLOR = (229,252,194)
RECT_WIDTH = 10
CIRCLE_WIDTH = 10
CANVAS_LEFT_OFFSET = 300
CANVAS_UP_OFFSET = 300
CANVAS_WIDTH = SCR_WIDTH - CANVAS_LEFT_OFFSET
CANVAS_HEIGHT = SCR_HEIGHT - CANVAS_UP_OFFSET

def GetAppScreen():
    screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
    screen.fill(BACKGROUND_COLOR)

    pygame.display.flip()
    return screen


def DrawBoard(screen):
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT)).convert()
    canvas.fill((255, 255, 255))
    
    rect_space = (CANVAS_WIDTH - RECT_WIDTH * (BOARD_COLS + 1)) / BOARD_COLS

    for x in range(BOARD_COLS + 1):
        rectangle = pygame.Rect(x * (rect_space + RECT_WIDTH), 0, RECT_WIDTH, CANVAS_HEIGHT)
        pygame.draw.rect(canvas, (0, 0, 0), rectangle)
    
    rect_space = (CANVAS_HEIGHT - RECT_WIDTH * (BOARD_ROWS +1)) / BOARD_ROWS

    for y in range(BOARD_ROWS + 1):
        rectangle = pygame.Rect(0, y * (rect_space + RECT_WIDTH), CANVAS_WIDTH, RECT_WIDTH)
        pygame.draw.rect(canvas, (0, 0, 0), rectangle)
    
    screen.blit(canvas , (CANVAS_LEFT_OFFSET / 2, CANVAS_UP_OFFSET / 2))
    pygame.display.flip()


def AddToCanvas(screen, col, row, color):
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT)).convert()
    canvas.fill((255, 255, 255))

    rect_space_x = (CANVAS_WIDTH - RECT_WIDTH * (BOARD_COLS + 1)) / BOARD_COLS
    rect_space_y = (CANVAS_HEIGHT - RECT_WIDTH * (BOARD_ROWS +1)) / BOARD_ROWS
    radius = rect_space_x / 2
    
    print(canvas, color, (rect_space_x * col + radius, rect_space_y * row + radius), radius, CIRCLE_WIDTH)
    pygame.draw.circle(canvas, color, (rect_space_x * col + radius, rect_space_y * row + radius), radius, CIRCLE_WIDTH)

    screen.blit(canvas , (CANVAS_LEFT_OFFSET / 2, CANVAS_UP_OFFSET / 2))
    pygame.display.flip()


def CloseGame(soc):
    pygame.quit()
    soc.close()
    quit()


def OnClick(screen, event, soc, color):
    mouse_x = event.pos[0]
    mouse_y = event.pos[1]

    rect_space = (CANVAS_WIDTH - RECT_WIDTH * (BOARD_COLS + 1)) / BOARD_COLS

    for x in range(BOARD_COLS -1):
        col_start = x * (rect_space + RECT_WIDTH) + CANVAS_LEFT_OFFSET / 2

        if col_start  < mouse_x < col_start + RECT_WIDTH:    
            soc.send(str(x).encode())
            print("SENDING", x)
            result = soc.recv(1024).decode()
            print("Got", result)
            
            if result == "FALSE":
                return True
            elif result in ("WIN", "LOSE", "TIE"):
                pass
            else:
                AddToCanvas(screen, x, int(result), color)
                return False


def main():
    screen = GetAppScreen()
    DrawBoard(screen)

    ip = '127.0.0.1'
    port = 42069
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((ip,port))
    
    my_turn = soc.recv(1024).decode() == "1"
    if my_turn:
        my_color = (255, 0, 0)
    else:
        my_color = (0, 0, 255)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CloseGame(soc)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   my_turn = OnClick(screen, event, soc, my_color)


if __name__ == '__main__':
    main()