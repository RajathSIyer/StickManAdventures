import pygame
from network import Network
import pickle
import random
import socket

pygame.init()

BLACK = (0, 0, 0)
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


WIDTH = 1280
HEIGHT = 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

n = Network()

def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Finding opponent...", 1, (255, 0, 0), True)
        win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    else:
        print('Game is connected!')
        # game.run()
        print(game.p0.position, game.p1.position)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        run = True
        random_index = random.randint(0, 25)
        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]
        print('should be true', n.p == p)
        if n.p != p:
            print('n.p:', n.p, 'p:', p)
            print(type(n.p), type(p))
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
                        # game.p0.move()
                        if p == 0:
                            game.p0.move()
                        else:
                            game.p1.move()

                        random_index = random.randint(0, 25)
                        temp_Key = LETTER_TO_PYGAME[ALPHA_LST[random_index]]

            # game.p1.move()
            # n.send('abc')
            if p == 0:
                data = str(n.getP()) + ":" + str(game.p0.position[0]) + "," + str(game.p0.position[1])
                # game.p1.position = parse_data(send_data2(data))
                print('client sent:', data)
                n.client.send(str.encode(data))
                reply = n.client.recv(2048).decode()
                print('received:', reply)
                if reply[0] != n.getP():  # the problem is this is never True
                    print('here1')
                    game.p1.position = parse_data(reply)
                # else:
                 #   reply = n.client.recv(2048).decode()
                  #  print('here1')
                   # game.p1.position = parse_data(reply)
            else:
                data = str(n.getP()) + ":" + str(game.p1.position[0]) + "," + str(game.p1.position[1])
                # game.p0.position = parse_data(send_data2(data))
                print('client sent:', data)
                n.client.send(str.encode(data))
                reply = n.client.recv(2048).decode()
                print('received:', reply)
                if reply[0] != n.getP():
                    game.p0.position = parse_data(reply)

           # if p == 0:
           #     game.p1.position = parse_data(send_data2(data))
           # else:
           #     game.p0.position = parse_data(send_data2(data))
            print(p, game.p0.position, game.p1.position)
           # n.client.send(data.encode('utf-8'))
            # print('client sent:', data)
            """
            try:
                just_received = n.client.recv(2048)
                # print(just_received)
                just_received = just_received.decode('utf-8')
                print('player', p)
                print('client received:', just_received)
                if p != int(just_received[0]):
                    if int(just_received[0]) == 1 and p == 0:
                        game.p1.position = parse_data(just_received)
                    elif int(just_received[0]) == 0 and p == 1:
                        game.p0.position = parse_data(just_received)
                    if p == 0:
                        print('my position:', game.p0.position)
                        print('Opponents position:', game.p1.position)
                    else:
                        print('my position:', game.p1.position)
                        print('Opponents position:', game.p0.position)
            except UnicodeDecodeError:
                print('UnicodeDecodeError')
            """

            text = FONT.render(ALPHA_LST[random_index], 1, (0, 0, 0))
            screen.blit(text, (50, 50))

            game.p0.draw(screen)
            game.p1.draw(screen)
            pygame.display.update()

    pygame.display.update()


def send_data2(data):
    reply = n.send_pos(data)
    return reply


def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return [int(d[0]), int(d[1])]
    except:
        return [0, 0]


def main():
    run = True
    clock = pygame.time.Clock()
    got_game = False
    player = int(n.getP())  # 0 or 1
    print("You are player", player)

    while run:
        clock.tick(60)
        if not got_game:  # if it hasn't found an opponent yet
            try:
                game = n.send("get")
                print(game)
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
        win.blit(text, (100, 200))
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