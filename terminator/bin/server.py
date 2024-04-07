import threading
import socket
import pickle

from colorama import Fore
from datetime import datetime


class Server:
    def __init__(self, terminal):
        self.terminal = terminal
        self.server = None
        self.server_address = (self.terminal.settings["localhost"], self.terminal.settings["host port"])
        self.clients = []
        self.usernames = []
        self.run = False
        self.client_threads = []
        self.party_name = "PARTY"
        self.receive_thread = None
        self.lock = threading.Lock()
        self.party_text_buffer = []

    def start_server(self):
        with self.lock:
            self.server.run = True
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.server_address)
            self.server.listen()
            self.party_text_buffer.append(
                self.server_message(f"{self.party_name} server has started and is listening.")
            )
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()

    def broadcast(self, message: bytes):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        while self.run:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                with self.lock:
                    i = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    username = self.usernames[i]
                    self.usernames.remove(username)
                    self.broadcast(pickle.dumps(self.server_message(f"{username} was disconnected from the chat")))
                break

    def receive(self):
        while self.run:
            client, client_address = self.server.accept()
            self.clients.append(client)

            client.send(pickle.dumps("INIT CONNECTION"))
            username = pickle.loads(client.recv(1024))
            with self.lock:
                self.usernames.append(username)
            self.party_text_buffer.append(
                self.server_message(f"The user {username} connected from the address: {str(client_address)}")
            )
            self.broadcast(pickle.dumps(self.server_message(f"{username} joined the chat")))
            client.send(pickle.dumps(
                self.server_message(f"You successfully connected to the {self.party_name} party!"))
            )

            client_thread = threading.Thread(target=self.handle_client, args=[client])
            client_thread.start()
            with self.lock:
                self.client_threads.append(client_thread)

        with self.lock:
            for thread in self.client_threads:
                thread.join()

    def server_message(self, message: str) -> dict:
        return {
            "message": message,
            "pic": "🎉",
            "name": f"{Fore.WHITE}{self.party_name.upper()}",
            "time": datetime.now().strftime('%H:%M')
        }
