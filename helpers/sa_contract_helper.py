from eth_account import Account
from web3 import Web3


class SAContractHelper:
    """
    A helper class for interacting with a deployed smart contract, including sending messages,
    transferring ERC20 tokens, acknowledging messages, and retrieving inbox data.

    Attributes:
        web3 (Web3): An instance of Web3 for blockchain interaction.
        contract_address (str): The address of the smart contract.
        abi (list): The ABI (Application Binary Interface) of the smart contract.
        private_key (str): The private key of the account for signing transactions.
        account (Account): The Ethereum account derived from the private key.
        contract (Contract): An instance of the smart contract for interaction.
    """

    def __init__(self, provider_url: str, contract_address: str, abi: list, private_key: str):
        """
        Initializes the SAContractHelper with the blockchain provider, contract details, and account credentials.

        Args:
            provider_url (str): The URL of the blockchain provider (e.g., Infura, Alchemy).
            contract_address (str): The address of the smart contract.
            abi (list): The ABI of the smart contract.
            private_key (str): The private key of the Ethereum account.
        """
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.abi = abi
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def send_message(self, sender: str, receiver: str, message: str) -> str:
        """
        Sends a message to another smart contract's inbox.

        Args:
            sender (str): The address of the sender.
            receiver (str): The address of the receiving smart contract.
            message (str): The message content.

        Returns:
            str: The transaction hash of the message sending transaction.

        Raises:
            Exception: If there is an error during the transaction.
        """
        try:
            contract = self.web3.eth.contract(address=receiver, abi=self.abi)
            tx = contract.functions.addToInbox(sender, message).build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'gas': 3000000,
                'gasPrice': self.web3.to_wei('20', 'gwei')
            })
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return self.web3.to_hex(tx_hash)
        except Exception as e:
            print("Error sending transaction to contract", e)
            return None

    def send_erc20(self, token_address: str, token_abi: list, to_address: str, amount: float) -> str:
        """
        Sends ERC20 tokens to a specified address.

        Args:
            token_address (str): The address of the ERC20 token contract.
            token_abi (list): The ABI of the ERC20 token contract.
            to_address (str): The recipient's Ethereum address.
            amount (float): The amount of tokens to send.

        Returns:
            str: The transaction hash of the ERC20 token transfer transaction.

        Raises:
            Exception: If there is an error during the transaction.
        """
        try:
            erc20_contract = self.web3.eth.contract(address=token_address, abi=token_abi)
            decimals = erc20_contract.functions.decimals().call()
            token_amount = amount * (10 ** decimals)

            tx = erc20_contract.functions.transfer(to_address, int(token_amount)).build_transaction({
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

    def ack_msg(self, message_id: int) -> str:
        """
        Acknowledges a message in the smart contract's inbox.

        Args:
            message_id (int): The ID of the message to acknowledge.

        Returns:
            str: The transaction hash of the message acknowledgment transaction.
        """
        tx = self.contract.functions.ackMsg(message_id).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': 3000000,
            'gasPrice': self.web3.to_wei('20', 'gwei')
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return self.web3.to_hex(tx_hash)

    def get_inbox(self) -> str:
        """
        Retrieves the first message from the smart contract's inbox.

        Returns:
            str: The content of the first message in the inbox, or None if an error occurs.
        """
        try:
            return self.contract.functions.inBox(0).call()
        except Exception as e:
            print("Error retrieving inbox message", e)
            return None
