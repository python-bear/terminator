import threading
import socket


class Server:
    def __init__(self, terminal):
        self.terminal = terminal
        self.server = None
        self.server_address = (self.terminal.settings["localhost"], self.terminal.settings["host port"])
        self.clients = []
        self.usernames = []
        self.run = False
        self.client_threads = []

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.server_address)
        self.server.listen()
        print("Server has started and is listening.")
        self.receive()

    def broadcast(self, message: bytes):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        while self.run:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                i = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                username = self.usernames[i]
                self.usernames.remove(username)
                self.broadcast(f"{username} was disconnected from the chat".encode("ascii"))
                break

    def receive(self):
        while self.run:
            client, client_address = self.server.accept()
            self.clients.append(client)
            print(f"Connected with {str(client_address)}")

            client.send("INIT CONNECTION".encode("ascii"))
            username = client.recv(1024).decode("ascii")
            self.usernames.append(username)
            print(f"Username of last connected client is {username}")
            self.broadcast(f"{username} joined the chat".encode("ascii"))
            client.send("You successfully connected to the server!".encode("ascii"))

            client_thread = threading.Thread(target=self.handle_client, args=[client])
            client_thread.start()
            self.client_threads.append(client_thread)

        for thread in self.client_threads:
            thread.join()
