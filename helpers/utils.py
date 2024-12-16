import os

from server.http_server_impl import HTTPServerImpl
from server.socket_server_impl import SocketServerImpl

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


def get_server_instance() -> HTTPServerImpl | SocketServerImpl:
    mode = os.getenv("SERVER_MODE", "socket")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    peer_host = os.getenv("OUTBOX_HOST")
    peer_port = os.getenv("OUTBOX_PORT")
    os.getenv("OUTBOX_PORT")
    print(f"Starting server on {mode}://{host}:{port}")
    if mode == "http":
        return HTTPServerImpl(host, port, peer_host, peer_port)
    else:
        return SocketServerImpl(host, port, peer_host, peer_port)
