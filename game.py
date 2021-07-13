import pygame
import random
import PIL

pygame.init()

BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720

NUM_TO_IMAGE = {0: pygame.image.load('standing.png'), 1: pygame.image.load('moving.png')}


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
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.K_ESCAPE:
                    run = False

            self.p0.move()
            self.p1.move()

            self.p0.curr_image = int(not self.p0.curr_image)
            self.p1.curr_image = int(not self.p1.curr_image)

            screen.fill((214, 214, 214))
            pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)  # vertical line
            self.p0.draw(screen)
            self.p1.draw(screen)
            pygame.display.update()


"""
def main():  # can remove
    # game.p0 = Stickman()
    # game.p1 = Opponent()
    game = Game(0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Stick Adventures")
    looping = True

    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
                pygame.quit()

        screen.fill((214, 214, 214))
        pygame.draw.line(screen, BLACK, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 4)

        game.p0.move()
        game.p1.move()

        if game.p0.curr_image == 0:
            screen.blit(NUM_TO_IMAGE[1], game.p0.position)
            game.p0.curr_image = 1
        else:
            screen.blit(NUM_TO_IMAGE[0], game.p0.position)
            game.p0.curr_image = 0

        if game.p1.curr_image == 0:
            screen.blit(NUM_TO_IMAGE[1], game.p1.position)
            game.p1.curr_image = 1
        else:
            screen.blit(NUM_TO_IMAGE[0], game.p1.position)
            game.p1.curr_image = 0

        pygame.display.update()
        clock.tick(10)
"""


# if __name__ == '__main__':
#     game_ = Game(0)
#    game_.run()