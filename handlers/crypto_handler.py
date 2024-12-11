from helpers.abi import erc20_abi
from agent import AutonomousAgent
from handlers.handler import Handler
from helpers.parse_arguments import config


class CryptoHandler(Handler):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)

    def handle_message(self, sender: str, message: str) -> bool:
        if "crypto" in message.lower():
            print(f"Crypto message: {message} received from {sender}")
            amount = 1
            self.agent.interactor.send_erc20(config.erc20_address, erc20_abi, sender, amount)
            print(f"sent {amount} to address {sender}")
            return True
        return False
