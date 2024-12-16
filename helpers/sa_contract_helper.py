import os

from eth_account import Account
from web3 import Web3

from helpers.utils import erc20_abi


class SAContractHelper:
    """
    A helper class for interacting with an ERC20 smart contract. This includes functionalities such as sending tokens,
    checking balances, and initializing with blockchain provider details.

    Attributes:
        web3 (Web3): An instance of Web3 for interacting with the blockchain.
        account (Account): The Ethereum account derived from the provided private key.
        private_key (str): The private key used to sign transactions.
        contract (Contract): An instance of the ERC20 token contract for interaction.
        decimals (int): The number of decimal places the ERC20 token supports.
    """

    def __init__(self, provider_url: str, private_key: str):
        """
        Initializes the SAContractHelper with the blockchain provider, ERC20 token details, and account credentials.

        Args:
            provider_url (str): The URL of the blockchain provider (e.g., Infura, Alchemy).
            private_key (str): The private key of the Ethereum account.
        """
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = Account.from_key(private_key)
        self.private_key = private_key
        self.contract = self.web3.eth.contract(address=os.getenv("ERC20_ADDRESS"), abi=erc20_abi)
        self.decimals = self.contract.functions.decimals().call()

    def send_token(self, to_address: str, amount: int) -> str:
        """
        Sends ERC20 tokens to a specified address.

        Args:
            to_address (str): The recipient's Ethereum address.
            amount (int): The amount of tokens to send, in the smallest unit (e.g., wei for Ether).

        Returns:
            str: The transaction hash of the token transfer transaction as a hexadecimal string.

        Raises:
            Exception: If there is an error during the transaction.
        """
        try:
            tx = self.contract.functions.transfer(to_address, amount).build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'gas': 100000,
                'gasPrice': self.web3.to_wei('20', 'gwei')
            })

            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return self.web3.to_hex(tx_hash)
        except Exception as e:
            print("Error during ERC20 token transfer", e)
            return None

    async def check_balance(self) -> float:
        """
        Retrieves the account's ERC20 token balance.

        Returns:
            float: The token balance in human-readable format (adjusted for token decimals).
            None: If an error occurs during the balance retrieval.

        Raises:
            Exception: If there is an issue accessing the token contract or performing the call.
        """
        try:
            balance = self.contract.functions.balanceOf(self.account.address).call()
            decimals = self.contract.functions.decimals().call()
            human_readable_balance = balance / (10 ** decimals)
            return human_readable_balance
        except Exception as e:
            print(f"Error checking balance: {e}")
            return None
