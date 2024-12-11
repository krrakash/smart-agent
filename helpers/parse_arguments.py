import argparse
from types import SimpleNamespace

data = {
    "erc20_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "provider_url": None,
    "factory_address": None,
    "private_key": None
}
config = SimpleNamespace(**data)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse command-line arguments.")
    parser.add_argument("-k", "--key", type=str, help="Private key for the agent", default=0)
    parser.add_argument("-f", "--factory", type=str, help="Factory contract address", default=0)
    parser.add_argument("-r", "--rpc", type=str, help="RPC url for tenderly fork", default=0)
    parser.add_argument("-d", "--dai", type=str, help="Dai contract address", default=0)
    args = parser.parse_args()

    config.provider_url = args.rpc
    config.factory_address = args.factory
    config.private_key = args.key
    config.erc20_address = args.dai or "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    if not config.private_key:
        print("Private key must be provided to run the agent")
        exit(1)

    if not config.provider_url:
        print("Tenderdly rpc url must be provided to run the agent")
        exit(1)

    if not config.factory_address:
        print("Factory address must be provided to run the agent")
        exit(1)
