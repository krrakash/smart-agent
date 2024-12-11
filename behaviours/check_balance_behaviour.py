import datetime

from web3 import Web3

from helpers.abi import erc20_abi
from agent import AutonomousAgent
from behaviours.behaviour import Behaviour
from helpers.parse_arguments import config


class CheckBalanceBehaviour(Behaviour):

    def __init__(self, agent: AutonomousAgent):
        super().__init__(agent)
        self.web3 = Web3(Web3.HTTPProvider(config.provider_url))
        self.erc20_contract = self.web3.eth.contract(address=config.erc20_address, abi=erc20_abi)

    def guard(self) -> bool:
        return datetime.datetime.now() - self.last_ran_at >= datetime.timedelta(seconds=10)

    async def logic(self):
        try:
            balance = self.erc20_contract.functions.balanceOf(self.agent.address).call()
            decimals = self.erc20_contract.functions.decimals().call()
            human_readable_balance = balance / (10 ** decimals)
            print(f"Balance of {self.agent.address} is {human_readable_balance:.2f}")
        except Exception as e:
            print(f"Error checking balance: {e}")
            return None
