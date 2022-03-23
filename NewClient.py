import socket
import pygame

pygame.init()
pygame.display.set_caption("4 In a Row")


COLORS = {
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "BACKGROUND": (220, 255, 190)
}


class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ConnectToServer(self):
        self.soc.connect((self.ip, self.port))

        self.id = self.soc.recv(1024).decode()

        if self.id == "1":
            self.my_color = COLORS['RED']
            self.enemy_color = COLORS['BLUE']
        else:
            self.my_color = COLORS['BLUE']
            self.enemy_color = COLORS['RED']

    def SendMove(self, col):
        self.soc.send(str(col).encode())
        row = self.soc.recv(1024).decode()
        
        return int(row) 
    
    def GetMove(self):
        data = self.soc.recv(1024).decode()
        
        return map(int, data.split(','))
         
    def Close(self):
        self.soc.close()


class GameScreen:
    def __init__(self, width, height, cols, rows):
        # screen
        self.screen_width = width
        self.screen_height = height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(COLORS['BACKGROUND'])
        pygame.display.flip()

        # board
        self.cols = cols
        self.rows = rows

        self.line_width = 10
        self.square_width = 80
        self.square_height = 80

        # canvas
        self.canvas_width = self.square_width * \
            self.cols + self.line_width * (self.cols + 1)
        self.canvas_height = self.square_height * \
            self.rows + self.line_width * (self.rows + 1)

        self.canvas_offset_left = (self.screen_width - self.canvas_width) / 2
        self.canvas_offset_top = (self.screen_height - self.canvas_height) / 2

        self.canvas = pygame.Surface(
            (self.canvas_width, self.canvas_height)).convert()

    def DrawBoard(self):
        self.canvas.fill(COLORS['WHITE'])

        # draw vertical lines
        for x in range(self.cols + 1):
            rectangle = pygame.Rect(
                x * (self.square_width + self.line_width), 0, self.line_width, self.canvas_height)
            pygame.draw.rect(self.canvas, COLORS['BLACK'], rectangle)

        # draw horizontal lines
        for y in range(self.rows + 1):
            rectangle = pygame.Rect(
                0, y * (self.square_height + self.line_width), self.canvas_width, self.line_width)
            pygame.draw.rect(self.canvas, COLORS['BLACK'], rectangle)

        # update screen
        self.screen.blit(
            self.canvas, (self.canvas_offset_left, self.canvas_offset_top))
        pygame.display.flip()

    def DrawPiece(self, piece_col, piece_row, color):
        radius = int(self.square_width / 2)

        # circle's coordinates
        circle_x = radius + self.line_width + piece_col * \
            int((self.square_width + self.line_width))
        circle_y = radius + self.line_width + piece_row * \
            int((self.square_height + self.line_width))

        pygame.draw.circle(self.canvas, color,
                           (circle_x, circle_y), radius - 2, 0)

        # update screen
        self.screen.blit(
            self.canvas, (self.canvas_offset_left, self.canvas_offset_top))
        pygame.display.flip()

    def PixelsToCol(self, event):
        # mouse coodinates
        mouse_x = event.pos[0]
        mouse_y = event.pos[1]

        if self.canvas_offset_top < mouse_y < self.screen_height - self.canvas_offset_top:
            for x in range(self.cols + 1):
                start_point = self.line_width + x * \
                    (self.square_width + self.line_width) + \
                    self.canvas_offset_left

                if start_point < mouse_x < start_point + self.square_width:
                    return x

        return -1


def main():
    screen = GameScreen(1000, 1000, 7, 6)
    screen.DrawBoard()

    client = Client('127.0.0.1', 42069)
    client.ConnectToServer()
    print(client.id)
    if client.id == "2":
        col, row = client.GetMove()
        screen.DrawPiece(col, row, client.enemy_color)
        print("first move")

    print("STARTED WHILE LOOP")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.Close()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("GOT CLICK")
                col = screen.PixelsToCol(event)
                if col != -1:
                    row = client.SendMove(col)
                    print("SENDING",col)
                    if row != -1:
                        screen.DrawPiece(col, row, client.my_color)
                        col, row = client.GetMove()
                        if col == -2:
                            if row == 0:
                                print("TIE")
                            elif row == int(client.id):
                                print("YOU WIN")
                            else:
                                print("YOU LOSE")
                            client.Close()
                            pygame.quit()
                            quit()
                        else:
                            print("GOT",col,row)
                            screen.DrawPiece(col, row, client.enemy_color)


if __name__ == '__main__':
    main()
