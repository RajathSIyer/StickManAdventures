import pygame
import random
import socket
# from network import Network
import pickle
from typing import *
import PIL

pygame.init()

BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720
FONT = pygame.font.SysFont("comicsans", 100)

NUM_TO_IMAGE = {0: pygame.image.load('standing.png'),
                1: pygame.image.load('moving.png')}
LETTER_TO_PYGAME = {'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c,
                    'd': pygame.K_d,
                    'e': pygame.K_e, 'f': pygame.K_f, 'g': pygame.K_g,
                    'h': pygame.K_h, 'i': pygame.K_i,
                    'j': pygame.K_j, 'k': pygame.K_k, 'l': pygame.K_l,
                    'm': pygame.K_m, 'n': pygame.K_n,
                    'o': pygame.K_o, 'p': pygame.K_p, 'q': pygame.K_q,
                    'r': pygame.K_r, 's': pygame.K_s,
                    't': pygame.K_t, 'u': pygame.K_u, 'v': pygame.K_v,
                    'w': pygame.K_w, 'x': pygame.K_x,
                    'y': pygame.K_y, 'z': pygame.K_z}
ALPHA_LST = list('abcdefghijklmnopqrstuvwxyz')


class Network2:
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
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)


class Stickman:
    def __init__(self, player):
        """
        Initialize a Stickman.
        :param player: 0 or 1
        """
        if player == 0:
            self.position = [0, 270]
            self.player = 0
        else:
            self.position = [1150, 270]
            self.player = 1
        # self.image = [pygame.image.load('standing.png'), pygame.image.load('moving.png')]
        self.curr_image = 0
        self.speed = 10

    def move(self):
        if self.player == 0:
            self.position[0] += random.randint(45, 55)
        else:
            self.position[0] += random.randint(-55, -45)

    def draw(self, s):
        if self.curr_image == 0:
            s.blit(NUM_TO_IMAGE[1], self.position)
            self.curr_image = 1
        else:
            s.blit(NUM_TO_IMAGE[0], self.position)
            self.curr_image = 0


class Game:
    def __init__(self, game_id):
        self.p0 = Stickman(0)
        self.p1 = Stickman(1)
        self.game_id = game_id
        self.score = [0, 0]  # [p0 score, p1 score]
        self.ready = False
        # self.net = Network2()
        print('here')

    def connected(self):
        return self.ready

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        run = True
        random_index = random.randint(0, 25)
        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]
        while run:
            clock.tick(10)
            screen.fill((214, 214, 214))
            pygame.draw.line(screen, BLACK, (WIDTH // 2, 0),
                             (WIDTH // 2, HEIGHT), 4)  # vertical line

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.K_ESCAPE:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == temp_Key:
                        self.p0.move()
                        random_index = random.randint(0, 25)
                        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]

            self.p1.move()
            # self.p1.position = self.parse_data(self.send_data2())

            text = FONT.render(ALPHA_LST[random_index], 1, (0, 0, 0))
            screen.blit(text, (50, 50))

            self.p0.draw(screen)
            self.p1.draw(screen)
            pygame.display.update()

   # def send_data2(self):
    #    data = str(self.net.p) + ":" + str(self.p0.position[0]) + "," + str(
     #       self.p0.position[1])
        # reply = self.net.send_pos(data)
       # return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0



# if __name__ == '__main__':
#     game_ = Game(0)
#    game_.run()