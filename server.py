import socket
from _thread import *
import pickle
from game import Game

server = ""  # keep this as empty string
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
game_id_to_players = dict()
idCount = 0
pos = ['0:0,270', '1:1150,270']


def threaded_client(conn, p, gameId):
    global idCount, pos
    conn.send(str.encode(str(p)))
    print('Server send:', str(p))

    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode('utf-8')

            if gameId in games:
                game = games[gameId]
                # print(game)
                if not data:
                    break
                else:
                    print('Server received:', data)
                    # print(pickle.dumps(game))

                    if data == "reset":
                        pass
                    elif 'ready' in data:
                        if data[1] == '0':
                            game.p0.ready = True
                        else:
                            game.p1.ready = True
                        game.ready = game.p0.ready and game.p1.ready

                    elif data[1] == ':':
                        # other_player = str(int(not(int(data[0]))))
                        reply = data
                        arr = reply.split(':')
                        id_ = int(arr[0])
                        nid = int(not id_)
                        pos[id_] = reply
                        reply = pos[nid][:]
                        print('Server sent:', reply)
                        conn.sendall(str.encode(reply))
                   # elif data == 'get':
                    else:
                        conn.sendall(pickle.dumps(game))
            else:
                print(gameId)
                print(games)
                break
        except:
            break

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
            game_id_to_players[gameId] = [conn]
            print("Creating a new game...")
        else:
            # games[gameId].ready = True
            game_id_to_players[gameId].append(conn)
            p = 1

        start_new_thread(threaded_client, (conn, p, gameId))