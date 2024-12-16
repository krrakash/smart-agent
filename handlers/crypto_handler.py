import os

from agent import AutonomousAgent
from handlers.handler import Handler
from message import Message


class CryptoHandler(Handler):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)
        self.amount = float(os.getenv('TRANSFER_AMOUNT'))
        self.to_address = os.getenv("OUTBOX_PUBLIC_ADDRESS")

    def handle_message(self, message: Message) -> bool:
        if "crypto" in message.message.lower():
            decimals = self.agent.interactor.decimals
            amount = int(self.amount * (10 ** decimals))
            self.agent.print(f"Crypto message received: {message.__dict__}\n sending {amount} to {self.to_address}")
            sent = self.agent.interactor.send_token(self.to_address, amount)
            if sent:
                self.agent.print(f"sent {amount} to address {self.to_address}")
            else:
                self.agent.print(f"failed to handle crypto message {message.__dict__}")
            return True
        return False
