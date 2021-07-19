import pygame
import random
import socket
# from network import Network
import pickle
from typing import *

pygame.init()

BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720
FONT = pygame.font.SysFont("comicsans", 100)

NUM_TO_IMAGE = {0: pygame.image.load('charImages/standing.png'),
                1: pygame.image.load('charImages/moving.png')}
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
ALPHABET = list('abcdefghijklmnopqrstuvwxyz')


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
        self.curr_image = 0
        self.speed = 10
        self.ready = False

    def move(self):
        if self.player == 0:
            self.position[0] += random.randint(WIDTH//200, WIDTH//25)
        else:
            self.position[0] += random.randint(-WIDTH//25, -WIDTH//200)

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

    def connected(self):
        return self.ready

    def is_game_over(self):
        return self.p0.position[0] >= WIDTH // 2 or self.p1.position[0] <= WIDTH // 2

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        run = True
        temp_letter = random.choice(ALPHABET)
        temp_Key = LETTER_TO_PYGAME[temp_letter]
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
                        temp_letter = random.choice(ALPHABET)
                        temp_Key = LETTER_TO_PYGAME[temp_letter]

            # self.p1.move()
            # self.p1.position = self.parse_data(self.send_data2())

            text = FONT.render(temp_letter, 1, (0, 0, 0))
            screen.blit(text, (50, 50))

            self.p0.draw(screen)
            self.p1.draw(screen)
            pygame.display.update()


# if __name__ == '__main__':
#     game_ = Game(0)
#    game_.run()
