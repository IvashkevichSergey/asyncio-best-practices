import asyncio
import signal
from asyncio import AbstractEventLoop
import socket

from utils import delay, cancel_tasks

tasks = []


async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop) -> None:
    """Ожидает подключение к сокету и запускает корутину для прослушивания сообщений от пользователя"""
    while True:
        print("START")
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        task = asyncio.create_task(echo(connection, loop))
        print("task created")
        tasks.append(task)
        print("task awaited")


async def echo(client_socket: socket, loop: AbstractEventLoop) -> None:
    """Симулирует эхо-сервис, отправляющий в консоль сообщения напечатанные пользователем"""
    print("ECHO STARTS")
    try:
        while data := await loop.sock_recv(client_socket, 1024):
            print("received >>> ", data)
            if data == b"\r\n":
                raise Exception("BOOM happened")
            await loop.sock_sendall(client_socket, data)
    except Exception as e:
        print(e)
    finally:
        client_socket.close()


async def main():
    """Создает новый сокет и связывает его с адресом и портом сервера, после чего
    запускается корутину для прослушивания подключений к сокету"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = "localhost", 8080
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connections(server_socket, asyncio.get_event_loop())


# async def main():
#     loop: AbstractEventLoop = asyncio.get_running_loop()
#     loop.add_signal_handler(signal.SIGINT, cancel_tasks)
#     await delay(10)

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
