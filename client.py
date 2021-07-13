import pygame
# from network import Network
import pickle
import socket
pygame.init()

WIDTH = 1280
HEIGHT = 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        # self.server = "139.177.194.104"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print('Player ', self.p)  # 0 or 1

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):  # send data to server
        try:
            self.client.send(str.encode(data))
            # return self.client.recv(2048*2).decode()
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Finding opponent...", 1, (255, 0, 0), True)
        win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    else:
        print('Game is connected!')
        game.run()

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    got_game = False
    player = int(n.getP())  # 0 or 1
    print("You are player", player)

    while run:
        clock.tick(60)
        if not got_game:  # if it hasn't found an opponent yet
            try:
                game = n.send("get")
                print(game.connected())
                got_game = game.connected()  # bool
            except:
                run = False
                print("Couldn't get game")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()