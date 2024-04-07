import threading
import socket
import pickle

from datetime import datetime


class Client:
    def __init__(self, terminal):
        self.terminal = terminal
        self.client = None
        self.server_host = "127.0.0.1"
        self.server_port = 8888
        self.receive_thread = None
        self.write_thread = None
        self.run = False
        self.party_text_buffer = []
        self.lock = threading.Lock()

    def start_client(self):
        with self.lock:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_host, self.server_port))
            self.client.run = True
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()

    def receive(self):
        while self.run:
            try:
                message = pickle.loads(self.client.recv(1024))

                if message == "INIT CONNECTION":
                    self.client.send(pickle.dumps(self.terminal.account["plain name"]))
                else:
                    with self.lock:
                        self.party_text_buffer.append(message)
            except (pickle.UnpicklingError, EOFError) as e:
                print(f"An error occurred in messaging the server! {e}")
                self.run = False
                self.party_text_buffer = []
                self.client.close()
                break
            except socket.error as e:
                print(f"Socket error occurred: {e}")
                self.run = False
                self.party_text_buffer = []
                self.client.close()
                break

    def write(self, message: str, pic: str, name: str):
        try:
            self.client.send(pickle.dumps(
                {"message": message, "pic": pic, "name": name, "time": datetime.now().strftime('%H:%M')}
            ))
        except socket.error as e:
            print(f"Socket error occurred while trying to write message: {e}")
