import socket
import pickle


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
