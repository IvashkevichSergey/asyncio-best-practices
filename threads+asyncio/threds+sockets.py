import socket
from threading import Thread


class ClientThread(Thread):
    """Класс для обработки в непрерывном цикле каждого отдельного подключения
    к сокету"""
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    raise BrokenPipeError('Подключение закрыто!')
                print("We've got data -->", data)
                self.client.sendall(data)
        except OSError as e:
            print("Thread was interrupted by", e)

    def close(self):
        if self.is_alive():
            self.client.sendall(b'Trying to stop')
            self.client.shutdown(socket.SHUT_RDWR)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", 8080))
        server_socket.listen()
        connections = []
        try:
            while True:
                print('Ready to wait')
                connection, _ = server_socket.accept()
                print('Got connection from', _)
                new_thread = ClientThread(connection)
                connections.append(new_thread)
                print('Created new thread', new_thread)
                new_thread.start()
        except KeyboardInterrupt:
            [thread.close() for thread in connections]
