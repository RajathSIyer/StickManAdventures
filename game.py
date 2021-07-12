import pygame
import random

pygame.init()
class Stickman():
    def __init__(self):
        self.position = [0,270]
        self.image = [pygame.image.load('standing.png'), pygame.image.load('moving.png')]
        self.curr_image = 0
        self.speed = 10
class Opponent(Stickman):
    def __init__(self):
        super().__init__()
        self.position[0] = 1150
def main():
    frank = Stickman()
    bob = Opponent()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Stick Adventures")
    looping = True
    
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
        
        screen.fill([214,214,214])
        
        frank.position[0] += random.randint(0,4)
        bob.position[0] += random.randint(-4,0)
        
        
        if frank.curr_image == 0:
            screen.blit(frank.image[1],frank.position)
            frank.curr_image = 1
        else:
            screen.blit(frank.image[0],frank.position)
            frank.curr_image = 0

        if bob.curr_image == 0:
            screen.blit(bob.image[1],bob.position)
            bob.curr_image = 1
        else:
            screen.blit(bob.image[0],bob.position)
            bob.curr_image = 0

        pygame.display.update()
        clock.tick(10)
if __name__ == '__main__':
    main()