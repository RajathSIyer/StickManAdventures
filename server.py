import socket
from _thread import *
import pickle
from game import Game

server = ""
# server = "139.177.194.104"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        # try:
        data = conn.recv(2048).decode('utf-8')

        if gameId in games:
            game = games[gameId]
            print(game)
            if not data:
                break
            else:
                print('Server received:', data)
                if data == "reset":
                    pass
                elif data == 'P0_move':  # we can change this
                    pass
                elif data == 'P1_move':
                    pass
                print(pickle.dumps(game))
                conn.sendall(pickle.dumps(game))
        else:
            break
        # except:
         #   break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


if __name__ == '__main__':
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            p = 1

        start_new_thread(threaded_client, (conn, p, gameId))