import asyncio
import json

from message import Message
from server.base_server import BaseServer


class SocketServerImpl(BaseServer):

    def __init__(self, host, port, peer_host=None, peer_port=None):
        super().__init__(host, port, peer_host, peer_port)
        self.server = None
        self.reader = None
        self.writer = None

    async def start_server(self):
        """Starts the server to listen for incoming connections."""
        self.server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        addr = self.server.sockets[0].getsockname()
        self.print(f'Server started and listening at {addr}')

    async def handle_connection(self, reader, writer):
        """Handles incoming connections."""
        self.print("Connection established to the outbox agent")
        # self.reader = reader
        # self.writer = writer
        asyncio.create_task(self.receive_message(reader))

    async def connect_to_peer(self):
        """Connects to the peer server as a client."""
        if self.peer_host and self.peer_port:
            while True:
                try:
                    self.reader, self.writer = await asyncio.open_connection(self.peer_host, self.peer_port)
                    self.print(f"Connected to peer at {self.peer_host}:{self.peer_port}")
                    self.is_connected = True
                    return
                except Exception as e:
                    self.print(
                        f"Could not connect to outbox agent at {self.peer_host}:{self.peer_port}, Make sure outbox agent is up and running. Retrying after 5 seconds...")
                    await asyncio.sleep(5)

    async def receive_message(self, reader):
        """Continuously receives messages from a connected peer."""
        while True:
            try:
                data = await reader.readline()
                if not data:
                    self.print("Connection closed by peer.")
                    break
                message = json.loads(data.decode('utf-8').rstrip())
                self.print(f"Received message: {message}")
                self.received_messages.put(Message(**message))
            except Exception as e:
                self.print(f"Error receiving message: {e}")
                break

    async def send_to_outbox(self, message: Message):
        message_str = json.dumps(message.__dict__)
        self.sent_messages.put(message_str)
        self.print(f"Saved message to outbox queue: {message_str}")

    async def flush_outbox(self):
        """Continuously sends messages to the peer."""
        if not self.is_connected:
            return

        try:
            while not self.sent_messages.empty():
                message = self.sent_messages.get()
                self.writer.write((message + "\n").encode('utf-8'))
                await self.writer.drain()
                self.print(f"Sent message to agent from outbox queue: {message}")
        except Exception as e:
            self.print(f"Error sending message: {e}")
            self.is_connected = False

    async def run(self):
        """Starts the server and attempts to connect to the peer."""
        await self.start_server()
        if self.peer_host and self.peer_port:
            await self.connect_to_peer()
