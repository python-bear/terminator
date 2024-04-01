import threading
import socket


class Client:
    def __init__(self, terminal):
        self.terminal = terminal
        self.client = None
        self.server_host = "127.0.0.1"
        self.server_port = 8888
        self.receive_thread = None
        self.write_thread = None
        self.run = False

    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_host, self.server_port))

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while self.run:
            try:
                message = self.client.recv(1024).decode("ascii")

                if message == "INIT CONNECTION":
                    self.client.send(self.terminal.account["plain name"].encode("ascii"))
                else:
                    print(message)
            except:
                print("An error occurred in messaging the server!")
                self.client.close()
                break

        self.receive_thread.join()

    def write(self, message: str):
        self.client.send(message.encode("ascii"))
