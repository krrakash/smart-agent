agent_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_owner",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "messageId",
                "type": "uint256"
            }
        ],
        "name": "MessageAcknowledged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "receiver",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "messageId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "MessageSent",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "messageId",
                "type": "uint256"
            }
        ],
        "name": "ackMsg",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "addToInbox",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "inBox",
        "outputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
factory_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "creator",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "smartAgentAddress",
                "type": "address"
            }
        ],
        "name": "SmartAgentCreated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "createSmartAgent",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "getSmartAgent",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getSmartAgentCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "smartAgentContractMapping",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "smartAgents",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
erc20_abi = [
    {
        "inputs": [{"internalType": "address", "name": "recipient", "type": "address"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable",
        "type": "function"
    },
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf",
     "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view",
     "type": "function"},
    {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
     "stateMutability": "view", "type": "function"}
]