import queue
from abc import abstractmethod

from message import Message
from datetime import datetime, timezone


class BaseServer:
    """
    A base class for creating servers with message queuing and peer-to-peer communication capabilities.
    This class defines the basic structure for managing received and sent messages, along with attributes 
    for server and peer connection details. It includes an abstract method for sending messages, 
    which must be implemented by subclasses.

    Attributes:
        host (str): The host address of this server.
        port (int): The port number on which this server is running.
        peer_host (str): The host address of the peer server to connect to as a client.
        peer_port (int): The port number of the peer server to connect to as a client.
        received_messages (Queue): A queue to store messages received by the server.
        sent_messages (Queue): A queue to store messages to be sent by the server.
        is_connected (bool): A flag indicating whether the server is connected to a peer.
    """

    def __init__(self, host, port, peer_host=None, peer_port=None):
        """
        Initializes the BaseServer with server and peer connection details.

        Args:
            host (str): The host address for this server.
            port (int): The port number for this server.
            peer_host (str, optional): The host address of the peer server to connect to. Defaults to None.
            peer_port (int, optional): The port number of the peer server to connect to. Defaults to None.
        """
        self.host = host
        self.port = int(port)
        self.peer_host = peer_host
        self.peer_port = int(peer_port) if peer_port else None
        self.received_messages = queue.Queue()
        self.sent_messages = queue.Queue()
        self.is_connected = False

    def print(self, message):
        """
        Logs a message with the server's host and port as a prefix.

        Args:
            message (str): The message to be logged.
        """

        utc_time = datetime.now(timezone.utc)
        local_time = utc_time.astimezone()
        local_iso_time = local_time.isoformat().split('.')[0]
        print(f"{self.host}:{self.port} [{local_iso_time}]: {message}")

    @abstractmethod
    async def send_to_outbox(self, message: Message):
        """
        Abstract method for sending a message to the outbox queue. This method must be implemented 
        by subclasses to define specific behavior for message handling.

        Args:
            message (Message): The message object to send to the outbox.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        pass
