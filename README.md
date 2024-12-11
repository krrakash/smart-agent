```
docker build -t agent .

docker run agent \
-k your_private_key \
-f factory_address \
-r tenderly_rpc \
-d dai_address(optional)
```

Smart Agent Python Implementation
This project implements a Python-based autonomous agent system that interacts with Ethereum smart contracts, handles behaviors, and processes messages. The agent system includes:

Message Generation Behavior:
Generates random 2-word messages from a predefined set of 10 words every 2 seconds.
Message Filtering Handler:
Filters messages containing the keyword hello and prints them to stdout.
ERC-20 Token Balance Behavior:
Checks the ERC-20 token balance of an Ethereum address every 10 seconds and prints it to stdout.
ERC-20 Token Transfer Handler:
Filters messages for the keyword crypto and transfers 1 ERC-20 token unit from a source Ethereum address to a target Ethereum address, if sufficient balance is available.