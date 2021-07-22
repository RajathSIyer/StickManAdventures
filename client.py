import pygame
# from network import Network
import pickle
import random
import socket
import pygame_input

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 146, 204)
YELLOW = (255, 255, 0)
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
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
FONT2 = pygame.font.SysFont("comicsans", 60)

WIDTH = 1280
HEIGHT = 720
MEDIUM_FONT = pygame.font.SysFont("times new roman", 60)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = '172.105.20.159'  # new linode
        self.server = 'localhost'
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
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)

    def send_pos(self, data):
        try:
            print('client sent:', data)
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            print('received:', reply)
            return reply
        except socket.error as e:
            return str(e)


n = Network()


def redrawWindow(win, game, p, username: str):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Finding opponent...", 1, (255, 0, 0), True)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2,
                        HEIGHT // 2 - text.get_height() // 2))
    else:
        # problem is game.ready is True when it should be False
        print(game.p0.ready, game.p1.ready)
        print('Game is connected!')
        # game.run()
        print(game.p0.position, game.p1.position)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        run = True
        temp_letter = random.choice(ALPHABET)
        temp_Key = LETTER_TO_PYGAME[temp_letter]
        text_you = FONT.render("You", 1, (0, 0, 0))

        text_main_menu = MEDIUM_FONT.render("Back to Main Menu", 1, RED)

        game.usernames[p] = username

        print('should be true', int(n.p) == p)
        while run:
            clock.tick(10)
            screen.fill((214, 214, 214))
            pygame.draw.line(screen, BLACK, (WIDTH // 2, 0),
                             (WIDTH // 2, HEIGHT), 4)  # vertical line

            if p == 0:
                screen.blit(text_you, (100, HEIGHT - 100))
            else:
                screen.blit(text_you, (WIDTH - 200, HEIGHT - 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.K_ESCAPE:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == temp_Key:
                        if p == 0:
                            game.p0.move()
                        else:
                            game.p1.move()

                        temp_letter = random.choice(ALPHABET)
                        temp_Key = LETTER_TO_PYGAME[temp_letter]

            if p == 0:
                data = str(n.getP()) + ":" + str(
                    game.p0.position[0]) + "," + str(game.p0.position[1])
                print('client sent:', data)
                reply = n.send_pos(data)

                if reply[0] != n.getP():
                    print('here1')
                    game.p1.position = parse_data(reply)

            else:
                data = str(n.getP()) + ":" + str(
                    game.p1.position[0]) + "," + str(game.p1.position[1])
                print('client sent:', data)
                reply = n.send_pos(data)
                print('received:', reply)
                if reply[0] != n.getP():
                    game.p0.position = parse_data(reply)

            print(p, game.p0.position, game.p1.position)

            if game.is_game_over():
                screen.fill(BLACK)
                if game.p0.position[0] >= WIDTH // 2:  # p0 wins
                    game.score[0] += 1
                    if p == 0:
                        text = FONT.render("Game Over. You won!", 1, WHITE)
                        screen.blit(text, (100, 100))
                    else:
                        text = FONT.render("Game Over. You lost", 1, WHITE)
                        screen.blit(text, (100, 100))

                elif game.p1.position[0] <= WIDTH // 2:  # p1 wins
                    game.score[1] += 1
                    if p == 1:
                        text = FONT.render("Game Over. You won!", 1, WHITE)
                        screen.blit(text, (100, 100))
                    else:
                        text = FONT.render("Game Over. You lost", 1, WHITE)
                        screen.blit(text, (100, 100))

                # P0: 3-2
                # P1: 2-3
                if p == 0:
                    text_score = game.usernames[0] + ': ' + str(game.score[0]) + '-' + str(game.score[1])
                else:
                    text_score = game.usernames[1] + ': ' + str(game.score[1]) + '-' + str(game.score[0])
                text_score = FONT.render(text_score, 1, WHITE)

                main_menu_rect = pygame.draw.rect(screen, WHITE, (
                55, HEIGHT - 150, text_main_menu.get_width() + 10, 100),
                                                  1)  # Back to Main Menu rect
                screen.blit(text_score, (WIDTH // 2, HEIGHT // 2))

                screen.blit(text_main_menu, (60, HEIGHT - 140))  # Back to Main Menu text
                game.p0.position = [0, 270]
                game.p1.position = [WIDTH - 130, 270]

                game.ready = False
                game.p0.ready = False
                game.p1.ready = False
                a = False

                while not a:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and main_menu_rect.collidepoint(event.pos):
                            menu_screen()

                    pygame.display.update()

            text = FONT.render(temp_letter, 1, (0, 0, 0))
            screen.blit(text, (50, 50))

            game.p0.draw(screen)
            game.p1.draw(screen)
            pygame.display.update()

    pygame.display.update()


def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return [int(d[0]), int(d[1])]
    except:
        return [0, 0]


def main(username: str):
    run = True
    clock = pygame.time.Clock()
    got_game = False
    player = int(n.getP())  # 0 or 1
    print("You are player", player)

    while run:
        clock.tick(60)
        if not got_game:  # if it hasn't found an opponent yet
            # try:
            game = n.send("get")
            print(game)
            game.p0.position = [0, 270]
            game.p1.position = [WIDTH - 130, 270]
            print(game.connected())
            msg = 'P' + str(player) + 'ready'
            n.client.send(str.encode(msg))
            got_game = game.connected()  # bool
            print('got_game', got_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, game, player, username)


def menu_screen():
    textinput = pygame_input.TextInput()
    run = True
    clock = pygame.time.Clock()
    FONT3 = pygame.font.SysFont("comicsans", 40)
    while run:
        win.blit(pygame.image.load("charImages/background.jpeg"), (0, 0))

        play_rect = pygame.draw.rect(win, BLUE,
                         pygame.Rect(int(WIDTH // 2.7), int(HEIGHT // 2.55), int(WIDTH // 3.65),
                                     HEIGHT // 9))
        play_text = FONT2.render("Click to Play!", 1, (255, 255, 0))
        win.blit(play_text, (WIDTH // 2.5, HEIGHT // 2.5 + 10))
        made_by_text = FONT2.render("Made by Raj²", 1, WHITE)
        win.blit(made_by_text, (WIDTH - made_by_text.get_width() - 10, HEIGHT - 50))

        pygame.draw.rect(win, YELLOW,
                         pygame.Rect(WIDTH // 5, int(HEIGHT // 1.5), WIDTH // 2,
                                     HEIGHT // 15))
        name_text = FONT3.render("Enter Your Name: ", 1, BLUE)
        win.blit(name_text, (int(WIDTH // 4.95), int(HEIGHT // 1.465)))

        curr_events = pygame.event.get()
        x = textinput.update(curr_events)
        if x:
            print(textinput.get_text())  # prints name after enter is pressed
        win.blit(textinput.get_surface(), (505, 490))
        pygame.display.update()
        clock.tick(60)

        for event in curr_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(pygame.mouse.get_pos()) and len(textinput.get_text()) > 0:
                run = False

    main(textinput.get_text())


while True:
    menu_screen()