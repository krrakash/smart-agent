from agent import AutonomousAgent
from behaviours.check_balance_behaviour import CheckBalanceBehaviour
from behaviours.discover_agents_behaviour import DiscoverAgentsBehaviour
from behaviours.incoming_message_behaviour import IncomingMessageBehaviour
from behaviours.random_message_behaviour import RandomMessageBehaviour
from handlers.crypto_handler import CryptoHandler
from handlers.hello_handler import HelloHandler
from helpers.parse_arguments import parse_arguments, config

if __name__ == '__main__':
    parse_arguments()

    agent = AutonomousAgent(config.provider_url, config.private_key, config.factory_address)

    agent.register_behaviour(DiscoverAgentsBehaviour(agent))
    agent.register_behaviour(RandomMessageBehaviour(agent))
    agent.register_behaviour(CheckBalanceBehaviour(agent))
    agent.register_behaviour(IncomingMessageBehaviour(agent))

    agent.register_handler(HelloHandler(agent))
    agent.register_handler(CryptoHandler(agent))

    agent.run()

