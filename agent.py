import asyncio
from web3 import Web3

from helpers.abi import agent_abi
from helpers.sa_contract_helper import SAContractHelper
from helpers.sa_factory_helper import SAFactoryHelper


class AutonomousAgent:
    """
    Represents an autonomous agent capable of deploying itself on a blockchain, interacting with other agents,
    and executing behaviors and message handlers.

    Attributes:
        factory_helper (SAFactoryHelper): Helper for deploying and interacting with the agent factory contract.
        address (str): The blockchain address of the deployed agent.
        web3 (Web3): An instance of Web3 for interacting with the blockchain.
        interactor (SAContractHelper): Helper for interacting with the agent's smart contract.
        other_agents (list): A list of other agents this agent interacts with.
        handlers (list): A list of registered message handlers for processing incoming messages.
        behaviours (list): A list of registered behaviors for periodic execution.
    """

    def __init__(self, provider_url: str, private_key: str, factory_address: str):
        """
        Initializes the AutonomousAgent instance by deploying it on the blockchain and setting up necessary components.

        Args:
            provider_url (str): The URL of the blockchain provider (e.g., Infura, Alchemy).
            private_key (str): The private key of the agent for signing transactions.
            factory_address (str): The address of the smart contract factory used to deploy the agent.
        """
        self.factory_helper = SAFactoryHelper(provider_url, factory_address, private_key)
        self.address = self.factory_helper.deploy_new_agent()
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.interactor = SAContractHelper(provider_url, self.address, agent_abi, private_key)
        self.other_agents = []
        self.handlers = []
        self.behaviours = []

    def register_behaviour(self, behaviour):
        """
        Registers a behavior for periodic execution.

        Args:
            behaviour (Behaviour): The behavior instance to be registered.
        """
        self.behaviours.append(behaviour)

    def register_handler(self, handler):
        """
        Registers a message handler for processing incoming messages.

        Args:
            handler (Handler): The handler instance to be registered.
        """
        self.handlers.append(handler)

    async def run_behaviours(self):
        """
        Executes all registered behaviors in a periodic loop.

        Each behavior is run asynchronously, and the loop waits for 1 second
        between executions.
        """
        while True:
            for behaviour in self.behaviours:
                await behaviour.run()
            await asyncio.sleep(1)

    def run(self):
        """
        Starts the agent by running all registered behaviors in an asynchronous event loop.
        """
        asyncio.run(self.run_behaviours())

    async def process_message(self, message: str, sender: str):
        """
        Processes an incoming message using all registered handlers.

        Args:
            message (str): The content of the incoming message.
            sender (str): The address or identifier of the sender.
        """
        for handler in self.handlers:
            handler.handle_message(message, sender)
