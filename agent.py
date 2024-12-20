import asyncio
from datetime import datetime, timezone

from web3 import Web3

from helpers.sa_contract_helper import SAContractHelper
from helpers.utils import get_server_instance


class AutonomousAgent:
    """
    Represents an autonomous agent capable of deploying itself on a blockchain, interacting with other agents,
    executing behaviors, and handling incoming messages.

    Attributes:
        server (BaseServer): The server instance for handling communication with other agents.
        web3 (Web3): An instance of Web3 for interacting with the blockchain.
        interactor (SAContractHelper): Helper for interacting with the agent's smart contract on the blockchain.
        handlers (list): A list of registered message handlers to process incoming messages.
        behaviours (list): A list of registered behaviors for periodic asynchronous execution.
    """

    def __init__(self, provider_url: str, private_key: str):
        """
        Initializes the AutonomousAgent instance by setting up the server, blockchain connection, and contract interactor.

        Args:
            provider_url (str): The URL of the blockchain provider (e.g., Infura, Alchemy).
            private_key (str): The private key of the agent's Ethereum account for signing transactions.
        """
        self.server = get_server_instance()
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.interactor = SAContractHelper(provider_url, private_key)
        self.handlers = []
        self.behaviours = []

    def get_message_to_process(self):
        """
        Retrieves the next message from the server's received messages queue, if available.

        Returns:
            Message: The next message to process, or None if the queue is empty.
        """
        if self.server.received_messages.empty():
            return None
        else:
            return self.server.received_messages.get()

    def print(self, message):
        """
        Logs a message with the server's host and port as a prefix.

        Args:
            message (str): The message to be logged.
        """
        utc_time = datetime.now(timezone.utc)
        local_time = utc_time.astimezone()
        local_iso_time = local_time.isoformat().split('.')[0]
        print(f"{self.server.host}:{self.server.port} [{local_iso_time}]: {message}")

    def register_behaviour(self, behaviour):
        """
        Registers a behavior for periodic execution.

        Args:
            behaviour (Behaviour): The behavior instance to be registered for execution.
        """
        self.behaviours.append(behaviour)

    def register_handler(self, handler):
        """
        Registers a message handler for processing incoming messages.

        Args:
            handler (Handler): The handler instance to be registered for message processing.
        """
        self.handlers.append(handler)

    async def run_behaviours(self):
        """
        Executes all registered behaviors in an infinite asynchronous loop.

        Each behavior's `run` method is executed asynchronously. The loop pauses for 1 second
        between successive executions of behaviors.
        """
        while True:
            for behaviour in self.behaviours:
                await behaviour.run()
            await asyncio.sleep(0.1)

    def run(self):
        """
        Starts the agent by running the server and all registered behaviors within an asynchronous event loop.

        This method orchestrates both communication and periodic behavior execution for the agent.
        """
        asyncio.gather(self.server.run(), self.run_behaviours())
        asyncio.get_event_loop().run_forever()

    async def process_message(self, message: str):
        """
        Processes an incoming message using all registered handlers.

        Each registered handler's `handle_message` method is invoked with the incoming message.

        Args:
            message (str): The content of the incoming message to be processed.
        """
        for handler in self.handlers:
            handler.handle_message(message)

