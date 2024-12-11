from eth_account import Account
from web3 import Web3

from helpers.abi import factory_abi


class SAFactoryHelper:
    """
    A helper class for interacting with the SmartAgent factory contract, allowing deployment
    of new SmartAgent contracts and retrieval of existing agents.

    Attributes:
        web3 (Web3): An instance of Web3 for blockchain interaction.
        contract_address (str): The address of the SmartAgent factory contract.
        abi (list): The ABI (Application Binary Interface) of the factory contract.
        private_key (str): The private key of the account for signing transactions.
        account (Account): The Ethereum account derived from the private key.
        contract (Contract): An instance of the factory contract for interaction.
    """

    def __init__(self, provider_url: str, contract_address: str, private_key: str):
        """
        Initializes the SAFactoryHelper with the blockchain provider, contract details, and account credentials.

        Args:
            provider_url (str): The URL of the blockchain provider (e.g., Infura, Alchemy).
            contract_address (str): The address of the SmartAgent factory contract.
            private_key (str): The private key of the Ethereum account.
        """
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.abi = factory_abi
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def deploy_new_agent(self) -> str:
        """
        Deploys a new SmartAgent contract using the factory contract.

        If a SmartAgent contract already exists for the account, its address is returned.
        Otherwise, a new SmartAgent contract is created and its address is returned.

        Returns:
            str: The blockchain address of the deployed or existing SmartAgent.

        Raises:
            Exception: If an error occurs during transaction execution or address retrieval.
        """
        try:
            # Check if a SmartAgent already exists for this account
            existing_address = self.contract.functions.smartAgentContractMapping(self.account.address).call()

            # If an existing contract address is found, return it
            if existing_address != '0x0000000000000000000000000000000000000000':  # Default zero address
                print('Existing Smart Agent found at address: {}'.format(existing_address))
                return Web3.to_checksum_address(existing_address)

            # Build the transaction to create a new SmartAgent
            tx = self.contract.functions.createSmartAgent().build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'gas': 3000000,
                'gasPrice': self.web3.to_wei('20', 'gwei')
            })

            # Sign the transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)

            # Send the transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for the transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            # Decode the address of the new SmartAgent from logs
            hex_bytes = receipt.logs[0].topics[-1]
            new_address = Web3.to_checksum_address('0x' + hex_bytes.hex()[-40:])

            print('New Smart Agent deployed successfully at address: {}'.format(new_address))
            return new_address
        except Exception as e:
            print("Error deploying new SmartAgent", e)
            return None

    def get_all_smart_agents(self) -> list:
        """
        Retrieves a list of all SmartAgent addresses deployed by the factory contract.

        Returns:
            list: A list of blockchain addresses for all deployed SmartAgent contracts.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            # Get the total number of SmartAgent contracts
            agent_count = self.contract.functions.getSmartAgentCount().call()

            # Retrieve all SmartAgent addresses
            smart_agents = []
            for i in range(agent_count):
                agent_address = self.contract.functions.getSmartAgent(i).call()
                smart_agents.append(agent_address)

            return smart_agents
        except Exception as e:
            print("Error retrieving SmartAgents", e)
            return []
