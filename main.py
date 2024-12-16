import os

from agent import AutonomousAgent
from behaviours.check_balance_behaviour import CheckBalanceBehaviour
from behaviours.incoming_message_behaviour import IncomingMessageBehaviour
from behaviours.random_message_behaviour import RandomMessageBehaviour
from behaviours.send_message_behaviour import SendMessageBehaviour
from handlers.crypto_handler import CryptoHandler
from handlers.hello_handler import HelloHandler
import dotenv
dotenv.load_dotenv()

if __name__ == '__main__':
    agent = AutonomousAgent(os.getenv("PROVIDER_URL"), os.getenv("PRIVATE_KEY"))

    agent.register_behaviour(RandomMessageBehaviour(agent))
    agent.register_behaviour(SendMessageBehaviour(agent))
    agent.register_behaviour(CheckBalanceBehaviour(agent))
    agent.register_behaviour(IncomingMessageBehaviour(agent))

    agent.register_handler(HelloHandler(agent))
    agent.register_handler(CryptoHandler(agent))

    agent.run()

