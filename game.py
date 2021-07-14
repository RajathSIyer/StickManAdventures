import pygame
import random
import PIL

pygame.init()

BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720
FONT= pygame.font.SysFont("comicsans", 100)

NUM_TO_IMAGE = {0: pygame.image.load('standing.png'), 1: pygame.image.load('moving.png')}
LETTER_TO_PYGAME = {'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c, 'd': pygame.K_d, 
'e': pygame.K_e, 'f': pygame.K_f, 'g': pygame.K_g, 'h': pygame.K_h, 'i': pygame.K_i, 
'j': pygame.K_j, 'k': pygame.K_k, 'l': pygame.K_l, 'm': pygame.K_m, 'n': pygame.K_n, 
'o': pygame.K_o, 'p': pygame.K_p, 'q': pygame.K_q, 'r': pygame.K_r, 's': pygame.K_s, 
't': pygame.K_t, 'u': pygame.K_u, 'v': pygame.K_v, 'w': pygame.K_w, 'x': pygame.K_x, 
'y': pygame.K_y, 'z': pygame.K_z}
ALPHA_LST = list('abcdefghijklmnopqrstuvwxyz')
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
            self.position[0] += random.randint(2, 4)
        else:
            self.position[0] += random.randint(-4, -2)

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
        print('here')

    def connected(self):
        return self.ready

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        run = True
        random_index = random.randint(0,25)
        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]
        while run:
            clock.tick(10)
           
           
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.K_ESCAPE:
                    run = False
        
                if event.type == pygame.KEYDOWN:
                    if event.key == temp_Key:
                        random_index = random.randint(0,25)
                        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]

                        self.p0.move()
            self.p1.move()

            screen.fill((214, 214, 214))
            text = FONT.render(ALPHA_LST[random_index], 1, (0,0,0))
            screen.blit(text, (50 , 50))

            pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)  # vertical line
            self.p0.draw(screen)
            self.p1.draw(screen)
            pygame.display.update()




if __name__ == '__main__':
    game_ = Game(0)
    game_.run()